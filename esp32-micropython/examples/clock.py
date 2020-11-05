# simple basic example - ESP32
# upyshel& cp("examples/clock.py") > main.py

from ntptime import settime
from machine import RTC
from time import sleep
from utils.octopus_lib import w, time_init, setlocal
from shell.terminal import printTitle
from shell import clear

printTitle("examples/clock.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

rtc = RTC()

def add0(sn):
    return "0"+str(sn) if int(sn)<10 else str(sn)


def get_hhmm_sep(separator=":",rtc=rtc):
    #get_hhmm(separator) | separator = string: "-" / " "
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh + separator + mm


w()         # wifi connect
settime()   # server > time setup
setlocal(1) # 1: time zone +1h

while True:
    clear()
    print(get_hhmm_sep(":"))
    sleep(1)
    clear()
    print(get_hhmm_sep(" ")) # blinking ":"
    sleep(1)