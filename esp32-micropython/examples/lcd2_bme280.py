# simple basic example - ESP32 + i2c lcd display
# cp("examples/lcd2_bme280.py") > main.py


from time import sleep
from utils.octopus import w, i2c_init, lcd2_init, get_hhmm, time_init
from shell.terminal import printTitle
from bme280 import BME280

i2c = i2c_init(1)
bme280 = BME280(i2c=i2c)

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
    lcd.move_to(0,1)
    lcd.putstr("               ")
    lcd.move_to(0,1)
    lcd.putstr(bme280.values[2])
    lcd.putstr(" ")
    # lcd.putstr(bme280.values[3])
    # w()
    # temp =  int(bme280.read_compensated_data()[0]*10)/10

    # print(bme280.values)