from machine import Pin, I2C
from ds3231 import DS3231

scl = Pin(16, Pin.OPEN_DRAIN, Pin.PULL_UP)
sda = Pin(2, Pin.OPEN_DRAIN, Pin.PULL_UP)

i2c = I2C(scl=scl, sda=sda, freq=400000)

ds3231 = DS3231(i2c)

ds3231.get_time()
ds3231.get_temperature()
