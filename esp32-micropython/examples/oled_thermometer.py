# octopusLAB example - 2019
# simple dallas thermometer and oled test

from time import sleep
from util.octopus import temp_init, get_temp, oled_init
from util.display_segment import threeDigits

print("init > ")
t = temp_init()
oled = oled_init()

print("start > ")

while True:
    temp  = get_temp(t[0], t[1])
    print(temp)
    temp10 = int(temp * 10)
    threeDigits(oled, temp10, True, True)
    sleep(1)
