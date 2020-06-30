# simple basic example - ESP32
# cp("examples/bme280.py") > main.py


from time import sleep
from utils.octopus import i2c_init
from shell.terminal import printTitle
from bme280 import BME280

def bme280_init():
    i2c = i2c_init(1)
    bme = BME280(i2c=i2c)
    return bme

printTitle("examples/bme280.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

bme280 = bme280_init()

while True:
    print(bme280.values)
    sleep(1)