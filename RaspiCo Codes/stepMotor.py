import machine
import utime
from machine import ADC, Pin

#DELAY = 0.004
stopPin = ADC(Pin(26))

# Define motor pins
IN1 = machine.Pin(6, machine.Pin.OUT)
IN2 = machine.Pin(7, machine.Pin.OUT)
IN3 = machine.Pin(8, machine.Pin.OUT)
IN4 = machine.Pin(9, machine.Pin.OUT)

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

"""
def speedCheck():
    file = open("servoSpeed.txt","r")
    freq = int(file.readlines()[0])
    file.close()
    if freq == 0:
        delay = 0.003
    if freq == 1:
        delay = 0.002
    if freq == 2:
        delay =0.001
   
    return delay
    
def speedWrite(speed):
    file = open("servoSpeed.txt","w")
    file.write(speed)
    file.close()
"""        


# Step motor function
def run(steps,freq,flag):
    if freq == 0:
        DELAY = 0.005
    if freq == 1:
        DELAY = 0.003
    if freq == 2:
        DELAY =0.002
   
    
    print(DELAY)
    for i in range(steps):
        if flag == 1:
            break
        for j in range(8):
            if flag == 1:
                break
            IN1.value(SEQ[j][0])
            IN2.value(SEQ[j][1])
            IN3.value(SEQ[j][2])
            IN4.value(SEQ[j][3])
            utime.sleep(DELAY)
        x = stopExecution()
        if x == True:
            break
            
            
        
           
def reverseRun(steps):
    #print("Reverse Run")
    #DELAY = speedCheck()
    k = 0
    for i in range(steps):
        for j in range(8):
            IN1.value(SEQ2[j][0])
            IN2.value(SEQ2[j][1])
            IN3.value(SEQ2[j][2])
            IN4.value(SEQ2[j][3])
            utime.sleep(DELAY)
        x = stopExecution()
        if x == True:
            break

# Test step motor

def stopExecution():
    
    x = stopPin.read_u16()
    #print(x)
    
    if x<150:
        return 1
    else:
        return 0

        
