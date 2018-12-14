"""
This example usage of DS18B20 "Dallas" temperature sensor and SSD1306 OLED display

"""
import machine
from machine import Pin, PWM, Timer
import time
import urequests
import os, ubinascii

from lib import ssd1306
from lib.temperature import TemperatureSensor
from util.buzzer import beep
from util.led import blink
from util.pinout import set_pinout
pinout = set_pinout()

#--- setup ---
minute = 10 # 1/10 for data send



#tim2 = Timer(1) #
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED
ts = TemperatureSensor(pinout.ONE_WIRE_PIN)
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

aa = 16
y0 = 5
x0 = aa+5

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
    print("config for: " + wifi_config["wifi_ssid"])
    w = WiFiConnect()
    w.events_add_connecting(connecting_callback)
    w.events_add_connected(connected_callback)
    w.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
    print("WiFi: OK")

sevenSeg = [      #seven segment display
#0,1,2,3,4,5,6
 [1,1,1,1,1,1,0], #0      +----0----+
 [0,1,1,0,0,0,0], #1      |         |
 [1,1,0,1,1,0,1], #2      5         1
 [1,1,1,1,0,0,1], #3      |         |
 [0,1,1,0,0,1,1], #4      +----6----+
 [1,0,1,1,0,1,1], #5      |         |
 [1,0,1,1,1,1,1], #6      4         2
 [1,1,1,0,0,0,0], #7      |         |
 [1,1,1,1,1,1,1], #8      +----3----+
 [1,1,1,1,0,1,1], #9
 [1,1,0,0,0,1,1], #deg
 [0,0,0,0,0,0,1]  #-
]

def oneDigit(seg,x,y,a): #segment /x,y position / a=size
    oled.hline(x,y,a,seg[0])
    oled.vline(x+a,y,a,seg[1])
    oled.vline(x+a,y+a,a,seg[2])
    oled.hline(x,y+a+a,a,seg[3])
    oled.vline(x,y+a,a,seg[4])
    oled.vline(x,y,a,seg[5])
    oled.hline(x,y+a,a,seg[6])

def threeDigits(d,point,deg): #display number 0-999 / point 99.9 / degrees
    d100=int(d/100)
    d10=int((d-d100*100)/10)
    d1= d-d100*100-d10*10
    oneDigit(sevenSeg[d100],x0,y0,aa)
    oneDigit(sevenSeg[d10],x0+aa+int(aa/2),y0,aa)
    oneDigit(sevenSeg[d1],x0+(aa+int(aa/2))*2,y0,aa)
    if point:
       oled.fill_rect(x0+(aa+int(aa/2))*2-5,y0+aa+aa,2,3,1) #test poin
    if deg:
       oneDigit(sevenSeg[10],x0+(aa+int(aa/2))*3,y0,aa) #test deg
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

    postdata = "device={0}&place={1}&value={2}&type={3}".format(deviceID, "PP1", str(tw),"temp1")
    res = urequests.post(urlPOST, data=postdata, headers=header)

#-----------------------------------------------------------------------------
print("start - init")

deviceID = str(get_eui())
print("> unique_id: "+ deviceID)

w_connect()
"""
url1="http://octopuslab.cz/api/ws.json"
r1 = urequests.post(url1)
print(r1.text)
# j = json.loads(r1.text)
"""

it = 0
def count():
    global it
    it = it+1
    print(">"+str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0

tim1 = Timer(0)
tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:count())

"""
tim1 = Timer(1)
tim1.init(mode=Timer.PERIODIC, period=1000)
tim.callback(timer2do)
"""

# test_whole display
oled.fill(1)
oled.show()
time.sleep_ms(300)

oled.fill(0) # reset display
oled.show()

sendData() # first test sending

print("start - loop")
while True:
    oled.text('OctopusLab', x0, 57)

    temp = ts.read_temp()
    tw = int(temp*10)
    print(tw/10)
    threeDigits(tw,True,True)
    oled.show()

    blinkOledPoint()
