import stepMotor
import _thread
import motorDrive

delay = 0.001
Speed = 40
spinSpeed = Speed-15
spinDir = "TOP"

def findAnalogOut(duty):
    output = duty*65000/100
    return output

def barrel():

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
    

while True:
    barrel()
    _thread.start_new_thread(reloader,())
    _thread.exit()

    
