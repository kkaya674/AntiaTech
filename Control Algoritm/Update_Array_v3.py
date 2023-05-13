import random
from scipy.stats import rv_discrete
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
frames = []

p = pyaudio.PyAudio()
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

comm = 'repetition practicing'
last_comm = 'speed'

user_pref = [0, 0, 0, 0, 0]
kubi_pico = user_pref

# Default settings
on_off_switch = 1
mode_changed = 0
foreground_feature = 'spin'
seq_counter = 0
random_vector = [random.randint(-2, 2), random.randint(0, 2), random.randint(0, 2), random.randint(-2, 2),
                 random.randint(-2, 2)]
operating_mode = 0   # operating mode (0: rep-prac; 1: seq-prac; 2: game-mode)
Is_random = 0   # randomness (0: regular; 1: random)
user_pref[0] = 0  # spin (-2,-1: backspin; 0: no spin; 1,2: topspin)
user_pref[1] = 1  # frequency (0,1,2)
user_pref[2] = 1  # speed (0,1,2)
user_pref[3] = 0  # direction (-2,-1: left; 0: mid; 1,2: right)
user_pref[4] = 0  # launching angle (-2,-1: down; 0: mid; 1,2: up)

dummy_perf_data_spin = [0.3, 0.2, 0.1, 0.2, 0.2]
r_spin = rv_discrete(name='r_spin', values=([-2, -1, 0, 1, 2], dummy_perf_data_spin))
dummy_perf_data_freq = [0.2, 0.3, 0.5]
r_freq = rv_discrete(name='r_freq', values=([0, 1, 2], dummy_perf_data_freq))
dummy_perf_data_speed = [0.1, 0.4, 0.5]
r_speed = rv_discrete(name='r_speed', values=([0, 1, 2], dummy_perf_data_speed))
dummy_perf_data_dir = [0.2, 0.3, 0.1, 0.2, 0.2]
r_dir = rv_discrete(name='r_dir', values=([-2, -1, 0, 1, 2], dummy_perf_data_dir))
dummy_perf_data_lau_ang = [0.1, 0.2, 0.3, 0.2, 0.2]
r_lau_ang = rv_discrete(name='r_lau_ang', values=([-2, -1, 0, 1, 2], dummy_perf_data_lau_ang))


def listener():
    print('Recording')
    while True:
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        while len(frames) > int(total_file_duration * fs / chunk * seconds):
            frames.pop(0)


def motor_parameters(op_mode, rand, data, counter, vec_random, last_data_pico, switch):
    if switch == 1:
        if op_mode == 0:  # repetition practicing
            if rand == 0:  # regular repetition practicing
                data_pico = data
            else:  # random repetition practicing
                data_pico = vec_random

        elif op_mode == 1:  # sequence practicing
            if rand == 0:  # regular sequence practicing
                if counter == 1:
                    data_pico = [0, 1, 0, -2, -1]
                elif counter == 2:
                    data_pico = [0, 1, 0, 2, -1]
                elif counter == 3:
                    data_pico = [0, 1, 0, 2, 1]
                else:
                    data_pico = [0, 1, 1, 0, 1]
            else:  # random sequence practicing
                if counter == 1:
                    data_pico = [vec_random[0], 1, 0, -2, -1]
                elif counter == 2:
                    data_pico = [vec_random[0], 1, 0, vec_random[3], -1]
                elif counter == 3:
                    data_pico = [vec_random[0], 1, 0, vec_random[3], vec_random[4]]
                else:
                    data_pico = [vec_random[0], 1, vec_random[2], vec_random[3], vec_random[4]]

        else:  # game mode
            param = random.randint(1, 5)
            if param == 1:
                data_pico = last_data_pico
                data_pico[0] = int(r_spin.rvs(size=1))
            elif param == 2:
                data_pico = last_data_pico
                data_pico[1] = int(r_freq.rvs(size=1))
            elif param == 3:
                data_pico = last_data_pico
                data_pico[2] = int(r_speed.rvs(size=1))
            elif param == 4:
                data_pico = last_data_pico
                data_pico[3] = int(r_dir.rvs(size=1))
            else:
                data_pico = last_data_pico
                data_pico[4] = int(r_lau_ang.rvs(size=1))

        return data_pico
    else:
        pass


def update_data(command, data):

    global operating_mode
    global Is_random
    global mode_changed
    global foreground_feature
    global on_off_switch

    if command == 'start':
        on_off_switch = 1
    elif command == 'stop':
        on_off_switch = 0

    if on_off_switch == 1:
        if command == 'repetition practicing' or command == 'petition practicing':
            operating_mode = 0
            mode_changed = 1
            print('The verbal command: repetition practicing')
        elif command == 'sequence practicing' or command == 'sequins practicing':
            operating_mode = 1
            mode_changed = 1
            print('The verbal command: sequence practicing')
        elif command == 'gamemode' or command == 'Gamo' or command == 'game mode':
            operating_mode = 2
            mode_changed = 1
            print('The verbal command: game mode')
        elif command == 'random':
            Is_random = 1
            mode_changed = 1
            print('The verbal command: random')
        elif command == 'regular':
            Is_random = 0
            print('The verbal command: regular')
        elif command == 'serving frequency':
            foreground_feature = 'serving frequency'
            print('The verbal command: serving frequency')
        elif command == 'speed' or command == 'peed':
            foreground_feature = 'speed'
            print('The verbal command: speed')
        elif command == 'launching angle' or command == 'launching Django':
            foreground_feature = 'launching angle'
            print('The verbal command: launching angle')
        elif command == 'spin':
            foreground_feature = 'spin'
            print('The verbal command: spin')
        elif command == 'right' and data[3] != 2:
            data[3] = data[3] + 1
            print('The verbal command: right')
        elif command == 'middle':
            data[3] = 0
            print('The verbal command: middle')
        elif command == 'left' and data[3] != -2:
            data[3] = data[3] - 1
            print('The verbal command: left')
        elif command == 'low level' or command == 'no level' or command == 'low-level':
            print('The verbal command: low level')
            if foreground_feature == 'spin' and data[0] != -2:
                data[0] = data[0] - 1
            elif foreground_feature == 'serving frequency':
                data[1] = 0
            elif foreground_feature == 'speed':
                data[2] = 0
            elif foreground_feature == 'launching angle' and data[4] != -2:
                data[4] = data[4] - 1
        elif command == 'high level' or command == 'hi level' or command == 'hi Neville'\
                or command == 'high-level' or command == 'volume level' or command == 'I never':
            print('The verbal command: high level')
            if foreground_feature == 'spin' and data[0] != 2:
                data[0] = data[0] + 1
            elif foreground_feature == 'serving frequency':
                data[1] = 2
            elif foreground_feature == 'speed':
                data[2] = 2
            elif foreground_feature == 'launching angle' and data[4] != 2:
                data[4] = data[4] + 1
        elif command == 'medium level':
            print('The verbal command: medium level')
            if foreground_feature == 'spin':
                data[0] = 0
            elif foreground_feature == 'serving frequency':
                data[1] = 1
            elif foreground_feature == 'speed':
                data[2] = 1
            elif foreground_feature == 'launching angle':
                data[4] = 0
    return data


def myf(commands):
    while True:
        time.sleep(seconds)
        global comm
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
                comm = text
                print('What recognizer understood:', text)
            except sr.UnknownValueError:
                pass


listener_thread = _thread.start_new_thread(listener, ())
recognition_thread = _thread.start_new_thread(myf, (frames,))
while True:
    user_pref = update_data(comm, user_pref)
    if operating_mode == 1:
        seq_counter += 1
    if mode_changed == 1:
        random_vector = [random.randint(-2, 2), random.randint(0, 2), random.randint(0, 2), random.randint(-2, 2),
                         random.randint(-2, 2)]
        mode_changed = 0
        seq_counter = 1
    kubi_pico = motor_parameters(operating_mode, Is_random, user_pref, seq_counter, random_vector,
                                 kubi_pico, on_off_switch)
    if seq_counter == 4:
        seq_counter = 0
    print('---------------------------------------')
    print('To rasp. pico: ', kubi_pico)
    print('foreground feature: ', foreground_feature)
    print('---------------------------------------')
    time.sleep(seconds)