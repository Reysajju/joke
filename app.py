from flask import Flask, render_template, request, jsonify, send_file
from transformers import pipeline
import io

app = Flask(__name__)

# Load pipelines
image_to_text_pipeline = pipeline('image-to-text', 'Xenova/vit-gpt2-image-captioning')
text_generation_pipeline = pipeline('text-generation', 'Xenova/llama2.c-stories15M')
text_to_speech_pipeline = pipeline('text-to-speech', 'Xenova/speecht5_tts')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    # Get the image from the request
    image = request.files['image'].read()

    # Convert image to text
    image_text = image_to_text_pipeline(image)

    # Generate a joke based on the image text
    joke = text_generation_pipeline(image_text)[0]['generated_text']

    # Return the result as JSON
    return jsonify({'image_text': image_text, 'joke': joke})

@app.route('/speak-text', methods=['POST'])
def speak_text():
    # Get the joke text from the request
    text = request.json['text']

    # Convert text to speech
    audio = text_to_speech_pipeline(text)

    # Convert the generated audio to a file-like object
    audio_file = io.BytesIO(audio)
    audio_file.seek(0)

    # Send the audio file as a response
    return send_file(audio_file, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)
