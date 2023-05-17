from machine import Pin, PWM,ADC
import utime

m1 = Pin(5, Pin.OUT)
m2 = Pin(4, Pin.OUT)##alt motor
m3 = Pin(7,Pin.OUT)
m4 = Pin(8,Pin.OUT)##üst motor
maxNum = 65535
en1 = PWM(Pin(6))
en2 = PWM(Pin(9))



def driveDC(speed1,speed2):

    en1.duty_u16(0)  # motor 1 disable
    en2.duty_u16(0)

    # Both motors in forward direction
    m1.value(1)
    m2.value(0)
    m3.value(1)
    m4.value(0)

#25000 sayilari duty cycle parametresidir. Cycle = sayi/65535"
    en1.duty_u16(int(speed1))  # motor 1 enable at 50% duty cycle
    en2.duty_u16(int(speed2))

    
        
#driveDC()