# this module is main library
# for other modules
# or directly in terminal: 
# >>> from util.octopus import *
# >>> help()
ver = "9.7.2019"

# todo object "o"


from micropython import const
import time, os, math
from time import sleep
import machine, gc, ubinascii
from machine import Pin, PWM, SPI, Timer

from util.buzzer import beep, play_melody
from util.led import blink
from util.pinout import set_pinout
pinout = set_pinout()

from util.display_segment import *

rtc = machine.RTC() # real time
pwm0 = PWM(Pin(pinout.PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)
fet = None
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

WT = 39 # widt terminal / 39*=

menuList = [
"clt()             > clear terminal",
"printOctopus()    > print ASCII logo",
"led.value(1)      | led.value(0)",
"np[0]=(128, 0, 0) | np.write()",
"npRGBtest()",
"oledTest()",
"led7Test()",
"getTemp()",
"i2c_scann()",
"w_connect()",
"...",
"sleep(1)          > 1 s pause"
]

# -------------------------------- common terminal function ---------------
def getVer():
    return "octopus lib.ver: " + ver 

def o_help():
    printOctopus()
    print("Welcome to MicroPython on the ESP32 and octopusLAB board!")
    print("("+getVer()+")")
    printTitle("example - list commands",WT)
    for ml in menuList:
        print(ml)
  
#def npRBG((r,g,b)):
#    np[0] = ((r,g,b))
#    np.write()

def npRGBtest(): 
    np = neo_init(1)

    np[0] = (128, 0, 0) #R
    np.write()
    sleep(1)

    np[0] = (0,128, 0) #G
    np.write()
    time.sleep_ms(1)

    np[0] = (0, 0, 128) #B
    np.write()
    sleep(1)

    np[0] = (0, 0, 0) #0
    np.write()       

def i2c_scann():
    printTitle("i2c_scann() > devices:",WT)
    i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
    devices = i2c.scan()
    print(devices)    

def clt():
    print(chr(27) + "[2J") # clear terminal
    print("\x1b[2J\x1b[H") # cursor up

octopuASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   )  \ `)(' / ( ",
]

def printOctopus():
    print()
    for ol in octopuASCII:
        print(str(ol))
    print()        

def printTitle(t,num):
    print()
    print('=' * num)
    print(t.center(num))
    print('=' * num)    

def printLog(i,s):
    print()
    print('-' * 35)
    print("[--- " + str(i) + " ---] " + s)  

def printFree():
    print("Free: "+str(gc.mem_free()))    

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)      

def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)

def add0(sn):
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str

def get_hhmm(rtc):
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm

def neo_init(num_led):
    from neopixel import NeoPixel
    pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
    npObj = NeoPixel(pin, num_led)
    return npObj 

# Define function callback for connecting event
"""def connected_callback(sta):
    global WSBindIP
    blink(led, 50, 100)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    blink(led, 50, 100)
"""

def w_connect():
    led.value(1)
    from util.wifi_connect import  WiFiConnect
    sleep(1)
    w = WiFiConnect()
    if w.connect():
        print("WiFi: OK")
    else:
        print("WiFi: Connect error, check configuration")
    led.value(0)    

def octopus():
    print("this is basic library, type o_help() for help")    