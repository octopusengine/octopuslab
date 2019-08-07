# simple basic example - ESP32 + 7segment display

from util.octopus import *

w()			# wifi connect
d7 = disp7_init()	# 8 x 7segment display init   

def clock():
	d7.show(get_hhmm("-"))
	sleep(0.5)
	d7.show(get_hhmm(" "))        
	sleep(0.5)

time_init() 		# server > time setup

printTitle("clock.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
	clock()
