"""
This is octopusLab basic library for robotBoard PCB
I2C / SPI / MOTORs / SERVO / PWM...
Edition: --- 31.10.2018 ---
Installation:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
"""

from micropython import const
# inherit from robot board1
from pinouts.olab_esp32_robot_board1 import *

WS_LED_PIN = const(13)   # Robot Board v1 - WS RGB ledi diode
MOTOR_34EN = const(15)   # Robot Board v1
