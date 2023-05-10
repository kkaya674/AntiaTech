from sys import stdin
from machine import Pin
import _thread, uselect
from time import sleep

led = Pin("LED", Pin.OUT)
led.toggle()

while True:
    buffer = []
    select_result = uselect.select([stdin], [], [], 0)
    while select_result[0]:
        char = stdin.read(1)
        buffer.append(char)
        select_result = uselect.select([stdin], [], [], 0)
    
    message = "".join(buffer) if buffer != [] else None
    if message != None:
        with open("in.txt", "w") as f:
            led.toggle()
            print(message)
            f.write(message)
            return message
