"""
This is first basic test ESP32 programming
needs only ESP32 (DoIt 2x15pin)
Installation:
ampy -p /dev/ttyUSB0 put ./01-blink.py main.py
# reset device
"""
from machine import Pin
from time import sleep
pin_diody = Pin(2, Pin.OUT)
while True:
    pin_diody.value(0)
    sleep(1/2)
    pin_diody.value(1)
    sleep(1/2)
