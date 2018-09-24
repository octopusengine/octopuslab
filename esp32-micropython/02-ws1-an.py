#octopusLAB - ESP32 - WS RGB LED (Neopixel) and analog input
#https://github.com/micropython/micropython-esp32/issues/33

import machine
from time import sleep
from machine import Pin
from neopixel import NeoPixel

BUILT_IN_LED = 2
PIN_WS = 13
PIN_AN = 35
NUM_LED = 1

pin= Pin(PIN_WS, Pin.OUT)
np = NeoPixel(pin, NUM_LED)

pin_led = Pin(BUILT_IN_LED, Pin.OUT)
pin_an = Pin(PIN_AN, Pin.IN)
adc = machine.ADC(pin_an)

def simple_blink():
    pin_led.value(0)
    sleep(1/5)
    pin_led.value(1)
    sleep(1/2)

while True:
    an = adc.read()    
    if (an<3000 and an>=2600):
      np[0] = (128, 0, 0)
      np.write()
      simple_blink() 
    
    if (an<2600 and an>=2000):
      np[0] = (0,128, 0)
      np.write()
      simple_blink() 
    
    if (an<2000):
       np[0] = (0, 0, 128)
       np.write()
       simple_blink()
 
    np[0] = (0, 0, 0)
    np.write()
    simple_blink()     