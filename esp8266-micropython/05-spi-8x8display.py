#spi-max7219 https://github.com/mcauser/micropython-max7219
#ampy -p  /COM7 put 05-spi-8x8display.py main.py

# Connections:
# SCK (CLK) -> GPIO4
# MOSI (DIN) -> GPIO2
# SS (CS) -> GPIO5
#spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
#ss = Pin(15, Pin.OUT)

from machine import Pin, SPI
from lib.max7219 import Matrix8x8

spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
display = Matrix8x8(spi, Pin(15), 4)
display.brightness(0)
display.fill(0)
display.text("oLAB",0,0,1)
display.show()
