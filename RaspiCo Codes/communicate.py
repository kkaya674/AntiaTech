

def sendData():

    import time
    from machine import Pin, I2C

    # Define the I2C pins for the sender
    i2c_sda_pin = Pin(0)
    i2c_scl_pin = Pin(1)

    i2c = I2C(0, sda=i2c_sda_pin, scl=i2c_scl_pin, freq=100000)

    while True:
        i2c.writeto(0x12, b"Hello, Receiver!")
        time.sleep(1)




def readData():
    import time
    from machine import Pin, I2C

    # Define the I2C pins for the receiver
    i2c_sda_pin = Pin(2)
    i2c_scl_pin = Pin(3)

    i2c = I2C(0, sda=i2c_sda_pin, scl=i2c_scl_pin, freq=100000)

    while True:
        if i2c.any():
            received_data = i2c.readfrom(0x12, 16)
            print("Received Data: ", received_data.decode("utf-8"))
        time.sleep(1)


