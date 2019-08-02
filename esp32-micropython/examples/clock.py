# simple basic example - ESP32 + 7segment display

from util.octopus import *

w()			# wifi connect
d = disp7_init()	# 8 x 7segment display init   

def clock():
	disp7(d,get_hhmm("-"))
	sleep(0.5)
	disp7(d,get_hhmm(" "))        
	sleep(0.5)

timeSetup() 		# server > time setup

while True:
	clock()
