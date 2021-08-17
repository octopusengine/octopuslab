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

# octopusLAB - matrix8x8
# ---demo/test disp8 ---

from time import sleep
from machine import Pin
from utils.octopus_lib import spi_init
from utils.pinout import set_pinout
from lib.max7219 import Matrix8x8


spi = spi_init()
pinout = set_pinout()
ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)

d8 = Matrix8x8(spi, ss, 4)


def scroll(d8, text, num):  # TODO speed, timer? / NO "sleep"
    WIDTH = 8*4
    x = WIDTH + 2
    for _ in range(8*len(text)*num):
        sleep(0.03)
        d8.fill(0)
        x -= 1
        if x < - (8*len(text)):
            x = WIDTH + 2
        d8.text(text, x, 0, 1)
        d8.show()
    d8.fill(0)
    d8.show()


d8.fill(0)
d8.text(str("Test"), 0, 0, 1)
d8.show()

# scroll(d8, "pokus posuv 123", 5')