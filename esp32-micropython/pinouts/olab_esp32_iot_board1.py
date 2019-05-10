"""
This is octopusLab basic library for iotBoard PCB and esp32 soc
I2C / SPI / MOTORs / SERVO / PWM...
Edition: --- 2.1.2019 ---
"""
from micropython import const
from pinouts.olab_esp32_base import *

#---esp32---IoT board:
PIEZZO_PIN = const(27)  #14 //MOTOR_4A = const(27)
WS_LED_PIN = const(15)  #TDO
ANALOG_PIN = const(36)
ONE_WIRE_PIN = const(32) # = DEV1_PIN
RELAY_PIN = const(33)
MFET_PIN = const(14)

BUTT1_PIN = const(25) # up
BUTT2_PIN = const(12) # o #TDI
BUTT3_PIN = const(13) # dw #TCK

PWM1_PIN = const(17) #PWM/servo //pwr for moisture
PWM2_PIN = const(16)
PWM3_PIN = const(4)

DEV1_PIN = const(32)
DEV2_PIN = const(26)

#inputs:
I39_PIN = const(39)
I34_PIN = const(34)
I35_PIN = const(35) #analog in for moisture
