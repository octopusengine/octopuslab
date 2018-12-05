"""
This is first basic test ESP32 programming
needs only ESP32 (DoIt 2x15pin)

Installation:
ampy -p /dev/ttyUSB0 put ./01-blink.py main.py
# reset device
"""
from machine import Pin
from time import sleep
BUILT_IN_LED = 2

led = Pin(BUILT_IN_LED, Pin.OUT)
while True:
    led.value(0)
    sleep(1/2)
    led.value(1)
    sleep(1/2)
