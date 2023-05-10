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



def processData():
    data = communicate.readData()

    return data






def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel(spin,speed):
    print("NOW Barrel")
    if spinDir == "TOP":
        motorDrive.driveDC(findAnalogOut(Speed),findAnalogOut(spinSpeed))
    else:
        motorDrive.driveDC(findAnalogOut(spinSpeed),findAnalogOut(Speed))

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
        
def servo3(): ##rana code, horizontal
    servoRun.servo_Angle(80)
    
def servo4(): ##basak code, vertical
    servoRun2.servo_Angle(120)
    

#_thread.start_new_thread(reloader,())
"""while True:
    
    #barrel()
    #servo1()
    #servo2()
    #servo3()
    #servo4()
    """
while True:
    communicate.sendData("dme")
    