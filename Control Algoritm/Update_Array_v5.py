import random
from scipy.stats import rv_discrete
import pyaudio
import wave
import speech_recognition as sr
import _thread
import time
import serial
import os
import numpy as np
import RPi.GPIO as GPIO
import time

total_file_duration = 2
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 1
os.chdir("/home/antia/Desktop/connection")
filename = "/home/antia/Desktop/connection/commands.wav"
r = sr.Recognizer()
flag = 0
frames = []


ser = serial.Serial(
    port='/dev/ttyACM0',  # Change this according to connection methods, e.g. /dev/ttyUSB0
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
p = pyaudio.PyAudio()
stream = p.open(
    format=sample_format,
    channels=channels,
    rate=fs,
    frames_per_buffer=chunk,
    input=True
)

comm = 'sequence practicing'
last_comm = 'adjust speed'

user_pref = [0, 0, 0, 0, 0]
kubi_pico = [0, 0, 0, 0, 0]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
ball_count = 0

# Default settings
on_off_switch = 1
no_repeat_flag = 0
no_repeat_ct = 0
mode_changed = 0
foreground_feature = 'spin'
seq_counter = 0
random_vector = [random.randint(-2, 2), random.randint(0, 2), random.randint(0, 2), random.randint(-2, 2),
                 random.randint(-2, 2)]
operating_mode = 1   # operating mode (0: rep-prac; 1: seq-prac; 2: game-mode)
Is_random = 0   # randomness (0: regular; 1: random)
user_pref[0] = 0  # spin (-2,-1: backspin; 0: no spin; 1,2: topspin)
user_pref[1] = 1  # frequency (0,1,2)
user_pref[2] = 1  # speed (0,1,2,3)
user_pref[3] = 0  # direction (-2,-1: left; 0: mid; 1,2: right)
user_pref[4] = 0  # launching angle (-2,-1: down; 0: mid; 1,2: up)

try:
    num_of_balls_thrown = np.load("perf_data_thrown_balls.npy")
    num_of_balls_returned = np.load("perf_data_returned_balls.npy")
except FileNotFoundError:
    num_of_balls_thrown = np.zeros(21)  # 0-4:spin 5-7:freq 8-10:speed(1,2,3) 11-15:direction 16-20:launching_angle
    num_of_balls_returned = np.zeros(21)  # 0-4:spin 5-7:freq 8-10:speed(1,2,3) 11-15:direction 16-20:launching_angle

dummy_perf_data_spin = [0.3, 0.25, 0.1, 0.15, 0.2]
dummy_perf_data_freq = [0.2, 0.3, 0.5]
dummy_perf_data_speed = [0.1, 0.4, 0.5]
dummy_perf_data_dir = [0.25, 0.1, 0.3, 0.1, 0.25]
dummy_perf_data_lau_ang = [0.1, 0.2, 0.4, 0.2, 0.1]
r_spin = rv_discrete(name='r_spin', values=([-2, -1, 0, 1, 2], dummy_perf_data_spin))
r_freq = rv_discrete(name='r_freq', values=([0, 1, 2], dummy_perf_data_freq))
r_speed = rv_discrete(name='r_speed', values=([1, 2, 3], dummy_perf_data_speed))
r_dir = rv_discrete(name='r_dir', values=([-2, -1, 0, 1, 2], dummy_perf_data_dir))
r_lau_ang = rv_discrete(name='r_lau_ang', values=([-2, -1, 0, 1, 2], dummy_perf_data_lau_ang))

reset_counter = 0


def perf_data_update():
    global r_spin
    global r_freq
    global r_speed
    global r_dir
    global r_lau_ang
    nope = 0
    for value in num_of_balls_thrown:
        if value < 15:
            nope = 1
    if nope == 0:
        temp = 1 - (num_of_balls_returned / (num_of_balls_thrown+1))
        r_spin = rv_discrete(name='r_spin', values=([-2, -1, 0, 1, 2], temp[:5] / np.sum(temp[:5])))
        r_freq = rv_discrete(name='r_freq', values=([0, 1, 2], temp[5:8] / np.sum(temp[5:8])))
        r_speed = rv_discrete(name='r_speed', values=([1, 2, 3], temp[8:11] / np.sum(temp[8:11])))
        r_dir = rv_discrete(name='r_dir', values=([-2, -1, 0, 1, 2], temp[11:16] / np.sum(temp[11:16])))
        r_lau_ang = rv_discrete(name='r_lau_ang', values=([-2, -1, 0, 1, 2], temp[16:21] / np.sum(temp[16:21])))
    else:
        r_spin = rv_discrete(name='r_spin', values=([-2, -1, 0, 1, 2], dummy_perf_data_spin))
        r_freq = rv_discrete(name='r_freq', values=([0, 1, 2], dummy_perf_data_freq))
        r_speed = rv_discrete(name='r_speed', values=([1, 2, 3], dummy_perf_data_speed))
        r_dir = rv_discrete(name='r_dir', values=([-2, -1, 0, 1, 2], dummy_perf_data_dir))
        r_lau_ang = rv_discrete(name='r_lau_ang', values=([-2, -1, 0, 1, 2], dummy_perf_data_lau_ang))


def listener():
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
    global no_repeat_flag
    global sensor_thread_execute
    global reset_counter
    global num_of_balls_thrown
    global num_of_balls_returned

    if command == 'reset':
        reset_counter += 1
        if reset_counter >= 3:
            os.remove("/home/antia/Desktop/connection/perf_data_returned_balls.npy")
            os.remove("/home/antia/Desktop/connection/perf_data_thrown_balls.npy")
            num_of_balls_thrown = np.zeros(21)
            num_of_balls_returned = np.zeros(21)
            reset_counter = 0

    if command == 'start':
        on_off_switch = 1
    elif command == 'stop':
        on_off_switch = 0

    if on_off_switch == 1:
        if command in ['repetition practicing', 'petition practicing', 'repetition']:
            operating_mode = 0
            mode_changed = 1
            print('The verbal command: repetition practicing')
        elif command in ['sequence practicing', 'sequins practicing', 'sequence']:
            operating_mode = 1
            mode_changed = 1
            print('The verbal command: sequence practicing')
        elif command in ['gamemode', 'Gamo', 'game mode']:
            operating_mode = 2
            mode_changed = 1
            print('The verbal command: game mode')
        elif command in ['random']:
            Is_random = 1
            mode_changed = 1
            print('The verbal command: random')
        elif command in ['regular']:
            Is_random = 0
            print('The verbal command: regular')
        elif command in ['serving frequency', 'serving', 'frequency']:
            foreground_feature = 'serving frequency'
            print('The verbal command: serving frequency')
        elif command in ['adjust speed', 'speed']:
            foreground_feature = 'speed'
            print('The verbal command: speed')
        elif command in ['launching angle', 'launching Django']:
            foreground_feature = 'launching angle'
            print('The verbal command: launching angle')
        elif command in ['adjust spin', 'it just spin', 'just spin', 'adjustable spin']:
            foreground_feature = 'spin'
            print('The verbal command: spin')
        elif (command in ['right']) and data[3] != 2 and no_repeat_flag == 0:
            no_repeat_flag = 1
            data[3] = data[3] + 1
            print('The verbal command: right')
            if operating_mode == 0:
                sensor_thread_execute = 1
        elif (command in ['left']) and data[3] != -2 and no_repeat_flag == 0:
            no_repeat_flag = 1
            data[3] = data[3] - 1
            print('The verbal command: left')
            if operating_mode == 0:
                sensor_thread_execute = 1
        elif (command in ['low level', 'no level', 'low-level']) and no_repeat_flag == 0:
            no_repeat_flag = 1
            print('The verbal command: low level')
            if operating_mode == 0:
                sensor_thread_execute = 1
            if foreground_feature == 'spin' and data[0] != -2:
                data[0] = data[0] - 1
            elif foreground_feature == 'serving frequency':
                data[1] = 0
            elif foreground_feature == 'speed' and data[2] != 0:
                data[2] -= 1
            elif foreground_feature == 'launching angle' and data[4] != -2:
                data[4] = data[4] - 1
        elif (command in ['high level', 'hi level', 'hi Neville', 'high-level', 'volume level', 'I never',
                          'play devil', 'hi devil']) and no_repeat_flag == 0:
            no_repeat_flag = 1
            print('The verbal command: high level')
            if operating_mode == 0:
                sensor_thread_execute = 1
            if foreground_feature == 'spin' and data[0] != 2:
                data[0] = data[0] + 1
            elif foreground_feature == 'serving frequency':
                data[1] = 2
            elif foreground_feature == 'speed' and data[2] != 3:
                data[2] += 1
            elif foreground_feature == 'launching angle' and data[4] != 2:
                data[4] = data[4] + 1
        elif command in ['medium level']:
            print('The verbal command: medium level')
            if operating_mode == 0:
                sensor_thread_execute = 1
            if foreground_feature == 'spin':
                data[0] = 0
            elif foreground_feature == 'serving frequency':
                data[1] = 1
            elif foreground_feature == 'speed':
                data[2] = 2
            elif foreground_feature == 'launching angle':
                data[4] = 0
    return data


def myf(commands):
    while True:
        global comm
        global user_pref
        global no_repeat_flag
        global no_repeat_ct
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
                print('What recognizer understood:', text)
                user_pref = update_data(text, user_pref)
            except sr.UnknownValueError:
                pass

        if no_repeat_flag == 1:
            no_repeat_ct += 1
        if no_repeat_ct == 4:
            no_repeat_flag = 0
            no_repeat_ct = 0


def send_data(msg_list):
    msg = "{} {} {} {} {} {} {}".format(msg_list[0], msg_list[1], msg_list[2], msg_list[3], msg_list[4],
                                        msg_list[5], msg_list[6])
    print("Message {} is sent".format(msg))
    ser.write(msg.encode('utf-8'))


def read_ultrasonic_sensor():
    global ball_count
    global sensor_thread_running
    pulse_end = 0
    pulse_start = 0
    while True:
        if sensor_thread_execute == 1:
            sensor_thread_running = 0
            break

        GPIO.output(TRIG, False)

        time.sleep(0.5)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        if distance < 20:
            ball_count += 1


sensor_thread_execute = 0
sensor_thread_running = 0
k = 0
listener_thread = _thread.start_new_thread(listener, ())
recognition_thread = _thread.start_new_thread(myf, (frames,))
while True:
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
    if operating_mode == 0 and Is_random == 0:
        if sensor_thread_running == 0:
            _thread.start_new_thread(read_ultrasonic_sensor, ())
            sensor_thread_running = 1
        if sensor_thread_execute == 1:
            num_of_balls_thrown[kubi_pico[0]+2] += ball_count
            num_of_balls_thrown[kubi_pico[1]+5] += ball_count
            num_of_balls_thrown[kubi_pico[2]+7] += ball_count
            num_of_balls_thrown[kubi_pico[3]+13] += ball_count
            num_of_balls_thrown[kubi_pico[4]+18] += ball_count
            print(num_of_balls_thrown)
            ball_count = 0
            sensor_thread_execute = 0
        perf_data_update()
    sensor_thread_execute = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('To raspberry pico: ', kubi_pico)
    print('foreground feature: ', foreground_feature)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    kubi_pico.append(foreground_feature)
    kubi_pico.append(operating_mode)
    send_data(kubi_pico)
    kubi_pico.pop()
    kubi_pico.pop()
    k += 1
    if k == 31:
        k = 0
        recognition_thread = _thread.start_new_thread(myf, (frames,))
    np.save("perf_data_thrown_balls.npy", num_of_balls_thrown)
    np.save("perf_data_returned_balls.npy", num_of_balls_returned)
    time.sleep(seconds)
