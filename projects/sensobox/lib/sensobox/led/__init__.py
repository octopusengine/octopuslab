# basic library for class Led 
# octopusLAB 2019
""" 
led = Led(2)
led.value(1)
"""

__version__ = "1.0.0"

from time import sleep_ms
from machine import Pin

def blink(pin, length_on=1000, length_off=1000):
    print("WARGNING: DEPRECATED: Do not USE, Use Led class instead!!")

    if length_off == 1000 and length_on != 1000:
        length_off = length_on

    pin.value(1)
    sleep_ms(length_on)
    pin.value(0)
    sleep_ms(length_off)

class Led:
    def __init__(self, pin, value=False):
        self.pin = None
        self.state = value

        if pin is None:
            print("WARN: Pin is None")
            return

        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(self.state)

    def blink(self, length_on=1000, length_off=1000):
        if length_off == 1000 and length_on != 1000:
            length_off = length_on

        self.toggle()
        sleep_ms(length_on)
        self.toggle()
        sleep_ms(length_off)

    def value(self, value=None):
        if value is None:
            if self.pin is not None:
                self.state = self.pin.value() # Update internal value in case someone changed it from outside

            return self.state

        self.state = value
        self.pin.value(self.state)

    def toggle(self):
        self.value(not self.value())
