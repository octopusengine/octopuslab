# octopusLAB simple example
# ESP32board with "BUILT_IN_LED"

import machine
from util.octopus import *

octopus()       # include main library

def sendValue(val = 0,urlPOST = "http://www.octopusengine.org/iot17/add18.php"):
    from urequests import post
    header = {}
    header["Content-Type"] = "application/x-www-form-urlencoded"
    deviceID = Env.uID
    place = "octoPy32"
    value =  int(float(Env.ver)*100)
    try:
        postdata_v = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, value,"val")
        res = post(urlPOST, data=postdata_v, headers=header)
        sleep_ms(100)
        print("sendValue.ok")
    except:
        print("E.sendValue")

print('Im ready')
led.blink()
o = oled_init()
sleep(3)
o.clear()
o.text("octopusLAB 2019",10,10)
o.show()

led.value(1)
w()
led.value(0)

sleep(5)
o.poweroff()

print('Im awake, but Im going to sleep')

#sleep for 10 seconds (10000 milliseconds)
machine.deepsleep(10000)
