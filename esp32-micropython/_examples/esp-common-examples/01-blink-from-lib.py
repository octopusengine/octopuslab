"""
This is first basic test ESP8266/32 programming
blink with BUILT_IN_LED
"""
from time import sleep
from machine import Pin

from utils.pinout import set_pinout
pinout = set_pinout()

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)

print("simple demo:")
# esp_id = ubinascii.hexlify(machine.unique_id()).decode()                 
# print(esp_id)

def simple_blink():
    pin_led.value(1)
    sleep(0.5)
    pin_led.value(0)
    sleep(0.5)

print("blinking led")
while True:
    simple_blink()
