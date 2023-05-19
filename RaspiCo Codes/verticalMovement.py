import machine
import utime
 
# A4988 sürücüsü için GPIO pinleri
STEP_PIN = 0 # Adım pimi
DIR_PIN = 1 # Yön pimi
ENABLE_PIN = 2 # Etkinleştirme pimi
 
# Sürücü ayarları
STEPS_PER_REV = 200 # Motor adımları
RPM = 60 # Motor devir hızı
MICROSTEPS = 16 # Mikro adımlar
 
# GPIO pinlerinin yapılandırılması
step_pin = machine.Pin(STEP_PIN, machine.Pin.OUT)
dir_pin = machine.Pin(DIR_PIN, machine.Pin.OUT)
enable_pin = machine.Pin(ENABLE_PIN, machine.Pin.OUT)
 
# Sürücü etkinleştirme
enable_pin.value(0)
 
# Motor hareket fonksiyonu
def move_motor(steps, direction):
    dir_pin.value(direction)
    for i in range(steps):
        step_pin.on()
        utime.sleep_us(500000 / RPM / MICROSTEPS)
        step_pin.off()
        utime.sleep_us(500000 / RPM / MICROSTEPS)
 
# Örnek hareket
move_motor(STEPS_PER_REV, 0) # Saat yönünde bir tur
move_motor(STEPS_PER_REV * 2, 1) # Saat yönünün tersine iki tur
 
# Sürücüyü kapatma
enable_pin.value(1)
