# simple basic example - ESP32 + 7segment display

from time import sleep
from utils.octopus import oled_init, time_init, w, get_hhmm
from utils.display_segment import fourDigits

w()			# wifi connect
o = oled_init()

def oled_clock():
    timeString = get_hhmm()
    hh =  int(timeString[:2])
    mm =  int(timeString[3:5])
    fourDigits(o,hh,mm)
    sleep(0.5)
    fourDigits(o,hh,mm,0)
    sleep(0.5)

time_init() # server > time setup

print("oled_clock.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()
o.clear()
o.contrast(10)
o.hline(0,53,128,1)
o.text("octopusLAB 2019", 3, 1)
o.text("oled example .:.", 3, 55)
o.show()

while True:
	oled_clock()
