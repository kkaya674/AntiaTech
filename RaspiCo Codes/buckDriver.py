import machine
import time

pwmOut = machine.Pin(2)
pwm1 = machine.PWM(pwmOut)
pwm1.freq(2000)
maxNum = 65535
voltagePin = machine.ADC(26)



def convert16Bit(yuzde):
    result = yuzde*maxNum/100
    return result

def readVoltage():
    voltageData = voltagePin.read_u16()
    print("voltage Data  = " +str(voltageData))
    voltage = voltageData*3.3/maxNum
    return voltage


def buckConverterPWM():
    while True:
        voltage = readVoltage()
        print(voltage)
        x = voltage*100/3.3
        print("x = " +str(x))
        duty = convert16Bit(x)
        print(duty)
        pwm1.duty_u16(int(duty))
        time.sleep(1)
        
buckConverterPWM()

        
    
    
    
