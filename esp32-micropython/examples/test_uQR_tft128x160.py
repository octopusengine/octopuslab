# octopusLAB - TFT128x160 and ESP32board - 2020/06
try:
    import uqr
except ImportError:
    print("Error importing uQR native library, check if you have modded micropython version")

from machine import Pin, SPI
from time import sleep, sleep_ms
import urandom
from colors_brg import *

import framebuf
from lib import st7735fb
from lib.rgb import color565

print("spi.TFT 128x160 init >")

spi = SPI(2, baudrate=20000000, sck=Pin(18), mosi=Pin(23))

cs = Pin(26, Pin.OUT)
dc = Pin(25, Pin.OUT)

tft = st7735fb.ST7735R(spi, cs = cs, dc = dc, rst = None, rotation=3)

print("spi.TFT framebufer >")

# Initialize FrameBuffer of TFT's size
fb = framebuf.FrameBuffer(bytearray(tft.width*tft.height*2), tft.width, tft.height, framebuf.RGB565)
fbp = fb.pixel

fb.fill(color565(*BLUE))
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
sleep(1)

fb.fill(color565(*RED))
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
sleep(1)

fb.fill(color565(*GREEN))
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
sleep(1)

# reset display
fb.fill(0)
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)

sleep(0.5)

qr = uqr.make("OctopusLAB QR Code")

def draw_qr(pos_x, pos_y, qr, scale = 4, border = None):
    border = border or scale * 2
    fb.fill_rect(
        pos_x-(border//2),
        pos_y-(border//2),
        (qr.width()*scale)+(border),
        (qr.width()*scale)+(border),
        color565(*WHITE))

    for x in range(qr.width()):
        for y in range(qr.width()):
            if qr.get(x,y):
                fb.fill_rect(pos_x+x*scale, pos_y+y*scale, scale, scale, 0)

    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)

qr_pos_x = 30
qr_pos_y = 15
qr_scale = 4
qr_border = 10

draw_qr(qr_pos_x, qr_pos_y, qr, qr_scale, qr_border)
