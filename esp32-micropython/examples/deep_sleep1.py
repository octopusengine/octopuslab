# octopusLAB simple example
# ESP32board with "BUILT_IN_LED" and OLED display 

import machine
from time import sleep
from util.octopus import Env, w, time_init, get_hhmm, get_hhmmss
from shell.terminal import printTitle
isOled = False
isDisp7 = True

printTitle("examples/deep_sleep1.py")
from util.led import Led
led = Led(2)


if get_hhmm() == "00:00":
    print("first time setup > ")
    w()
    time_init()

print(get_hhmmss())


def sendValue(val = 0,urlPOST = "http://your_server/add_item_to_database.php"):
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

if isDisp7:
    try:
        from util.octopus import disp7_init
        disp7 = disp7_init()
        disp7.show(get_hhmm("-"))
        sleep(3)
        disp7.show("        ")
    except Exception as e:
        print("Exception: {0}".format(e))

if isOled:
    try:
        from util.octopus import oled_init
        oled = oled_init(runTest=False)
        sleep(1)
        oled.clear()
        oled.text("octopusLAB 2019",10,10)
        oled.text(get_hhmmss(), 10,20)
        oled.show()

        sleep(3)
        oled.poweroff()
    except Exception as e:
        print("Exception: {0}".format(e))


print('Im awake, but Im going to sleep')


#sleep for 10 seconds (20000 milliseconds)
machine.deepsleep(20000)