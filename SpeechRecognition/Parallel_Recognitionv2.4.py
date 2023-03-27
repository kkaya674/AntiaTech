# working version
import pyaudio
import wave
import speech_recognition as sr
import _thread
import time

total_file_duration = 2
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 1
filename = "commands.wav"
r = sr.Recognizer()
flag = 0


def myf(commands):
    t = time.time()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(commands))
    wf.close()

    with sr.AudioFile(filename) as source:
        try:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(text)
        except sr.UnknownValueError:
            print("Didn't get the command")
    elapsed_time = time.time() - t
    print('elapsed time while processing=')
    print(format(elapsed_time, '.5f'))


frames = []
frame_fill_counter = 0
Listening = True


def listener():
    print('Recording')
    while Listening:
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        while len(frames) > int(total_file_duration * fs / chunk * seconds):
            frames.pop(0)


p = pyaudio.PyAudio()
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

listener_thread = _thread.start_new_thread(listener, ())
while Listening:
    time.sleep(seconds)
    process_thread = _thread.start_new_thread(myf, (frames,))
