from flask import Flask, render_template, request
from vosk import Model, KaldiRecognizer
import pyaudio
import json

app = Flask(__name__)


model = Model(r"C:\\Users\\Wail Mawa\\Desktop\\vosk-model-en-us-0.22")
# C:\\Users\\Wail Mawa\\Desktop\\vosk-model-en-us-0.22 MSI Wail
# C:\\Users\\wsyf9\\OneDrive\\Desktop\\vosk-model-en-us-0.42-gigaspeech PC Wail
recognizer = KaldiRecognizer(model, 44100)
# Mic setup
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
stream.start_stream()

# Server
@app.route('/', methods=['GET', 'POST'])
def VoiceText():
    text = ""  # spoken text
    words = []  # store split words

    if request.method == 'POST':
        for _ in range(0, int(44100 / 1024 * 3)):  # Record for 3 seconds
            data = stream.read(1024)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += result.get('text', '') + ' '
        final_result = json.loads(recognizer.FinalResult())
        text += final_result.get('text', '')
        
        # Split text into words
        words = text.strip().split()
        print(words)
        
        return render_template('index.html', original_text=text.strip(), words=words)
    
    return render_template('index.html', original_text=None, words=None)

if __name__ == '__main__':
    app.run(debug=True)