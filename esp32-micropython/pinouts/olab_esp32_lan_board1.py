"""
This is octopusLab basic library for LANboard PCB and esp32 soc
Edition: --- 13.7.2019 ---
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

BUTT1_PIN = const(0) # up
