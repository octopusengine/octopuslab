# basic library for 8bit expander
# octopusLAB 2019 / FIRSTboard with PCF8574
# from util.expander8 import Expander8
# e8 = Expander8(addr) addr default 000 > 0x20
# e8.test()

from time import sleep_ms
from micropython import const
from util.pinout import set_pinout
from util.bits import neg, reverse, set_bit, get_bit
from machine import Pin, I2C

pinout = set_pinout() 
#PCF addr = 35 #33-0x21/35-0x23
ADDRESS = 0x20 #0x20(000) 0x23(100)

i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)
# 100kHz as Expander is slow

tempByte = bytearray(1)

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


class Expander8:
    def __init__(self, addr=ADDRESS):
        self.addr = addr
        self.i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) 

    def write(self, data):
        self.i2c.writeto(self.addr, data)

    def write_8bit(self, dataInt): # (int) or 0b101010100
        # ...write(struct.pack('<B', 255)) # alternative
        tempByte[0] = dataInt
        self.i2c.writeto(self.addr, tempByte)

    def write_bar(self, dataInt): # 1-8
        self.i2c.writeto(self.addr, bytearray([bar[dataInt]]))

    def set_all(self, all_0):
        if all_0:
            self.i2c.writeto(self.addr, bytearray([bar[0]]))
        else:
            self.i2c.writeto(self.addr, bytearray([bar[8]]))

    def read(self):
        bR = self.i2c.readfrom(self.addr, 1)[0]
        return(bR)        

    def pin_read(self, pinNum):
        mask = 0x1 << pinNum
        pinVal = self.i2c.readfrom(self.addr, 1)[0]

        pinVal &= mask
        if (pinVal == mask):
            return 1
        else:
            return 0

    def test(self):
        for dd in range(9):
            self.i2c.writeto(self.addr, bytearray([bar[dd]]))
            sleep_ms(200)

        for dd in range(9):
            self.i2c.writeto(self.addr, bytearray([neg(bar[dd])]))
            sleep_ms(200)

    def counter(self, delay = 100):
        for i in range(255):
            self.write(255-i)
            sleep_ms(delay)
            

class Expander16:
    def __init__(self, addr = ADDRESS):
        self.addr = addr
        self.i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) 

    def write(self, data):
        self.i2c.writeto(self.addr, data)
