from ds3231 import DS3231
from machine import Pin, I2C

scl = Pin(16, Pin.OPEN_DRAIN, Pin.PULL_UP)
sda = Pin(2, Pin.OPEN_DRAIN, Pin.PULL_UP)

i2c = I2C(1, scl=scl, sda=sda, freq=100000)

ds3231 = DS3231(i2c)

ds3231.get_time()
ds3231.get_temperature()
