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




def readCommand():
    msg = communicate.readData()
    
    #msg = msg.split(" ")
    spin = msg[0]
    freq = msg[1]
    speed = msg[2]
    direction = msg[3]
    lau_angle = msg[4]
    mode = msg[5]
    return spin,freq,speed,direction,lau_angle,mode





def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel(spinDir,speed):
    print(speed)
    ####Define Speed Parameters
    if speed =="-1":
        mainSpeed = 0
    if speed == "0":
        mainSpeed = 20
    if speed == "1":
        mainSpeed = 20
    if speed == "2":
        mainSpeed = 25
    if speed ==  "5":
        mainSpeed = 40
    
    ####Define Speed w.r.t Spin 
    if speed !="-1":
        if spinDir == "-2":
            spinSpeed = mainSpeed -10
        if spinDir == "-1":
            spinSpeed = mainSpeed -5
        if spinDir == "0":
            spinSpeed = mainSpeed
        if spinDir == "1":
            spinSpeed = mainSpeed
            mainSpeed = spinSpeed-5
        if spinDir == "2":
            spinSpeed = mainSpeed
            mainSpeed = spinSpeed -10
    if speed == "-1" or speed =="0":
        spinSpeed = 0
        mainSpeed = 0
    motorDrive.driveDC(findAnalogOut(mainSpeed),findAnalogOut(spinSpeed))

        
        
        
        
        
        

def reloader():
    utime.sleep(3)
    while True:
        print("NOW Reloader")
        stepMotor.run(512)
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
    bottom = 100
    inc = 7
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
"""
_thread.start_new_thread(reloader,())
while True:
    spin,freq,speed,direction,lau_angle,mode = readCommand() ##datayi aliyor
    print("{} {} {} {} {} {}".format(spin,freq,speed,direction,lau_angle,mode))
    barrel(spin,speed) ##namlu spin ve speed bilgisini gönderek motor parametrelerini degistiriyor
    stepMotor.speedWrite(freq) ##stepMotor ayri threadda sonsuz döngüde calistigi icin hiz degisimi file write-read metodu ile yapilacak
    servo1(direction)
    servo2(lau_angle)
    k+=1
    if k%10== 0:
        barrel("0","5")
    utime.sleep(2)"""
    


_thread.start_new_thread(reloader,())
k = 0
while True:
    
    barrel("0","0")
    
    #servoRun.servo_Angle(100)
    servo1("2")
    #servo2("2")
    k+=1
    if k%10== 0:
        barrel("0","5")
    utime.sleep(1)
    
    
    
    
    
    
    