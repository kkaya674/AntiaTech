import stepMotor
import _thread
import motorDrive
import servoRun
import servoRun2
import utime
import communicate
from machine import Pin
import lcdCode
import time


"""

delay = 0.001
Speed = 60
spinSpeed = Speed-15
spinDir = "TOP"
"""

m1 = Pin(18, Pin.IN, Pin.PULL_DOWN)
x = ""
time1 = time.time()
utime.sleep(1)
oldCount = 0

freq_changed_flag = 0

def ledToggle(value):
    if value == "True":
        led = 1
    else:
        led = 0
    m1 = machine.Pin(0,pin.OUT)
    m2 = machine.Pin(1, Pin.OUT)
    m1.value(0)
    m2.value(led)

    

def readCommand():
    msg = communicate.readData()
    
    #msg = msg.split(" ")
    spin = msg[0]
    freq = msg[1]
    speed = msg[2]
    direction = msg[3]
    lau_angle = msg[4]
    foreGround = msg[5]
    mode = msg[7]
    led= msg[6]
    return spin,freq,speed,direction,lau_angle,foreGround,mode,led





def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel(spinDir,speed):
    
    ####Define Speed Parameters
    if speed =="-1":
        mainSpeed = 0
    if speed == "0":
        mainSpeed = 0
    if speed == "1":
        mainSpeed = 80
    if speed == "2":
        mainSpeed = 90
    if speed =="3":
        mainSpeed = 100

    
    ####Define Speed w.r.t Spin 
    if speed !="0":
        if spinDir == "-2":
            spinSpeed = mainSpeed -30
        if spinDir == "-1":
            spinSpeed = mainSpeed -15
        if spinDir == "0":
            spinSpeed = mainSpeed
        if spinDir == "1":
            spinSpeed = mainSpeed
            mainSpeed = spinSpeed-15
        if spinDir == "2":
            spinSpeed = mainSpeed
            mainSpeed = spinSpeed -30
    if speed == "-1" or speed =="0":
        spinSpeed = 0
        mainSpeed = 0
    motorDrive.driveDC(findAnalogOut(mainSpeed),findAnalogOut(spinSpeed))

        
        
        
        
        
        

def reloader(level):
    global freq_changed_flag
    while True:
        if freq_changed_flag == 1:
            break
        stepMotor.run(52, level,freq_changed_flag)
        #stepMotor.reverseRun(20,level,freq_changed_flag)
        
        #stepMotor.reverseRun(32)

        
        
        
        

def servo1(direction):
  
    mostLeft = 125
    inc = 6
    if direction == "-2":
        servoRun.servo_Angle(mostLeft-2*inc)
    if direction == "-1":
        servoRun.servo_Angle(mostLeft-inc)
    if direction == "0":
        servoRun.servo_Angle(mostLeft)
    if direction == "1":
        servoRun.servo_Angle(mostLeft+inc)
    if direction == "2":
        servoRun.servo_Angle(mostLeft+inc*2)
        
    
def servo2(lau):
 
    bottom = 115
    inc = 3
    if lau == "-2":
        servoRun2.servo_Angle(bottom)
    if lau == "-1":
        servoRun2.servo_Angle(bottom+inc)
        
    if lau == "0":
        servoRun2.servo_Angle(bottom+2*inc)
        
    if lau == "1":
        servoRun2.servo_Angle(bottom+3*inc)
        
    if lau == "2":
        servoRun2.servo_Angle(bottom+4*inc)
print("start")
"""
k=0
prev_freq ="1"
led = 0
while True:
    
    spin,freq,speed,direction,lau_angle,foreGround,mode,led = readCommand() ##datayi aliyor
    ledToggle(led)
    barrel(spin,speed) ##namlu spin ve speed bilgisini gönderek motor parametrelerini degistiriyor
    servo1(direction)
    servo2(lau_angle)
    lcdCode.writeStr("Mode:{}".format(mode),"Speed:{}".format(speed))




"""


k = 1

while True:
        
    barrel("0","0")
    servo1("0")
    servo2("0")
    lcdCode.writeStr("deneme","rana")
    x=x+str(m1.value())
    print(x)
    print(x.count("1"))
    time2 = time.time()
    if not((time2-time1) % 10):
        rpmSpeed = x.count("1")*6
        x = ""
        print("RPM :{}".format(rpmSpeed))
        utime.sleep(1)
