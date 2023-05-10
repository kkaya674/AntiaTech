import random
from scipy.stats import rv_discrete

comm = 'repetition practicing'

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


def motor_parameters(op_mode, rand, data, counter, vec_random, last_data_pico):

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
        elif command == 'sequence practicing' or command == 'sequins practicing':
            operating_mode = 1
            mode_changed = 1
        elif command == 'gamemode' or command == 'gamo' or command == 'game mode':
            operating_mode = 2
            mode_changed = 1
        elif command == 'random':
            Is_random = 1
            mode_changed = 1
        elif command == 'regular':
            Is_random = 0
        elif command == 'serving frequency':
            foreground_feature = 'serving frequency'
        elif command == 'speed':
            foreground_feature = 'speed'
        elif command == 'launching angle':
            foreground_feature = 'launching angle'
        elif command == 'spin':
            foreground_feature = 'spin'
        elif command == 'right' and data[3] != 2:
            data[3] = data[3] + 1
        elif command == 'middle':
            data[3] = 0
        elif command == 'left' and data[3] != -2:
            data[3] = data[3] - 1
        elif command == 'low level' or command == 'no level':
            if foreground_feature == 'spin' and data[0] != -2:
                data[0] = data[0] - 1
            elif foreground_feature == 'serving frequency':
                data[1] = 0
            elif foreground_feature == 'speed':
                data[2] = 0
            elif foreground_feature == 'launching angle' and data[4] != -2:
                data[4] = data[4] - 1
        elif command == 'high level' or command == 'hi level':
            if foreground_feature == 'spin' and data[0] != 2:
                data[0] = data[0] + 1
            elif foreground_feature == 'serving frequency':
                data[1] = 2
            elif foreground_feature == 'speed':
                data[2] = 2
            elif foreground_feature == 'launching angle' and data[4] != 2:
                data[4] = data[4] + 1
        elif command == 'medium level':
            if foreground_feature == 'spin':
                data[0] = 0
            elif foreground_feature == 'serving frequency':
                data[1] = 1
            elif foreground_feature == 'speed':
                data[2] = 1
            elif foreground_feature == 'launching angle':
                data[4] = 0
    return data


while True:
    user_pref = update_data(comm, user_pref)
    if operating_mode == 1:
        seq_counter += 1
    if mode_changed == 1:
        random_vector = [random.randint(-2, 2), random.randint(0, 2), random.randint(0, 2), random.randint(-2, 2),
                         random.randint(-2, 2)]
        mode_changed = 0
        seq_counter = 1
    kubi_pico = motor_parameters(operating_mode, Is_random, user_pref, seq_counter, random_vector, kubi_pico)
    if seq_counter == 4:
        seq_counter = 0
    print(kubi_pico)
    print(foreground_feature)
    comm = input('Enter your command, my king: ')
