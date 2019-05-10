'''
Example usage of reading temperature from dallas DS18B20 sensor and displaying on a 8 digit led display MAX7219
'''

from machine import Pin, SPI
from time import sleep
from lib.temperature import TemperatureSensor
from lib.max7219_8digit import Display
from util.pinout import set_pinout
pinout = set_pinout()

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
d7 = Display(spi, ss)

ts = TemperatureSensor(pinout.ONE_WIRE_PIN)


while True:
    temp = ts.read_temp()
    d7.write_to_buffer("{}".format(temp))
    d7.display()
    sleep(1)
