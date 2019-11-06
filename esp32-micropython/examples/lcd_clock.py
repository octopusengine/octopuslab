# simple basic example - ESP32 + i2c lcd display
# cp("examples/lcd_clock.py") > main.py


from time import sleep
from util.octopus import w, lcd2_init, get_hhmm, time_init, printTitle

w()	# wifi connect
lcd = lcd2_init()	# 8 x 7segment display init   

lcd.clear()
lcd.move_to(3,0)
lcd.putstr("octopusLAB")

def clock():
    lcd.move_to(5,1)
    lcd.putstr(get_hhmm(":"))
    sleep(0.5)
    lcd.move_to(5,1)
    lcd.putstr(get_hhmm(" "))
    sleep(1)

time_init() # server > time setup

printTitle("examples/clock.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
	clock()
