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
    spin = msg[0]
    freq = msg[1]
    speed = msg[2]
    direction = msg[3]
    lau_angle = msg[4]
    return spin,freq,speed,direction,lau_angle





def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel(spinDir,speed):
    ####Define Speed Parameters
    if speed == "0":
        mainSpeed = 35
    if speed == "1":
        mainSpeed = 45
    if speed == "2":
        mainSpeed = 55
    
    ####Define Speed w.r.t Spin 
    
    if spinDir == "-2":
        spinSpeed = mainSpeed -20
    if spinDir == "-1":
        spinSpeed = mainSpeed -10
    if spinDir == "0":
        spinSpeed = mainSpeed
    if spinDir == "1":
        spinSpeed = mainSpeed
        mainSpeed = spinSpeed-10
    if spinDir == "2":
        spinSpeed = mainSpeed
        mainSpeed = spinSpeed -20
    
    
    print(mainSpeed, spinSpeed)
    motorDrive.driveDC(findAnalogOut(mainSpeed),findAnalogOut(spinSpeed))

        
        
        
        
        
        

def reloader():
    while True:
        print("NOW Reloader")
        stepMotor.run(512)
        stepMotor.reverseRun(32)
        x = stepMotor.stopExecution()
        if x == True:
            break
        
        
        
        

def servo1():
    for i in range(80,100,5):
        servoRun.servo_Angle(i)
        utime.sleep(0.2)
        
        
        
        
    
def servo2():
    for i in range(130,110,-5):
        print(i)
        servoRun2.servo_Angle(i)
        utime.sleep(1)


#_thread.start_new_thread(reloader,())
while True:
    spin,freq,speed,direction,lau_angle = readCommand() ##datayi aliyor 
    barrel(spin,speed) ##namlu spin ve speed bilgisini gönderek motor parametrelerini degistiriyor
    stepMotor.speedWrite(freq) ##stepMotor ayri threadda sonsuz döngüde calistigi icin hiz degisimi file write-read metodu ile yapilacak
    
    
    
    
    
    
    