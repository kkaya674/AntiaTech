from machine import Pin, PWM,ADC
import utime

m1 = Pin(5, Pin.OUT)
m2 = Pin(4, Pin.OUT)
m3 = Pin(6,Pin.OUT)
m4 = Pin(7,Pin.OUT)




def driveDC():

    maxNum = 65535
    m1 = Pin(5, Pin.OUT)
    m2 = Pin(4, Pin.OUT)

    en1 = PWM(Pin(6))
    opto = ADC(Pin(28))

    while True:
        en1.duty_u16(0)  # motor 1 disable

        # Both motors in forward direction
        m1.value(1)
        m2.value(0)
        duty = opto.read_u16()
        if duty == maxNum:
            duty = duty-1000
        print("Duty : " +str(duty))
        en1.duty_u16(duty)  # motor 1 enable at 50% duty cycle
        utime.sleep(5)

        # Measure the voltage across the opto-sensor
        voltage = opto.read_u16() / 65535 * 3.3
        
        print("Voltage : " + str(voltage))
        

        # Convert the voltage to RPM
        

        en1.duty_u16(0)  # motor 1 disable
        utime.sleep(1)
        
        
        
        
driveDC()