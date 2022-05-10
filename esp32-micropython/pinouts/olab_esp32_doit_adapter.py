"""
This is octopusLab basic library for DOIT adapter PCB and esp32 soc
I2C / SPI / SERVO / PWM...
Edition: --- 10.08.2021 ---
"""
from micropython import const
from pinouts.olab_esp32_base import *

##WS_LED_PIN 13          # Robot Board v1
WS_LED_PIN = const(15)   # Robot Board v2 - WS RGB ledi diode
ONE_WIRE_PIN = const(32)  #one wire (for Dallas temperature sensor)
PIEZZO_PIN = const(27)

#main analog input (for power management)
ANALOG_PIN = const(36)

#PWM/servo:
PWM1_PIN = const(17)
PWM2_PIN = const(16)
PWM3_PIN = const(4)
#pwm duty for servo:
SERVO_MIN = const(38)
SERVO_MAX= const(130)

#inputs:
I39_PIN = const(39)
I34_PIN = const(34)
I35_PIN = const(35)
BTN_LEFT = const(34)
BTN_RIGHT = const(35)

#temp
MFET_PIN = const(17) # PWM1
RELAY_PIN = const(16) # PWM2

# DEV pins
DEV1_PIN = const(32)
DEV2_PIN = const(33)
