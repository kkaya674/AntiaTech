import pyaudio
import wave
import speech_recognition as sr
import threading

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 1.5
filename = "commands.wav"
r = sr.Recognizer()


def myf():
    with sr.AudioFile(filename) as source:
        try:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(text)
        except sr.UnknownValueError:
            print("Didn't get the command")


Listening = True
while Listening:
    p = pyaudio.PyAudio()
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    threading.Thread(target=myf).start()
    