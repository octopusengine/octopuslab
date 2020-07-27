# octopusLAB simple example
# HW: ESP32 + i2c small OLED display 128x32

from time import sleep
from utils.octopus import *

octopus()            # include main library
o = oled_init(128, 32)      # init oled display
from utils.display_segment import displayDigit

def displayNum(num, row = 0):
    num = str(num)
    for n in range(len(num)):
        displayDigit(o, int(num[n]), n, row * 17)

o.clear()
for n in range(10):
    displayDigit(o, n, n)

for n in range(10):
    displayDigit(o, 9-n, n, 17)

sleep(3)
displayNum(314256987)













