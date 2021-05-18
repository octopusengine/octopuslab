from machine import Pin, I2C
from time import sleep

i2c = I2C(scl=Pin(16, Pin.IN, Pin.PULL_UP), sda=Pin(2, Pin.IN, Pin.PULL_UP), freq=100000)

read = i2c.readfrom_mem(84, 0, 10, addrsize=16)

for addr in range(1, 256):
    b = bytearray(32)
    b[0] = 4
    b[1] = 5
    b[2] = 6
    i2c.writeto_mem(84, addr*32, b, addrsize=16)
    sleep(0.01)
    read = i2c.readfrom_mem(84, 0, 3, addrsize=16)
    print("addr 0: {}".format(read))
    sleep(0.01)
    read = i2c.readfrom_mem(84, addr*32, 3, addrsize=16)
    print("addr {}: {}".format(addr*32,read))
