from flask import Flask, render_template
from flask_socketio import SocketIO
import speech_recognition as sr
import threading
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)
r = sr.Recognizer()
transcription_thread = None
transcribing = False

def record_text():
    time.sleep(1)
    return random.randint(0, 100)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            return text
    except:
        return ''

def transcribe():
    global transcribing
    while transcribing:
        text = str(record_text())
        socketio.emit('transcription', text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('start_transcription')
def handle_start_transcription():
    global transcription_thread, transcribing
    if not transcribing:
        transcribing = True
        transcription_thread = threading.Thread(target=transcribe)
        transcription_thread.start()

@socketio.on('stop_transcription')
def handle_stop_transcription():
    global transcription_thread, transcribing
    if transcribing:
        transcribing = False
        if transcription_thread.is_alive():
            transcription_thread.join()

if __name__ == '__main__':
    socketio.run(app)
