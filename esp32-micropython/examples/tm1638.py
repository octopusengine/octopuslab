# TM1638 example

from lib.tm1638 import TM1638
from machine import Pin
from util.bits import neg, reverse, set_bit, get_bit
from time import sleep

# right OCTOBUS SCI:
# STB = MOSI 23
# CLK = MISO 19
# DIO = SCLK 18

tm = TM1638(stb=Pin(23), clk=Pin(19), dio=Pin(18))

print("TM1638 example")

tm.leds(0b01010101)
tm.show("octopus")
sleep(2)

for i in range(8):
    tm.leds(set_bit(0b00000000, i,1))
    sleep(1)
    print("keys: " + str(tm.keys()))

tm.leds(0)




