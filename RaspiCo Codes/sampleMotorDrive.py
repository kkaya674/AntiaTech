import machine
import time

# define analog pin for voltage reading
voltage_pin = machine.ADC(26)

# define pins for motor driver control
motor_enable_pin = machine.Pin(0, machine.Pin.OUT)
motor_direction_pin = machine.Pin(1, machine.Pin.OUT)

# set motor driver enable pin to high
motor_enable_pin.value(1)

# define function to control motor speed and direction
def set_motor_speed(speed):
    # set motor direction pin based on speed
    if speed >= 0:
        motor_direction_pin.value(1)
    else:
        motor_direction_pin.value(0)
    # set motor speed using PWM
    motor_pwm = machine.PWM(machine.Pin(2))
    motor_pwm.freq(1000)
    motor_pwm.duty_u16(abs(speed))

# main loop to read voltage and control motor
while True:
    # read voltage data from analog pin
    voltage_data = voltage_pin.read_u16()
    voltage = voltage_data * 3.3 / 65535
    print("Voltage:", voltage)

    # control motor based on voltage data
    if voltage >= 2.0:
        set_motor_speed(50000) # set motor speed to maximum
    elif voltage >= 1.0:
        set_motor_speed(20000) # set motor speed to medium
    else:
        set_motor_speed(0) # stop motor
    time.sleep(0.1)

