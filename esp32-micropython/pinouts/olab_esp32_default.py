# Default board, some basic interfaces like I2C, SPI and built-in led

from micropython import const
from pinouts.olab_esp32_base import *

ANALOG_PIN = const(36)
BUTT1_PIN = const(12)
PIEZZO_PIN = const(14)
WS_LED_PIN = const(15)
ONE_WIRE_PIN = const(13)
