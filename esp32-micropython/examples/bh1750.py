# MicroPython BH1750 example

from time import sleep
from lib.bh1750 import BH1750
from util.octopus import i2c_init

i2c = i2c_init()
sbh = BH1750(i2c)

while True:
   light = int(sbh.luminance(BH1750.ONCE_HIRES_1))
   print(light)
   sleep(1)


