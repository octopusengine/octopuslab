# basic library for 8bit expander
# octopusLAB 2019 / FIRSTboard with PCF8574
# from util.expander8 import Exp8
# e8 = Exp8(addr) addr default 000 > 0x20
# e8.test()

from time import sleep_ms
from micropython import const
from util.pinout import set_pinout
from machine import Pin, I2C

pinout = set_pinout() 
#PCF address = 35 #33-0x21/35-0x23
ADDRESS = 0x20 #0x20(000) 0x23(100)

i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)
# 100kHz as Expander is slow

bar = (
const(0b00000000), #0
const(0b10000000), #1
const(0b11000000), #2
const(0b11100000), #3
const(0b11110000), #4
const(0b11111000), #5
const(0b11111100), #6
const(0b11111110), #7
const(0b11111111)  #8
)

all0 = const(0b00000000)
all1 = const(0b11111111)

def neg(bb):
    return(bb ^ 0xff)

class Exp8:
    def __init__(self, addr = ADDRESS):
        self.addr = addr
        self.i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) 

    def write(self, dataByte):
        self.i2c.writeto(self.addr, bytearray(dataByte))

    def set_all(self, all_0):
        if all_0:
            self.i2c.writeto(self.addr, bytearray([bar[0]]))
        else:
            self.i2c.writeto(self.addr, bytearray([bar[8]]))

    def read(self):
        byteB = 0b01010101
        return(byteB)

    def test(self):
        for dd in range(9):
            self.i2c.writeto(self.addr, bytearray([bar[dd]]))
            sleep_ms(200)

        for dd in range(9):
            self.i2c.writeto(self.addr, bytearray([neg(bar[dd])]))
            sleep_ms(200)