# simple basic example - ESP32 + 7segment display

from time import sleep
from util.octopus import disp7_init

print("this is simple Micropython example | ESP32 & octopusLAB")
print()

d7 = disp7_init()	# 8 x 7segment display init

for i in range(999):
    d7.show(1000-i)
    sleep(1)
