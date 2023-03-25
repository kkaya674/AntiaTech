import pyaudio
import wave
import speech_recognition as sr
import time
import threading

# not working

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 3
filename = "commands.wav"
filename2 = "commands_.wav"
r = sr.Recognizer()
dummy_variable = 1
first_recording_ok = 0
second_recording_ok = 0


def record_audio():
    time.sleep(1)
    p = pyaudio.PyAudio()
    print('Recording to first file')
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
    print('Finished recording 1')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def record_audio_parallel():
    time.sleep(1)
    p_ = pyaudio.PyAudio()
    print('Recording to second file')
    stream = p_.open(format=sample_format,
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
    p_.terminate()
    print('Finished recording 2')

    wf = wave.open(filename2, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p_.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def recognize_commands(file_name):
    with sr.AudioFile(file_name) as source:
        try:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(text)
        except sr.UnknownValueError:
            print("Didn't get the command")


Listening = True

while Listening:
    threading.Thread(target=record_audio()).start()
    if dummy_variable == 1:
        time.sleep(2)
        dummy_variable = 0
    threading.Thread(target=record_audio_parallel()).start()
    if first_recording_ok == 1:
        threading.Thread(target=recognize_commands(filename)).start()
        first_recording_ok = 0
    elif second_recording_ok == 1:
        threading.Thread(target=recognize_commands(filename2)).start()
        second_recording_ok = 0
