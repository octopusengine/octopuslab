# octopusLAB - matrix8x8
# ---demo/test disp8 ---

from machine import Pin
from utils.octopus_lib import spi_init
from utils.pinout import set_pinout
from lib.max7219 import Matrix8x8


spi = spi_init()
pinout = set_pinout()
ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)

d8 = Matrix8x8(spi, ss, 4)

d8.fill(0)
d8.text(str("Test"), 0, 0, 1)
d8.show()