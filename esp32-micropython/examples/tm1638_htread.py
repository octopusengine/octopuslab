# TM1638_thread example

from machine import Pin
from time import sleep
from lib.tm1638 import TM1638
from util.bits import neg, reverse, set_bit, get_bit
from util.led import Led
import _thread

# right OCTOBUS SCI:
# STB = MOSI 23
# CLK = MISO 19
# DIO = SCLK 18

keys = 0
led = Led(2)
tm = TM1638(stb=Pin(23), clk=Pin(19), dio=Pin(18))

print("TM1638_thread example")

tm.leds(0b01010101)
tm.show("octopus")
sleep(1.5)

for i in range(8):
    tm.leds(set_bit(0b00000000, i,1)) # snake
    sleep(0.2)

tm.leds(0)

def readKeys():
    global keys
    while True:
        keys = tm.keys()
        sleep(0.1)

_thread.start_new_thread(readKeys, ())

while True:
    print(keys)
    led.blink()
