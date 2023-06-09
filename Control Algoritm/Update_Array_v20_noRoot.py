import random
from scipy.stats import rv_discrete
import pyaudio
import wave
import speech_recognition as sr
import _thread
import serial
import os
import numpy as np
import RPi.GPIO as GPIO
import time
import socket
import re
import threading
import subprocess
from scapy.all import ARP, Ether, srp
import ast 

imageFlag = 0
vibrationFlag = 0


def get_local_ip():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server (doesn't matter which)
        sock.connect(("8.8.8.8", 80))
        # Get the local IP address
        local_ip = sock.getsockname()[0]
        # Close the socket
        sock.close()
        return local_ip
    except socket.error:
        return None



ser_vibration = serial.Serial("/dev/ttyS0", 9600)
ser_vibration.reset_input_buffer()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (get_local_ip(), 6005)
server_socket.bind(server_address)

num_synch = 0
LED = False

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

comm = 'repetition practicing'
last_comm = 'adjust speed'

user_pref = [0, 0, 0, 0, 0]
kubi_pico = [0, 0, 0, 0, 0]


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
step1 = 17
step2 = 18
step3 = 27
step4 = 22
TRIG = 23
ECHO = 24
LIGHT = 14
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(step1, GPIO.OUT)
GPIO.setup(step2, GPIO.OUT)
GPIO.setup(step3, GPIO.OUT)
GPIO.setup(step4, GPIO.OUT)

GPIO.output(step1, GPIO.LOW)
GPIO.output(step2, GPIO.LOW)
GPIO.output(step3, GPIO.LOW)
GPIO.output(step4, GPIO.LOW)

motor_pins = [step4, step3, step2, step1]
motor_step_counter = 0

step_count = 512

"""step_sequence = [[1, 0, 0, 1],
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1]]"""

step_sequence = [[1, 0, 0, 1],
                 [1, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 1]]
ball_count = 0


# Default settings
on_off_switch = 0
no_repeat_flag = 0
no_repeat_ct = 0
mode_changed = 0
foreground_feature = 'spin'
seq_counter = 0
random_vector = [random.randint(-2, 2), random.randint(0, 2), random.randint(0, 2), random.randint(-2, 2),
                 random.randint(-2, 2)]
operating_mode = 0  # operating mode (0: rep-prac; 1: seq-prac; 2: game-mode)
Is_random = 0  # randomness (0: regular; 1: random)
user_pref[0] = 0  # spin (-2,-1: backspin; 0: no spin; 1,2: topspin)
user_pref[1] = 1  # frequency (0,1,2)
user_pref[2] = 1  # speed (0,1,2,3)
user_pref[3] = 0  # direction (-2,-1: left; 0: mid; 1,2: right)
user_pref[4] = 0  # launching angle (-2,-1: down; 0: mid; 1,2: up)

try:
    with open('Perf_Data.txt', 'r') as f:
        content = f.read()
    f.close()
    integers = re.findall(r'\d+', content)
    integer_array = [int(num) for num in integers]
    if len(integer_array) == 42:
        num_of_balls_thrown = integer_array[:21]
        num_of_balls_returned = integer_array[-21:]
    else:
        num_of_balls_thrown = np.zeros(21)  # 0-4:spin 5-7:freq 8-10:speed(1,2,3) 11-15:direction 16-20:launching_angle
        num_of_balls_returned = np.zeros(21)
except FileNotFoundError:
    num_of_balls_thrown = np.zeros(21)
    num_of_balls_returned = np.zeros(21)

print(num_of_balls_thrown)
print(num_of_balls_returned)

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

r_game_mode = rv_discrete(name='param', values=([1, 2, 3, 4, 5, 6, 7, 8, 9], [0.28, 0.21, 0.21, 0.04,
                                                                              0.03, 0.03, 0.08, 0.06, 0.06]))

freq_changed = 0
reset_counter = 0
execute_step = 0


def MACtoIP(target_ip="192.168.65.1/24"):
    
    
    result = subprocess.run(["sudo","python", "/home/antia/Desktop/connection/macToIp.py",target_ip], capture_output=True)
    result = result.stdout
    result = result.decode().strip()
    result = ast.literal_eval(result)
    print(100*"-")
    print(result)
    

    return result


def findIP(clients, MAC = "8c:c6:81:3b:c9:87"):
    for client in clients:
        if client['mac'] == MAC:
            return client['ip']


def connectToUserInterface(hostname):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((hostname,8080))
    except:
        print("User Interface - TrainingBuddy bağlantısı kurulamadı")
        return None
    client_socket.setblocking(False)
    return client_socket


def readUserInterface(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            data = data.decode('utf-8')
            return data
        else:
            return None
    except:
        pass


def afer_computer_ip():
    # Call the function to retrieve the local IP address
    local_ip_address = get_local_ip()
    local_ip_address = local_ip_address.split('.')
    target_ip_range = local_ip_address[0]+'.'+local_ip_address[1]+'.'+local_ip_address[2]+'.1/24'
    clients = MACtoIP(target_ip_range)
    afer_computer_ip = findIP(clients=clients)
    return afer_computer_ip


User_interface_command = [0] * 7
User_interface_flag = 0
connection = None


def user_Interface():
    timeout = 10
    prev_data = [0] * 5
    global connection
    global User_interface_command
    global User_interface_flag
    global sensor_thread_execute
    while 1:
        connection = None
        while connection == None:
            connection = connectToUserInterface(afer_computer_ip())
        print("Connection to userInterface has been established...")
        checkTime = time.time()

        while True:
            data = readUserInterface(connection)
            elapsed_time = time.time() - checkTime
            if data != None:
                if "InterfaceON" in data:
                    checkTime = time.time()
                if "]" in data:
                    lastIndex = data.rindex("]")
                    lastCommand = data[lastIndex - 15:]
                    data = [int(lastCommand[2])-2, int(lastCommand[4])-2, int(lastCommand[6])-2, int(lastCommand[8])-2,
                            int(lastCommand[10])-2, int(lastCommand[12])-2, int(lastCommand[14])-2]
                    print(data)
                    User_interface_command = data
                    User_interface_flag = 1
                    if prev_data != data[:5]:
                        sensor_thread_execute = 1
                    prev_data = data[:5]

            if elapsed_time > timeout:
                print("Timeout Occured!, possible connection lost.")
                break

            time.sleep(1)
            # print("## DO OTHER STUFF HERE")
        connection.close()


def step_motor(sleep):
    global execute_step
    global motor_step_counter
    print('step calisior')
    while True:
        if execute_step == 1:
            execute_step = 0
            break
        for i in range(step_count):
            if execute_step == 1:
                break
            for j in range(4):
                GPIO.output(motor_pins[3], step_sequence[j][0])
                GPIO.output(motor_pins[2], step_sequence[j][1])
                GPIO.output(motor_pins[1], step_sequence[j][2])
                GPIO.output(motor_pins[0], step_sequence[j][3])
                time.sleep(sleep)


def image_reset():
    global imageFlag
    imageFlag = 0
    # print("image timer up and image flag cleared")


def vibration_reset():
    global vibrationFlag
    vibrationFlag = 0
    # print("vibration timer up and vibration flag cleared")


def vibrationTimer():
    vibrationTimer = threading.Timer(1, vibration_reset)
    vibrationTimer.start()


def imageTimer():
    imageTimer = threading.Timer(1, image_reset)
    imageTimer.start()


def checkSync():
    global num_synch
    global imageFlag
    global vibrationFlag
    if imageFlag and vibrationFlag:
        print("SYNCHRONIZATION!!!")
        if operating_mode == 0 and Is_random == 0:
            num_synch += 1
    else:
        if imageFlag:
            print("ONLY IMAGE!!!")
            pass
        else:
            if vibrationFlag:
                print("ONLY VIBRATION!!!")
                pass


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
        temp = 1 - (num_of_balls_returned / (num_of_balls_thrown + 1))
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
                data_pico = data
                for i in np.arange(2):
                    mp_rand = random.randint(0, 4)
                    data_pico[mp_rand] = vec_random[mp_rand]

        elif op_mode == 1:  # sequence practicing
            if rand == 0:  # regular sequence practicing
                if counter == 1:
                    data_pico = [0, 1, 1, -2, 1]
                elif counter == 2:
                    data_pico = [2, 1, 2, 0, 2]
                elif counter == 3:
                    data_pico = [0, 1, 3, -1, -2]
                else:
                    data_pico = [-2, 1, 2, 2, 0]
            else:  # random sequence practicing
                if counter == 1:
                    data_pico = [vec_random[0], 1, 3, -2, vec_random[4]]
                elif counter == 2:
                    data_pico = [0, 1, 2, vec_random[3], -1]
                elif counter == 3:
                    data_pico = [vec_random[0], 1, 3, 1, 0]
                else:
                    data_pico = [2, 1, vec_random[2], vec_random[3], vec_random[4]]

        else:  # game mode
            param = int(r_game_mode.rvs(size=1))
            if param == 1:
                data_pico = last_data_pico
                data_pico[4] = int(r_lau_ang.rvs(size=1))
                data_pico[3] = int(r_dir.rvs(size=1))
            elif param == 2:
                data_pico = last_data_pico
                data_pico[3] = int(r_dir.rvs(size=1))
                data_pico[2] = int(r_speed.rvs(size=1))
            elif param == 3:
                data_pico = last_data_pico
                data_pico[4] = int(r_lau_ang.rvs(size=1))
                data_pico[2] = int(r_speed.rvs(size=1))
            elif param == 4:
                data_pico = last_data_pico
                data_pico[1] = int(r_freq.rvs(size=1))
                data_pico[4] = int(r_lau_ang.rvs(size=1))
                data_pico[3] = int(r_dir.rvs(size=1))
            elif param == 5:
                data_pico = last_data_pico
                data_pico[1] = int(r_freq.rvs(size=1))
                data_pico[3] = int(r_dir.rvs(size=1))
                data_pico[2] = int(r_speed.rvs(size=1))
            elif param == 6:
                data_pico = last_data_pico
                data_pico[1] = int(r_freq.rvs(size=1))
                data_pico[4] = int(r_lau_ang.rvs(size=1))
                data_pico[2] = int(r_speed.rvs(size=1))
            elif param == 7:
                data_pico = last_data_pico
                data_pico[0] = int(r_spin.rvs(size=1))
                data_pico[4] = int(r_lau_ang.rvs(size=1))
                data_pico[3] = int(r_dir.rvs(size=1))
            elif param == 8:
                data_pico = last_data_pico
                data_pico[0] = int(r_spin.rvs(size=1))
                data_pico[3] = int(r_dir.rvs(size=1))
                data_pico[2] = int(r_speed.rvs(size=1))
            else:
                data_pico = last_data_pico
                data_pico[0] = int(r_spin.rvs(size=1))
                data_pico[4] = int(r_lau_ang.rvs(size=1))
                data_pico[2] = int(r_speed.rvs(size=1))
    else:
        data_pico = [0] * 5
    return data_pico


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
    global LED
    global freq_changed

    if command == 'reset':
        reset_counter += 1
        print('The verbal command: reset')
        if reset_counter >= 3:
            num_of_balls_returned = np.zeros(21)
            num_of_balls_thrown = np.zeros(21)
            reset_counter = 0

    if command in ['wake up', 'wake', 'wakeup']:
        on_off_switch = 1
        LED = not LED
        print('The verbal command: wake up')
    elif command in ['sleep', 'leaf', 'leap', 'leave', 'sleeve', 'Fleet', 'lead']:
        on_off_switch = 0
        LED = not LED
        print('The verbal command: sleep')

    if on_off_switch == 1:
        if command in ['repetition practicing', 'petition practicing', 'repetition', 'the petition practicing',
                       'repetition practice']:
            operating_mode = 0
            mode_changed = 1
            LED = not LED
            print('The verbal command: repetition practicing')
        elif command in ['sequence practicing', 'sequins practicing', 'sequence',
                         'sequence practice'] or 'sequence' in command:
            operating_mode = 1
            mode_changed = 1
            LED = not LED
            print('The verbal command: sequence practicing')
        elif command in ['gamemode', 'Gamo', 'game mode', 'game']:
            operating_mode = 2
            mode_changed = 1
            LED = not LED
            print('The verbal command: game mode')
        elif command in ['random', 'Lando', 'Rondo', 'Randa', 'Brando', 'blando', 'Rhonda']:
            Is_random = 1
            LED = not LED
            mode_changed = 1
            print('The verbal command: random')
        elif command in ['regular', 'Reggie', 'regimen']:
            Is_random = 0
            LED = not LED
            print('The verbal command: regular')
        elif command in ['serving frequency', 'serving', 'frequency', 'starving frequency', 'starving',
                         'starting frequency', 'starting'] or 'serving' in command or 'frequency' in command:
            foreground_feature = 'serving frequency'
            LED = not LED
            print('The verbal command: serving frequency')
        elif command in ['adjust speed', 'speed', 'peed', 'adjust peed', 'just speed',
                         'it just speed'] or 'speed' in command:
            foreground_feature = 'speed'
            LED = not LED
            print('The verbal command: speed')
        elif command in ['launching angle', 'launching Django', 'launch in Django']:
            foreground_feature = 'launching angle'
            LED = not LED
            print('The verbal command: launching angle')
        elif command in ['adjust spin', 'it just spin', 'just spin', 'adjustable spin', 'adjust spins']:
            foreground_feature = 'spin'
            LED = not LED
            print('The verbal command: spin')
        elif (command in ['right']) and data[3] != 2 and no_repeat_flag == 0:
            no_repeat_flag = 1
            data[3] = data[3] + 1
            LED = not LED
            print('The verbal command: right')
            if operating_mode == 0:
                sensor_thread_execute = 1
        elif (command in ['left']) and data[3] != -2 and no_repeat_flag == 0:
            no_repeat_flag = 1
            data[3] = data[3] - 1
            LED = not LED
            print('The verbal command: left')
            if operating_mode == 0:
                sensor_thread_execute = 1
        elif (command in ['low level', 'no level', 'low-level', 'low levels',
                          'low'] or 'low' in command) and no_repeat_flag == 0:
            no_repeat_flag = 1
            LED = not LED
            print('The verbal command: low level')
            if operating_mode == 0:
                sensor_thread_execute = 1
            if foreground_feature == 'spin' and data[0] != -2:
                data[0] = data[0] - 1
            elif foreground_feature == 'serving frequency':
                data[1] = 0
                freq_changed = 1
            elif foreground_feature == 'speed' and data[2] != 0:
                data[2] -= 1
            elif foreground_feature == 'launching angle' and data[4] != -2:
                data[4] = data[4] - 1
        elif (command in ['high level', 'hi level', 'hi Neville', 'high-level', 'volume level', 'I never',
                          'play devil', 'hi devil', 'high levels',
                          'high', 'hi'] or 'high' in command) and no_repeat_flag == 0:
            no_repeat_flag = 1
            LED = not LED
            print('The verbal command: high level')
            if operating_mode == 0:
                sensor_thread_execute = 1
            if foreground_feature == 'spin' and data[0] != 2:
                data[0] = data[0] + 1
            elif foreground_feature == 'serving frequency':
                data[1] = 2
                freq_changed = 1
            elif foreground_feature == 'speed' and data[2] != 3:
                data[2] += 1
            elif foreground_feature == 'launching angle' and data[4] != 2:
                data[4] = data[4] + 1
        elif command in ['medium level', 'medium levels']:
            print('The verbal command: medium level')
            LED = not LED
            if operating_mode == 0:
                sensor_thread_execute = 1
            if foreground_feature == 'spin':
                data[0] = 0
            elif foreground_feature == 'serving frequency':
                data[1] = 1
                freq_changed =1
            elif foreground_feature == 'speed':
                data[2] = 2
            elif foreground_feature == 'launching angle':
                data[4] = 0
    return data


def myf(commands):
    global k
    while True:
        if k == 10:
            break
        time.sleep(seconds+.2)
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
                user_pref = update_data(text, user_pref)
            except sr.UnknownValueError:
                pass

        if no_repeat_flag == 1:
            no_repeat_ct += 1
        if no_repeat_ct == 4:
            no_repeat_flag = 0
            no_repeat_ct = 0


def send_data(msg_list):
    msg = "{} {} {} {} {} {} {} {}".format(msg_list[0], msg_list[1], msg_list[2], msg_list[3], msg_list[4],
                                           msg_list[5], msg_list[6], msg_list[7])
    print("Message {} is sent".format(msg))
    ser.write(msg.encode('utf-8'))

myArray = ""
def read_ultrasonic_sensor():
    global ball_count
    global sensor_thread_running
    global myArray
    pulse_end = 0
    pulse_start = 0
    
    while True:
        
        x = GPIO.input(LIGHT)
        
        if x ==  1:
            myArray+="1"
            #ball_count += 1
        else:
            myArray+="0"
        
        ball_count = myArray.count("1100") 
        
        


def vibration_image():
    global vibrationFlag
    global imageFlag

    while True:
        # Listen for incoming connections (maximum of 1 connection)
        server_socket.listen(1)
        print("Waiting for a connection...")

        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)

        # Set the socket to non-blocking mode
        client_socket.setblocking(False)

        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024)

                # Check if data was received
                if data:
                    # Process the received data
                    data = data.decode('utf-8')
                    print("Received data:", data)
                    imageFlag = 1
                    imageTimer()
                    checkSync()

                else:
                    # No data received, client has disconnected
                    print("Client disconnected")
                    break
            except socket.error as e:
                # No data available to be read
                error_code = e.args[0]
                if error_code == socket.errno.EWOULDBLOCK:
                    # Handle the absence of data gracefully
                    # ...
                    pass

            # Continue with other tasks
            
            if ser_vibration.in_waiting > 0:
                vibrationFlag = 1
                vibrationTimer()
                line = ser_vibration.readline().decode('utf-8').rstrip()
                print(line)
                checkSync()

        # Close the client socket
        client_socket.close()

    # Close the server socket
    server_socket.close()


sensor_thread_execute = 0
sensor_thread_running = 0
k = 0
ball_count = 0
listener_thread = _thread.start_new_thread(listener, ())
recognition_thread = _thread.start_new_thread(myf, (frames,))
# step_thread = _thread.start_new_thread(step_motor, (0.001,))
vibration_image_thread = _thread.start_new_thread(vibration_image, ())
UI_thread = _thread.start_new_thread(user_Interface, ())
while True:
    if operating_mode == 1:
        seq_counter += 1
    if mode_changed == 1:
        random_vector = [random.randint(-2, 2), random.randint(0, 2), random.randint(1, 3), random.randint(-2, 2),
                         random.randint(-2, 2)]
        mode_changed = 0
        seq_counter = 1
    if seq_counter == 4:
        seq_counter = 0
    if operating_mode == 0 and Is_random == 0:
        if sensor_thread_running == 0:
            _thread.start_new_thread(read_ultrasonic_sensor, ())
            sensor_thread_running = 1
        if sensor_thread_execute == 1:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print("To raspberry pico: ", kubi_pico)
            print("foreground feature: ", foreground_feature)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # ball_count = random.randint(10, 20)
            # num_synch = random.randint(ball_count-7, ball_count)
            num_of_balls_thrown[kubi_pico[0] + 2] += ball_count
            num_of_balls_thrown[kubi_pico[1] + 5] += ball_count
            num_of_balls_thrown[kubi_pico[2] + 7] += ball_count
            num_of_balls_thrown[kubi_pico[3] + 13] += ball_count
            num_of_balls_thrown[kubi_pico[4] + 18] += ball_count
            num_of_balls_returned[kubi_pico[0] + 2] += num_synch
            num_of_balls_returned[kubi_pico[1] + 5] += num_synch
            num_of_balls_returned[kubi_pico[2] + 7] += num_synch
            num_of_balls_returned[kubi_pico[3] + 13] += num_synch
            num_of_balls_returned[kubi_pico[4] + 18] += num_synch
            print("ball_count = ", ball_count)
            print("num_synch = ", num_synch)
            num_synch = 0
            ball_count = 0
            try:
                print("****BURAYA GIRINCE INTERFACE'E {} YOLLUYO".format(str(num_of_balls_thrown)))
                connection.sendall(bytes("Thrown:"+str(num_of_balls_thrown), 'utf-8'))
                connection.sendall(bytes("Returned:"+str(num_of_balls_returned), 'utf-8'))
            except:
                print("Interface connection could not be found !!")
            print("returned ball number:", num_of_balls_returned)
            print("thrown ball number", num_of_balls_thrown)
            myArray=""
            sensor_thread_execute = 0
        perf_data_update()
    if User_interface_flag == 1:
        if User_interface_command[6] == 1:
            operating_mode = User_interface_command[5]
            Is_random = 1
            User_interface_flag = 0
            kubi_pico = motor_parameters(operating_mode, Is_random, user_pref, seq_counter, random_vector,
                                         kubi_pico, on_off_switch)
        else:
            Is_random = 0
            if User_interface_command[5] != 0:
                operating_mode = User_interface_command[5]
                kubi_pico = motor_parameters(operating_mode, Is_random, user_pref, seq_counter, random_vector,
                                             kubi_pico, on_off_switch)
            else:
                kubi_pico[0:5] = User_interface_command[0:5]
    else:
        kubi_pico = motor_parameters(operating_mode, Is_random, user_pref, seq_counter, random_vector,
                                     kubi_pico, on_off_switch)
    sensor_thread_execute = 0
    if operating_mode != 0:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print("To raspberry pico: ", kubi_pico)
        print("foreground feature: ", foreground_feature)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    if foreground_feature == 'launching angle':
        foreground_feature = 'launching_angle'
    elif foreground_feature == 'serving frequency':
        foreground_feature = 'serving_frequency'
    kubi_pico.append(foreground_feature)
    kubi_pico.append(LED)
    kubi_pico.append(operating_mode)
    send_data(kubi_pico)
    kubi_pico.pop()
    kubi_pico.pop()
    kubi_pico.pop()
    """
    if freq_changed == 1:
        freq_changed = 0
        if on_off_switch == 1:
            execute_step = 1
            time.sleep(0.01)
            if kubi_pico[1] == 0:
                step_thread = _thread.start_new_thread(step_motor, (0.010,))
            elif kubi_pico[1] == 1:
                step_thread = _thread.start_new_thread(step_motor, (0.005,))
            else:
                step_thread = _thread.start_new_thread(step_motor, (0.001,))
        else:
            execute_step = 1
    """
    if foreground_feature == 'launching_angle':
        foreground_feature = 'launching angle'
    elif foreground_feature == 'serving_frequency':
        foreground_feature = 'serving frequency'
    k += 1
    if k == 11:
        k = 0
        recognition_thread = _thread.start_new_thread(myf, (frames,))
    with open('Perf_Data.txt', 'w') as f:
        f.write(str(num_of_balls_thrown))
        f.write('\n')
        f.write(str(num_of_balls_returned))
        f.close()
    if operating_mode != 0:
        time.sleep(1.5*seconds)
    else:
        time.sleep(0.5*seconds)