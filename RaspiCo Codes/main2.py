import utime
import stepMotor
import servoRun
import _thread
import motorDrive
import communicate

##reloader için DELAY degisir
##spinDir

def readCommand():
    data = communicate.readData()
    
    ##codeHere
    
    return command
    
    

def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel(Speed):
    
    print("NOW Barrel")
    if spinDir == 2:
        spinSpeed = Speed-20
        motorDrive.driveDC(findAnalogOut(Speed),findAnalogOut(spinSpeed))
    if spinDir == 1:
        spinSpeed = Speed-10
        motorDrive.driveDC(findAnalogOut(Speed),findAnalogOut(spinSpeed))
    if spinDir == 0:
        spinSpeed = Speed
        motorDrive.driveDC(findAnalogOut(Speed),findAnalogOut(spinSpeed))
    if spinDir == -1:
        spinSpeed = Speed-10
        motorDrive.driveDC(findAnalogOut(spinSpeed),findAnalogOut(Speed))
    if spinDir == -2:
        spinSpeed = Speed-20
        motorDrive.driveDC(findAnalogOut(spinSpeed),findAnalogOut(Speed))
 

def reloader(DELAY):
    while True:
        print("NOW Reloader")
        stepMotor.run(512)
        stepMotor.reverseRun(32)
        x = stepMotor.stopExecution()
        if x == True:
            break
    
def servo():
    
    for i in range(0,90,10):
        servoRun.servo_Angle(i)
        utime.sleep(0.05)

_thread.start_new_thread(reloader,()) ##reloader thread'ini tetikler. Durdurmak icin 26. pini groundla
while True:
    
    barrel(Speed = 55) ##motor surucu 
    servo()
    
    

    


