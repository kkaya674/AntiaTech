import stepMotor
import _thread
import motorDrive
import servoRun
import servoRun2
import utime
import communicate



"""

delay = 0.001
Speed = 60
spinSpeed = Speed-15
spinDir = "TOP"
"""

freq_changed_flag = 0


def readCommand():
    msg = communicate.readData()
    
    #msg = msg.split(" ")
    spin = msg[0]
    freq = msg[1]
    speed = msg[2]
    direction = msg[3]
    lau_angle = msg[4]
    foreGround = msg[5]
    mode = msg[6]
    return spin,freq,speed,direction,lau_angle,foreGround,mode





def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel(spinDir,speed):
    print(speed)
    ####Define Speed Parameters
    if speed =="-1":
        mainSpeed = 0
    if speed == "0":
        mainSpeed = 0
    if speed == "1":
        mainSpeed = 18
    if speed == "2":
        mainSpeed = 21
    if speed =="3":
        mainSpeed = 24

    
    ####Define Speed w.r.t Spin 
    if speed !="0":
        if spinDir == "-2":
            spinSpeed = mainSpeed -7
        if spinDir == "-1":
            spinSpeed = mainSpeed -3
        if spinDir == "0":
            spinSpeed = mainSpeed
        if spinDir == "1":
            spinSpeed = mainSpeed
            mainSpeed = spinSpeed-3
        if spinDir == "2":
            spinSpeed = mainSpeed
            mainSpeed = spinSpeed -7
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
        #stepMotor.reverseRun(32)

        
        
        
        

def servo1(direction):
    print("now servo1")
    mostLeft = 75
    inc = 3
    if direction == "2":
        servoRun.servo_Angle(mostLeft)
    if direction == "1":
        servoRun.servo_Angle(mostLeft+inc)
    if direction == "0":
        servoRun.servo_Angle(mostLeft+inc*2)
    if direction == "-1":
        servoRun.servo_Angle(mostLeft+inc*3)
    if direction == "-2":
        servoRun.servo_Angle(mostLeft+inc*4)
        
    
def servo2(lau):
    print("now servo2")
    bottom = 120
    inc = 2
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

k=0
prev_freq ="1"
_thread.start_new_thread(reloader,(1, ))
while True:
    spin,freq,speed,direction,lau_angle,foreGround,mode = readCommand() ##datayi aliyor
    print("{} {} {} {} {} {} mode : {}".format(spin,freq,speed,direction,lau_angle,foreGround,mode))
    barrel(spin,speed) ##namlu spin ve speed bilgisini gönderek motor parametrelerini degistiriyor
    #stepMotor.speedWrite(freq) ##stepMotor ayri threadda sonsuz döngüde calistigi icin hiz degisimi file write-read metodu ile yapilacak
    servo1(direction)
    servo2(lau_angle)
    if freq != prev_freq:
        freq_changed_flag = 1
        utime.sleep(2)
        _thread.start_new_thread(reloader,(int(freq),))
        prev_freq = freq
        freq_changed_flag=0
    prev_freq = freq
    k+=1

    utime.sleep(0.5)
"""
k=0
freq="1"
prev_freq ="1"
#_thread.start_new_thread(reloader,(1, ))

k = 0
while True:
    
    barrel("0","3")
    
    #servoRun.servo_Angle(100)
    servo1("0")
    servo2("2")
    if freq != prev_freq:
        freq_changed_flag = 1
        utime.sleep(2)
        #_thread.start_new_thread(reloader,(int("2"),))
        prev_freq = freq
        freq_changed_flag=0
    prev_freq = freq
    
    k+=1

    utime.sleep(2)
"""
    
    
    
    
    