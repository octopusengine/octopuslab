# octopusLAB simple example
# ESP32board with "BUILT_IN_LED"

import machine
from util.octopus import *

octopus()       # include main library
if get_hhmm() == "00:00":
    w()
    time_init()

printTitle("examples/deep_sleep1.py")

print(get_hhmmss())

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
#o = oled_init(128,64,False)
o = oled_init(runTest=False)
sleep(1)
o.clear()
o.text("octopusLAB 2019",10,10)
o.text(get_hhmmss(), 10,20)
o.show()

sleep(3)
o.poweroff()

print('Im awake, but Im going to sleep')

#sleep for 10 seconds (10000 milliseconds)
machine.deepsleep(20000)
