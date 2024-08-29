from flask import Flask, request, jsonify, render_template
from chatbot.chat import chat_with_gpt
import os
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    response = chat_with_gpt(prompt)
    return jsonify({'response': response})

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if prompt.lower() in ["hello", "hi", "hey"]:
        return jsonify({'response': "Hello! How can I assist you today?"})
    response = chat_with_gpt(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    response = chat_with_gpt(prompt)
    return jsonify({'response': response})

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if prompt.lower() in ["help", "commands"]:
        return jsonify({'response': "You can ask me about various topics or say 'quit' to exit."})
    response = chat_with_gpt(prompt)
    return jsonify({'response': response})

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    response = chat_with_gpt(prompt)
    engine.say(response)
    engine.runAndWait()
    return jsonify({'response': response})

@app.route('/voice', methods=['POST'])
def voice():
    recognizer = sr.Recognizer()
    audio_file = request.files['file']
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        prompt = recognizer.recognize_google(audio)
        response = chat_with_gpt(prompt)
        engine.say(response)
        engine.runAndWait()
        return jsonify({'response': response})
    except sr.UnknownValueError:
        return jsonify({'response': "Sorry, I could not understand the audio."})
    except sr.RequestError as e:
        return jsonify({'response': f"Could not request results; {e}"})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'response': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'response': 'No selected file'})
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        # Process the file using Gemini API
        response = process_image(filename)
        return jsonify({'response': response})

def process_image(filepath):
    # Implement your image processing logic here
    return "Image processed successfully."

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
