"""
This is octopusLab basic library for iotBoard PCB and esp32 soc
I2C / SPI / MOTORs / SERVO / PWM...
Edition: --- 2.1.2019 ---
"""
from micropython import const
from pinouts.olab_esp32_base import *

# PIN as on octopusLAB LAN board 1 with built-in ESP32

BUILT_IN_LED = const(4)
HALL_SENSOR = const(8)

#I2C:
I2C_SCL_PIN = const(16)
I2C_SDA_PIN = const(2)

# SPI:
SPI_CLK_PIN  = const(32)
SPI_MISO_PIN = const(35)
SPI_MOSI_PIN = const(33)
SPI_CS0_PIN  = const(5)

#---esp32---LAN board:
PIEZZO_PIN = None
WS_LED_PIN = None
ANALOG_PIN = const(34)
ONE_WIRE_PIN = const(32) # = DEV1_PIN

BUTT1_PIN = const(0) # up

#inputs:
I39_PIN = const(39)
I34_PIN = const(34)
I35_PIN = const(35) #analog in for moisture
