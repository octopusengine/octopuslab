# octopusLAB simple example
# ESP32board with "BUILT_IN_LED" and OLED display 

import machine
from time import sleep
from util.octopus import printTitle, w, time_init, get_hhmm, get_hhmmss
isOled = False

printTitle("examples/deep_sleep1.py")

if get_hhmm() == "00:00":
    print("first time setup > ")
    w()
    time_init()

print(get_hhmmss())


def sendValue(val = 0,urlPOST = "http://youtserver/add-item-to-db.php"):
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
if isOled:
    from util.octopus import oled_init
    o = oled_init(runTest=False)
    sleep(1)
    o.clear()
    o.text("octopusLAB 2019",10,10)
    o.text(get_hhmmss(), 10,20)
    o.show()

    sleep(3)
    o.poweroff()


print('Im awake, but Im going to sleep')


#sleep for 10 seconds (20000 milliseconds)
machine.deepsleep(20000)