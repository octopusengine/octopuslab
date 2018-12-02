# https://github.com/pdwerryhouse/max7219_8digit
## todo: spi-max7219 https://github.com/mcauser/micropython-max7219
#ampy -p  /COM7 put 05-spi-7display.py main.py

# Connections:
# SCK (CLK)  -> D5 (14)
# MOSI (DIN) -> D7 (13)
# SS (CS)    -> D8 (15)

from machine import Pin, SPI
from lib.max7219_8digit import Display

spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
ss = Pin(15, Pin.OUT)

d = Display(spi, ss)
d.write_to_buffer('12345678')
d.display()
