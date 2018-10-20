"""
This is first basic test ESP32 programming
needs only ESP32 (DoIt 2x15pin)
Installation:
Linux:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py 
ampy -p /dev/ttyUSB0 put ./01-blink.py main.py
Windows:
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./01-blink.py main.py
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
