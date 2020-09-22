# simple basic example - ESP32 - Micropython - EDU_KIT1
# RTC settime / zone

from ntptime import settime
from machine import RTC
from utils.octopus import w, setlocal
from utils.octopus_lib import get_hhmm

rtc = RTC()
w()
settime()
print(get_hhmm(rtc))

# + 2 h.
setlocal(2)
print(get_hhmm(rtc))
