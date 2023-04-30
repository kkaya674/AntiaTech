import machine
import utime
from machine import ADC, Pin
import _thread
import stepMotor 



spin = [-2,-1,0,1,2]
freq = [0,1,2]
speed = [0,1,2]
dir = [-2,-1,0,1,2]
vert = [-2,-1,0,1,2]


while True:
    barrel()
    servo()
    _thread.start_new_thread(reloader,())
    _thread.exit()

    








def main(): 
    pass 


def verticalMove():
    pass 

def horizontalMove():
    pass 

def fireBall(): 
    pass 

def reloader(): 
    pass 


