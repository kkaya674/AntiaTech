import machine
import utime



uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17))


def readData():
    data = uart.read()
    if data:
        print(data)
        return data
    #utime.sleep(0.01)
