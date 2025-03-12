from flask import Flask, render_template, request
from vosk import Model, KaldiRecognizer
import pyaudio
import json

app = Flask(__name__)


model = Model(r"C:\\Users\\wsyf9\\OneDrive\\Desktop\\vosk-model-en-us-0.42-gigaspeech")
# C:\\Users\\Wail Mawa\\Desktop\\vosk-model-en-us-0.22 MSI Wail
# C:\\Users\\wsyf9\\OneDrive\\Desktop\\vosk-model-en-us-0.42-gigaspeech PC Wail

recognizer = KaldiRecognizer(model, 44100)
# Mic setup
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
stream.start_stream()

# List of stop words
stop_this_words = [
    "some", "any", "much", "many", "few", "several",
    "a", "an", "the", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "I", "you", "he", "she", "it", "we", "they",
    "and", "but", "or", "nor", "yet", "so"
]

# Server route to process voice input
@app.route('/', methods=['GET', 'POST'])
def VoiceText():
    text = ""  # Spoken text
    words = []  # List of words after filtering

    if request.method == 'POST':
        for _ in range(0, int(44100 / 1024 * 4)):  # Record for 3 seconds
            data = stream.read(1024)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += result.get('text', '') + ' '

        # Process the final recognized speech
        final_result = json.loads(recognizer.FinalResult())
        text += final_result.get('text', '')

        # Split the full text into words
        words = text.strip().split()

        # Remove stop words from the list 'stop_this_words'
        filtered_words = [word for word in words if word.lower() not in stop_this_words]
        print("Filtered words:", filtered_words)

        # Render the result on the webpage
        return render_template('index.html', original_text=text.strip(), words=filtered_words)
    
    # If it's a GET request, render the template with no initial text
    return render_template('index.html', original_text=None, words=None)

# Start the Flask web server in debug mode (reload mode, عرض رسائل الخطأ التفصيلية (Interactive Debugger),  )
if __name__ == '__main__':
    app.run(debug=True)