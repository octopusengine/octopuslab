"""
This is octopusLab basic library for ESP32 board PCB and esp32 soc
Edition: --- 10.8.2019 ---
"""
from micropython import const
from pinouts.olab_esp32_base import *

BUTT1_PIN = const(0)

PWM1_PIN = const(17)
PWM2_PIN = const(16)
PWM3_PIN = const(25)

DEV1_PIN = const(32)
DEV2_PIN = const(33)
DEV3_PIN = const(27)

#inputs:
I34_PIN = const(34)
I39_PIN = const(39)
I35_PIN = const(35)

# UART 1
RXD1 = const(36)
TXD1 = const(4)

PIEZZO_PIN = const(27) # hack on DEV3
