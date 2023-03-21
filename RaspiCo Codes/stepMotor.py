import machine
import utime

# Define motor pins
IN1 = machine.Pin(0, machine.Pin.OUT)
IN2 = machine.Pin(1, machine.Pin.OUT)
IN3 = machine.Pin(2, machine.Pin.OUT)
IN4 = machine.Pin(3, machine.Pin.OUT)

# Define motor sequence
SEQ = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]


SEQ2 = [[0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0],
        [1,0,0,1]]
        
# Define motor speed
DELAY = 0.002

# Step motor function
def run(steps):
    k = 0
    for i in range(steps):
        for j in range(8):
            IN1.value(SEQ[j][0])
            IN2.value(SEQ[j][1])
            IN3.value(SEQ[j][2])
            IN4.value(SEQ[j][3])
            utime.sleep(DELAY)
            print(k)
            k+=1
        
           
def reverseRun(steps):
    k = 0
    for i in range(steps):
        for j in range(8):
            IN1.value(SEQ2[j][0])
            IN2.value(SEQ2[j][1])
            IN3.value(SEQ2[j][2])
            IN4.value(SEQ2[j][3])
            utime.sleep(DELAY)
            print(k)
            k+=1
# Test step motor

