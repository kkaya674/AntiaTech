import stepMotor
import _thread
import motorDrive


def barrel():
    motorDrive.driveDC()

def reloader():
    stepMotor.run(512)
    stepMotor.reverseRun(96)
    

while True:
    barrel()    
    _thread.start_new_thread(reloader,())
    _thread.exit()
    
