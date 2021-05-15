# simple basic example - ESP32 - Micropython - EDU_KIT1
# RTC settime / zone

from ntptime import settime
from machine import RTC
from utils.octopus_lib import w, setlocal, get_hhmm


print("--- octopusLAB: test_rtc_ntp ---")
rtc = RTC()
w(logD=False)
settime()
print(get_hhmm(rtc))

# + 1/2 h.
setlocal(1)
print(get_hhmm(rtc))
