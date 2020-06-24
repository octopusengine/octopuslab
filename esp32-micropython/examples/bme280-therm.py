# simple basic example - ESP32 - thermometer
# cp("examples/bme280-therm.py") > main.py


from time import sleep
from util.octopus import i2c_init, disp7_init
from shell.terminal import printTitle
from bme280 import BME280

def bme280_init():
    i2c = i2c_init(1)
    bme = BME280(i2c=i2c)
    print(bme.values)
    return bme

printTitle("examples/bme280-therm.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

disp7 = disp7_init()
sleep(2)

bme280 = bme280_init()

while True:
    print(bme280.values)
    disp7.show(bme280.values[0])
    sleep(1)