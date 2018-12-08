import time
import urequests
import json
from machine import Pin
from util.buzzer import beep
from util.led import blink
from util.pinout import set_pinout
pinout = set_pinout()
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

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

#from util.octopus import neo_init

def neo_init(num_led):
    from neopixel import NeoPixel
    pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
    npObj = NeoPixel(pin, num_led)
    return npObj

w_connect()
np = neo_init(1)
url1="http://octopuslab.cz/api/ws.json"
#print(url1)

print("Test http request and WS RGB led controll")
while True:
      r1 = urequests.post(url1)
      j = json.loads(r1.text)
      time.sleep_ms(2000)
      print(str(j))
      np[0] = (j["r"], j["g"], j["b"]) #R
      np.write()
      time.sleep_ms(3000)
