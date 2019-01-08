from machine import SPI,Pin
from lib import st7735
from lib.rgb import color565
import framebuf

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))

cs = Pin(5, Pin.OUT)
dc = Pin(16, Pin.OUT)
rst = Pin(17, Pin.OUT)

tft = st7735.ST7735R(spi, cs = cs, dc = dc, rst = rst)

# Initialize FrameBuffer of TFT's size
fb = framebuf.FrameBuffer(bytearray(tft.width*tft.height*2), tft.width, tft.height, framebuf.RGB565)
fbp = fb.pixel

while True:
    fb.fill(color565(255,0,0))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)

    fb.fill(color565(0,255,0))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)

    fb.fill(color565(0,0,255))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
