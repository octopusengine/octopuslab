"""
octopusLAB - ESP32 - WS RGB LED (Neopixel)
This is simple usage of ws2812 - single RGB led diode

Installation:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
ampy -p /dev/ttyUSB0 put ./02-ws1.py main.py
# reset device
"""

from time import sleep
from machine import Pin
from neopixel import NeoPixel

import octopus_robot_board as o #octopusLab main library - "o" < octopus

NUMBER_LED = 1
pin = Pin(o.WS_LED_PIN, Pin.OUT)
np = NeoPixel(pin, NUMBER_LED)

led = Pin(o.BUILT_IN_LED, Pin.OUT)

def simple_blink_pause():
    led.value(0)
    sleep(1/2)
    led.value(1)
    sleep(1/2)

while True: #RGB test loop
    np[0] = (128, 0, 0) #R
    np.write()
    simple_blink_pause()

    np[0] = (0,128, 0) #G
    np.write()
    simple_blink_pause()

    np[0] = (0, 0, 128) #B
    np.write()
    simple_blink_pause()
