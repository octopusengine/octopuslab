"""
This example usage of DS18B20 "Dallas" temperature sensor, SSD1306 OLED display
and light sensor BH1750
for #hydroponics IoT monitoring system

alfa
"""
import machine
from machine import Pin, PWM, Timer
import time
import urequests
import os, ubinascii
import framebuf

from lib import ssd1306
from lib.temperature import TemperatureSensor
from lib.bh1750 import BH1750
from util.buzzer import beep
from util.led import blink
from util.display_segment import *
from assets.icons9x9 import ICON_clr, ICON_wifi
from util.pinout import set_pinout
pinout = set_pinout()

#--- setup ---
minute = 10 # 1/10 for data send
Debug = True

#tim2 = Timer(1) #
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED
if Debug: print("init dallas temp >")
ts = TemperatureSensor(pinout.ONE_WIRE_PIN)
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
if Debug: print("init i2c oled >")

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
time.sleep_ms(2000)
if Debug: print("init i2c bh >")
sbh = BH1750(i2c)

aa = 16
y0 = 9
x0 = aa+5
xb0 = 0 # display bar possition
yb0 = 58
ydown = 57

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    blink(led, 50, 100)
    # np[0] = (0, 128, 0)
    # np.write()
    blink(led, 50, 100)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    # np[0] = (0, 0, 128)
    # np.write()
    blink(led, 50, 100)

def w_connect():
    from util.wifi_connect import read_wifi_config, WiFiConnect
    time.sleep_ms(1000)
    wifi_config = read_wifi_config()
    if Debug: print("config for: " + wifi_config["wifi_ssid"])
    w = WiFiConnect()
    w.events_add_connecting(connecting_callback)
    w.events_add_connected(connected_callback)
    w.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
    if Debug: print("WiFi: OK")

def oledImage():
     IMAGE_WIDTH = 63
     IMAGE_HEIGHT = 63

     with open('assets/octopus_image.pbm', 'rb') as f:
         f.readline() # Magic number
         f.readline() # Creator comment
         f.readline() # Dimensions
         data = bytearray(f.read())
         fbuf = framebuf.FrameBuffer(data, IMAGE_WIDTH, IMAGE_HEIGHT, framebuf.MONO_HLSB)
         # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
         oled.invert(1)
         oled.blit(fbuf, 0, 0)

     oled.text("Octopus", 66,6)
     oled.text("Lab", 82,16)
     oled.text("Micro", 74,35)
     oled.text("Python", 70,45)
     oled.show()


def blinkOledPoint():
    oled.fill_rect(x0,y0,5,5,1)
    oled.show()
    time.sleep_ms(1000)

    oled.fill_rect(x0,y0,5,5,0)
    oled.show()
    time.sleep_ms(2000)

urlMain = "http://www.octopusengine.org/iot17/add19req.php?type=iot&place=pp&device="
urlPOST = "http://www.octopusengine.org/iot17/add18.php"
header = {}
header["Content-Type"] = "application/x-www-form-urlencoded"

def sendData():
    temp = ts.read_temp()
    tw = int(temp*10)
    # GET >
    #urlGET = urlMain + deviceID + "&type=temp1&value=" + str(tw)
    #print(urlGET)
    #req = urequests.post(url)

    postdata_t = "device={0}&place={1}&value={2}&type={3}".format(deviceID, "PP1", str(tw),"temp1")
    res = urequests.post(urlPOST, data=postdata_t, headers=header)

    numlux = sbh.luminance(BH1750.ONCE_HIRES_1)

    postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, "PP1", str(int(numlux)),"ligh1")
    res = urequests.post(urlPOST, data=postdata_l, headers=header)

def displMessage(mess,timm):
    oled.fill_rect(0,ydown,128,10,0)
    oled.text(mess, x0, ydown)
    oled.show()
    time.sleep_ms(timm*1000)

def displBar(by,num,timb,anim):
    oled.fill_rect(xb0,by-1,128,5+2,0) # clear
    for i in range(10):               # 0
        oled.hline(xb0+i*13,by+2,9,1)
    for i in range(num):               # 1
        oled.fill_rect(xb0+i*13,by,10,5,1)
        if anim:
           oled.show()
           time.sleep_ms(20) # animation
    oled.show()
    time.sleep_ms(timb)

def draw_icon(icon, posx, posy):
  for y, row in enumerate(icon):
    for x, c in enumerate(row):
        oled.pixel(x+posx, y+posy, c)

#-----------------------------------------------------------------------------
oledImage()
time.sleep_ms(3000)
oled.invert(0)
oled.fill(0)                # reset display

oled.text('octopusLAB', 0, 1)
if Debug: print("start - init")
deviceID = str(get_eui())
if Debug: print("> unique_id: "+ deviceID)

displMessage("init >",1)

oled.text("wifi",99, 1)
displMessage("wifi connect >",1)
for _ in range(5):
    draw_icon(ICON_clr, 88 ,0)
    oled.show()
    time.sleep_ms(100)
    draw_icon(ICON_wifi, 88 ,0)
    oled.show()
    time.sleep_ms(200)

w_connect()

it = 0
def count():
    global it
    it = it+1
    if Debug: print(">"+str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0

tim1 = Timer(0)
tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:count())

"""
tim1 = Timer(1)
tim1.init(mode=Timer.PERIODIC, period=1000)
tim.callback(timer2do)
"""
sendData() # first test sending

if Debug: print("start - loop")
displMessage("start >",1)

while True:
    numlux = sbh.luminance(BH1750.ONCE_HIRES_1)
    print(numlux)
    temp = ts.read_temp()
    tw = int(temp*10)
    print(tw/10)
    threeDigits(oled,tw,True,True)
    displBar(yb0,int(numlux/20),300,1)
    #blinkOledPoint()
    time.sleep_ms(1000)
