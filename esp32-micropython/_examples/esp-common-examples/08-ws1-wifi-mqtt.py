#octopusLAB - ESP32 - WiFi and WS RGB LED signalizationn - MQTT
#

from time import sleep
from machine import Pin
from neopixel import NeoPixel
import machine

# Include wifi
from util.wifi_connect import read_wifi_config, WiFiConnect

from umqtt.simple import MQTTClient
import ubinascii


from util.pinout import set_pinout
pinout = set_pinout()

# Warning: RobotBoard version 1 use different WS Pin 13 !
pin_ws = Pin(13, Pin.OUT)

esp_id = ubinascii.hexlify(machine.unique_id()).decode()

# Robot Board v2 (and newer)
# pin_ws = Pin(o.WS_LED_PIN, Pin.OUT)

np = NeoPixel(pin_ws, 1)

ws_r = 0
ws_g = 0
ws_b = 0

bd = bytes.decode

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)

mqtt_clientid_prefix = ""
mqtt_host = "CHANGE_ME"
mqtt_ssl  = False # Consider to use TLS!

def simple_blink():
    pin_led.value(0)
    sleep(0.1)
    pin_led.value(1)
    sleep(0.1)


# Default WS led light RED as init
np[0] = (128, 0, 0)
np.write()
simple_blink()


# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    np[0] = (0, 128, 0)
    np.write()
    simple_blink()
    print(sta.ifconfig())


def connecting_callback(retries):
    np[0] = (0, 0, 128)
    np.write()
    simple_blink()

def mqtt_sub(topic, msg):
    global ws_r
    global ws_g
    global ws_b

    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "wsled" in topic:
        data = bd(msg)
        if data[0] == 'R':
           ws_r = int(data[1:])
        elif data[0] == 'G':
           ws_g = int(data[1:])
        elif data[0] == 'B':
           ws_b = int(data[1:])

        np[0] = (ws_r, ws_g, ws_b)
        np.write()


wifi_config = read_wifi_config()
wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else 250 )
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])


mqtt_clientid = mqtt_clientid_prefix + esp_id

c = MQTTClient(mqtt_clientid, mqtt_host)
c.set_callback(mqtt_sub)
c.connect()
c.subscribe("/octopus/device/{0}/#".format(esp_id))

while True:
    c.check_msg()
