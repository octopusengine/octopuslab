# simple basic example - ESP32 + 7segment display
# cp("examples/clock.py") > main.py

from time import sleep
from util.octopus import w, disp7_init, get_hhmm, time_init
from shell.terminal import printTitle

w()	# wifi connect
d7 = disp7_init()	# 8 x 7segment display init   


def clock():
    d7.show(get_hhmm("-"))
    sleep(0.5)
    d7.show(get_hhmm(" "))
    sleep(0.5)

time_init() # server > time setup

printTitle("examples/clock.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
    clock()
