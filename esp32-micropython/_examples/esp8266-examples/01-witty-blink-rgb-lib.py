"""
This is first basic test ESP8266 Witty module programming
blink with RGB BUILT_IN_LED
"""
from time import sleep
from machine import Pin

from util.pinout import set_pinout
pinout = set_pinout()

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)
pin_ledR = Pin(pinout.LED_RED, Pin.OUT)
pin_ledG = Pin(pinout.LED_GRE, Pin.OUT)
pin_ledB = Pin(pinout.LED_BLU, Pin.OUT)


print("simple demo:")
# esp_id = ubinascii.hexlify(machine.unique_id()).decode()                 
# print(esp_id)

def simple_blinkRGB():
    pin_led.value(0)
    sleep(0.5)
    pin_led.value(1)
    sleep(0.5)
    

def simple_blink():
    pin_ledR.value(1)
    sleep(0.5)
    pin_ledR.value(0)
    sleep(0.1)

    pin_ledG.value(1)
    sleep(0.5)
    pin_ledG.value(0)
    sleep(0.1)

    pin_ledB.value(1)
    sleep(0.5)
    pin_ledB.value(0)
    sleep(0.1)


print("blinking led / RGB")
while True:
    simple_blink()
    simple_blinkRGB()
