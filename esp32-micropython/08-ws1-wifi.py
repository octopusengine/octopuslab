#octopusLAB - ESP32 - WS RGB LED (Neopixel)

from time import sleep
from machine import Pin
from neopixel import NeoPixel

# Include wifi
from WIFIconnect import WiFiConnect

# Remember set SSID and password in WiFiConfig.py file
import WiFiConfig

# Import OctopusLab Robot board definition file
import octopus_robot_board as o # octopusLab main library - "o" < octopus

# Warning: RobotBoard version 1 use different WS Pin 13 !
pin_ws = Pin(13, Pin.OUT)

# Robot Board v2 (and newer)
# pin_ws = Pin(o.WS_LED_PIN, Pin.OUT)

np = NeoPixel(pin_ws, 1)

pin_led = Pin(o.BUILT_IN_LED, Pin.OUT)


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


def connecting_callback():
    np[0] = (0, 0, 128)
    np.write()
    simple_blink()


w = WiFiConnect()
w.events_add_connecting(connecting_callback)
w.events_add_connected(connected_callback)

w.connect(WiFiConfig.WIFI_SSID, WiFiConfig.WIFI_PASS)
