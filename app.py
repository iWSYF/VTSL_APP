from flask import Flask, render_template, request
from vosk import Model, KaldiRecognizer
import pyaudio
import json

app = Flask(__name__)

# Load Vosk model
model = Model(r"C:\\Users\\wsyf9\\OneDrive\\Desktop\\vosk-model-en-us-0.42-gigaspeech")

# Initialize recognizer and microphone stream
recognizer = KaldiRecognizer(model, 44100)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
stream.start_stream()

# List of stop words
stop_this_words = [
    "any", "much", "many", "a", "an", "the", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "he", "she", "it", "they",
    "and", "but", "or", "nor", "yet", "so"
]

# Main route
@app.route('/', methods=['GET', 'POST'])
def home():  # ✅ Changed from VoiceText to home
    text = ""
    words = []

    if request.method == 'POST':
        for _ in range(0, int(44100 / 1024 * 5)):  # Record for 3 seconds
            data = stream.read(1024)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += result.get('text', '') + ' '

        # Final result
        final_result = json.loads(recognizer.FinalResult())
        text += final_result.get('text', '')

        # Filter out stop words
        words = text.strip().split()
        filtered_words = [word for word in words if word.lower() not in stop_this_words]
        print("Filtered words:", filtered_words)

        return render_template('index.html', original_text=text.strip(), words=filtered_words)

    return render_template('index.html', original_text=None, words=None)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
