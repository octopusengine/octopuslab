# octopusLAB example - 2019
# simple example: dallas thermometer and oled display

from time import sleep
from util.octopus import oled_init
from util.iot import Thermometer
from util.display_segment import threeDigits


print("init > ")

ts = Thermometer()
oled = oled_init()

print("start > ")

while True:
    temp  = ts.get_temp()
    print(temp)
    temp10 = int(temp * 10)
    threeDigits(oled, temp10, True, True)
    sleep(1)
