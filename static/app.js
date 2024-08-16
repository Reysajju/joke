async function processImage() {
    const imageInput = document.getElementById('imageInput').files[0];
    const outputDiv = document.getElementById('output');

    if (imageInput) {
        const formData = new FormData();
        formData.append('image', imageInput);

        // Send the image to the backend for processing
        const response = await fetch('/process-image', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        outputDiv.innerHTML = `<p>Image Description: ${result.image_text}</p>`;
        outputDiv.innerHTML += `<p>Generated Joke: ${result.joke}</p>`;
    } else {
        outputDiv.innerHTML = '<p>Please upload an image.</p>';
    }
}

async function speakText() {
    const outputDiv = document.getElementById('output');
    const joke = outputDiv.querySelector('p:last-child').textContent.replace('Generated Joke: ', '');

    if (joke) {
        // Send the joke to the backend for TTS
        const response = await fetch('/speak-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: joke })
        });
        
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audioElement = new Audio(audioUrl);
        audioElement.play();
    } else {
        alert('Please generate a joke first.');
    }
}
