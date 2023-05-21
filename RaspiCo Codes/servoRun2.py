import utime
from servo2 import Servo
 
s2 = Servo(21)       # Servo pin is connected to GP0
 
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s2.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value
   
   
