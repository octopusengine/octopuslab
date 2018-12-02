# https://github.com/pdwerryhouse/max7219_8digit
## todo: spi-max7219 https://github.com/mcauser/micropython-max7219
#ampy -p  /COM7 put 05-spi-7display.py main.py

# Connections:
# SCK (CLK)  -> D5 (14)
# MOSI (DIN) -> D7 (13)
# SS (CS)    -> D8 (15)

import time
from micropython import const
from machine import Pin, SPI
from lib.max7219_8digit import Display
from lib.temperature import TemperatureSensor

#SPI:
SPI_CLK_PIN  = const(14)
SPI_MOSI_PIN = const(13)
SPI_MISO_PIN = const(12)
SPI_CS0_PIN  = const(15)

spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(SPI_CLK_PIN), mosi=Pin(SPI_MOSI_PIN), miso=Pin(SPI_MISO_PIN))
ss = Pin(SPI_CS0_PIN, Pin.OUT)
d = Display(spi, ss)

ONE_WIRE_PIN = 2
ts = TemperatureSensor(ONE_WIRE_PIN)

d.display()
time.sleep_ms(2000)

while True:
    d.write_to_buffer(' OCtOPUS')
    d.display()
    time.sleep_ms(600)
    d.write_to_buffer('    LAB')
    d.display()
    time.sleep_ms(500)

    temp = ts.read_temp()
    time.sleep_ms(100)
    d.write_to_buffer("  "+str(int(temp*10)/10)+" C")
    d.display()
    time.sleep_ms(3000)
