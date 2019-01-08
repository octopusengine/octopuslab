from machine import SPI,Pin
from lib import st7735
from lib.rgb import color565
import framebuf
import time
import struct
import utime

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))

cs = Pin(5, Pin.OUT)
dc = Pin(16, Pin.OUT)
rst = Pin(17, Pin.OUT)

tft = st7735.ST7735R(spi, cs = cs, dc = dc, rst = rst)

# Initialize FrameBuffer of TFT's size
fb = framebuf.FrameBuffer(bytearray(tft.width*tft.height*2), tft.width, tft.height, framebuf.RGB565)
fbp = fb.pixel

tft.blit_buffer(fb, 0, 0, tft.width, tft.height)

start = utime.ticks_ms()
f = open("octopuslogo-120w-565rgb.bmp", "rb")
fr = f.read
fs = f.seek

# Read header
magic, size, res1,res2, imgoffset = struct.unpack('<2sIHHI', fr(14))

# Read image header
imgheadersize, w, h, planes, bits, comp, imgdatasize, xres,yres, ncol, icol = struct.unpack('<IiiHHIIiiII', fr(40))

# Seek to data file
fs(imgoffset)

for row in range(0, h):
    for col in range(0, w):
        data = fr(2)
        fbp(col, h-row, (data[0] << 8) + data[1])

# Write FB to TFT
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)

print("Took: {0}ms".format(utime.ticks_ms()-start))
