#octopusLAB - ESP32 - WS RGB LED (Neopixel)

from time import sleep
from machine import Pin
from neopixel import NeoPixel

import WIFIconnect as WIFIC

BUILT_IN_LED = 2
PIN_WS = 13
POCET_LED = 1
pin= Pin(PIN_WS, Pin.OUT)
np = NeoPixel(pin, POCET_LED)

pin_led = Pin(BUILT_IN_LED, Pin.OUT)

def simple_blink():
    pin_led.value(0)
    sleep(1/2)
    pin_led.value(1)
    sleep(1/2)

np[0] = (128, 0, 0)
np.write()
simple_blink()

WIFIC.do_connect()

np[0] = (0,128, 0)
np.write()
simple_blink()

np[0] = (0, 0, 128)
np.write()
simple_blink()
