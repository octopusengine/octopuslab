from sensobox.display.shortcuts import display
from time import sleep_ms
from sensobox.network.shortcuts import network
import ntptime
import time

network.connect()

ntptime.settime()
while True:
    t = time.localtime(time.mktime(time.localtime()) + 2*3600)
    hours = "%02d" % (t[3],)
    minutes = "%02d" % (t[4],)
    display.show(hours+"."+minutes)
    sleep_ms(1000)

