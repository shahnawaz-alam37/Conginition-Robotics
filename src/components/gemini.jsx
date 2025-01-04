// Main function to communicate with backend
export async function analyzeImageWithPrompt(prompt, imageData) {
    try {
        const requestData = {
            prompt: prompt,
            image: imageData || null  // Ensure we send null if no image
        };

        console.log('Sending request with data:', {
            prompt,
            hasImage: !!imageData
        });

        const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Unknown error occurred');
        }

        return data.response;
    } catch (error) {
        console.error('Analysis error:', error);
        throw error;
    }
}