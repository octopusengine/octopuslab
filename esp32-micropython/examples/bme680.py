from machine import Pin, I2C
import bme680i
import time

scl = Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP)
sda = Pin(21,Pin.OPEN_DRAIN, Pin.PULL_UP)

i2c = I2C(scl=scl, sda=sda, freq=400000)

bme = bme680i.BME680_I2C(i2c)

while True:
    print(bme.temperature, bme.humidity, bme.pressure, bme.gas)
    time.sleep(1)
