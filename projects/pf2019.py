"""
This is simple usage of TFT ST7735 display over SPI
needs external driver from adafruit from https://github.com/adafruit/micropython-adafruit-rgb-display

Installation:
./lib/rgb.py
./lib/st7735.py
ampy -p /dev/ttyUSB0 put ./05-tft-st7735.py main.py
# reset device

"""
from machine import SPI,Pin
from lib import st7735
from lib.rgb import color565
import framebuf
import time

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))

cs = Pin(5, Pin.OUT)
dc = Pin(16, Pin.OUT)
rst = Pin(17, Pin.OUT)

tft = st7735.ST7735R(spi, cs = cs, dc = dc, rst = rst)
fb = framebuf.FrameBuffer(bytearray(tft.width*tft.height*2), tft.width, tft.height, framebuf.RGB565)

# reset display
fb.fill(0)

fb.text('OctopusLab', 20, 15, color565(255,255,255))
fb.text("PF 2019", 35, 55, color565(255,255,255))
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
