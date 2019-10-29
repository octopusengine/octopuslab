# octopusLAB example - 2019
# simple dallas thermometer and oled test

from time import sleep
from util.octopus import temp_init, disp7_init


print("init > ")
d7 = disp7_init()	# 8 x 7segment display init   
t = temp_init()

print("start > ")

while True:
    temp  = t.get_temp()
    print(temp)
    d7.show(temp)
    sleep(2)




