from machine import Pin, PWM,ADC
import utime



en1 = PWM(Pin(15))
while True:
    en1.duty_u16(65000)