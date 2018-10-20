"""
This is first basic test ESP32 programming
needs only ESP32 (DoIt 2x15pin)

Installation:
Linux:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
ampy -p /dev/ttyUSB0 put ./01-blink.py main.py
Windows: (COM6 or another detected comPort)
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./01-blink.py main.py
# reset device
"""
from machine import Pin
from time import sleep

import octopus_robot_board as o #octopusLab main library - "o" < octopus

led = Pin(o.BUILT_IN_LED, Pin.OUT)
while True:
    led.value(0)
    sleep(1/2)
    led.value(1)
    sleep(1/2)
