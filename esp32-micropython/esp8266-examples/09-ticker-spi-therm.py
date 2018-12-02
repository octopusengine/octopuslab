# https://github.com/pdwerryhouse/max7219_8digit
## todo: spi-max7219 https://github.com/mcauser/micropython-max7219
#ampy -p  /COM7 put 05-spi-7display.py main.py

# Connections:
# SCK (CLK)  -> D5 (14)
# MOSI (DIN) -> D7 (13)
# SS (CS)    -> D8 (15)

import time
from machine import Pin, SPI
from lib.max7219_8digit import Display
from lib.temperature import TemperatureSensor
ONE_WIRE_PIN = 2

ts = TemperatureSensor(ONE_WIRE_PIN)

spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
ss = Pin(15, Pin.OUT)

d = Display(spi, ss)
d.write_to_buffer('12345678')
d.display()
time.sleep_ms(2000)

while True:
    temp = ts.read_temp()
    d.write_to_buffer(str(temp))
    d.display()
    time.sleep_ms(2000)
