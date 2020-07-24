# octopusLAB example - 2019
# simple example: dallas thermometer and 8x7 segment display (disp7)

from time import sleep
from utils.octopus import disp7_init
from components.iot import Thermometer


print("init > ")
d7 = disp7_init()
ts = Thermometer()

print("start > ")

while True:
    temp  = ts.get_temp()
    print(temp)
    d7.show(temp)
    sleep(2)
