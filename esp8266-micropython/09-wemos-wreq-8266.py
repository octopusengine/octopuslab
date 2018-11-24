"""
wemos - 8266:
This is simple usage of SSD1306 OLED display over I2C
ws rgb led
button

ampy -p /COM4 put 09-wemos-wreq-8266.py main.py
# reset device
"""
import machine
from machine import Pin, PWM
import time
from time import sleep
from neopixel import NeoPixel
import json
import urequests
from util.wifi_connect import WiFiConnect
from lib import ssd1306

wwwserver="http://octopuslab.cz/api/led3.json"

#from lib.temperature import TemperatureSensor
aa = 16
y0 = 5
y1 = 15
y2 = 25
x0 = aa+5

#import octopus_robot_board as o #octopusLab main library - "o" < octopus
BUILT_IN_LED = 2
BUTT1_PIN = 12 #d6 x gpio16=d0
PIEZZO_PIN = 14
WS_LED_PIN = 15 #wemos gpio14 = d5
ONE_WIRE_PIN = 13

I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2

i2c = machine.I2C(-1, machine.Pin(I2C_SCL_PIN), machine.Pin(I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

pwm0 = PWM(Pin(PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)

#ts = TemperatureSensor(ONE_WIRE_PIN)

def beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(200)   # set duty cycle
    time.sleep_ms(t)
    p.duty(0)
    #b.deinit()

NUMBER_LED = 1
pin = Pin(WS_LED_PIN, Pin.OUT)
butt = Pin(BUTT1_PIN, Pin.IN, Pin.PULL_UP)
np = NeoPixel(pin, NUMBER_LED)

led = Pin(BUILT_IN_LED, Pin.OUT)

def simple_blink_pause():
    led.value(0)
    sleep(1/10)
    led.value(1)
    sleep(1/5)

# ----------------------------------------------
oled.text("octopusLAB", x0, y0)
oled.text("wifi_conf", x0, y1)
oled.show()

f = open('config/wifi.json', 'r')
d = f.read()
f.close()
j = json.loads(d)
ssid=j["wifi_ssid"]

time.sleep_ms(1000)
simple_blink_pause()
oled.text("wifi_conf OK", x0, y1)
oled.show()

oled.text("wifi_conn", x0, y2)
oled.show()
w = WiFiConnect()
w.connect(ssid,j["wifi_pass"])

time.sleep_ms(1000)
simple_blink_pause()
oled.text("wifi_conn OK", x0, y2)
oled.show()

i=0
while True:
  r3 = urequests.post(wwwserver)
  j = json.loads(r3.text)
  time.sleep_ms(3000)
  rgb=j["led"]

  oled.fill(0)
  oled.text("octopusLAB", x0, y0)
  oled.text(str(i)+": "+rgb, x0, 55)
  oled.show()

  if rgb == "r": np[0] = (128, 0, 0) #R
  if rgb == "g": np[0] = (0,128, 0) #G
  if rgb == "b": np[0] = (0, 0, 128) #B
  if rgb == "0": np[0] = (0, 0, 0) #0
  if rgb == "rg": np[0] = (255,255, 0)
  if rgb == "rb": np[0] = (255,0, 255)
  if rgb == "gb": np[0] = (0,255, 255)
  np.write()
  time.sleep_ms(27000)
  i=i+1
