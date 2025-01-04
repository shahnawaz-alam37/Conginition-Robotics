from flask import Flask, request, jsonify
import google.generativeai as genai
import base64
from flask_cors import CORS
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)   

# Configuration
API_KEY = "AIzaSyCUlzJMebCtvPS_F1DtGPdKCOJIRUzbUY0"
MODEL_NAME = "models/gemini-2.0-flash-exp"

# Initialize AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def process_image_data(base64_image):
    try:
        # Remove header if present
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_image)
        
        # Convert to PIL Image
        image = Image.open(BytesIO(image_bytes))
        
        # Process image if needed (resize, convert, etc.)
        # image = image.resize((800, 600))
        
        # Convert back to bytes
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return buffered.getvalue()
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise e

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        image_data = data.get('image')

        # Construct the prompt for the robot arm
        main_prompt = f"""You are a robotic ARM controller. Analyze this image and provide JSON response with:
        1. Object coordinates (x,y,z)
        2. Required operations
        3. Movement sequence
        Task description: {prompt}"""

        if image_data:
            # Process the image
            processed_image = process_image_data(image_data)
            # Create parts with both text and image
            parts = [
                {"text": main_prompt},
                {"image": processed_image}
            ]
        else:
            # If no image, just use text
            parts = [{"text": main_prompt}]

        # Generate response
        response = model.generate_content(parts)
        print(response.text)
        
        return jsonify({
            "success": True,
            "response": response.text,
            "status": "completed"
        })

    except Exception as e:
        print(f"Error in analyze_image: {str(e)}")  # Add debug logging
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 