# sender.py
import time
import serial




ser = serial.Serial(
  port='/dev/ttyACM0', # Change this according to connection methods, e.g. /dev/ttyUSB0
  baudrate = 115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

def sendData(msg_list)
    msg = "{}{}{}{}{}".format(msg_list[0],msg_list[1],msg_list[2],msg_list[3],msg_list[4])
    print("Message {} is sent".format(msg))
    ser.write(msg.encode('utf-8'))
    time.sleep(2)



