from util.octopus import *

d = disp7_init()   

def clock():
	disp7(d,get_hhmm("-"))
	sleep(0.5)
	disp7(d,get_hhmm(" "))        
	sleep(0.5)

while True:
	clock()
