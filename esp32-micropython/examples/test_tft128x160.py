# octopusLAB - TFT128x160 and ESP32board - 2020/06
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

tft = st7735fb.ST7735R(spi, cs = cs, dc = dc, rst = None)

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

for i in range(0,3):
    fb.fill(0)
    fb.text('OctopusLab', 20, 15, color565(255,255,255))
    fb.text(" --- "+str(3-i)+" ---", 20, 55, color565(255,255,255))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
    sleep(0.5)

fb.line(0,83,128,83,color565(255,0,0)) # BGR
fb.line(0,0,128,166,color565(0,0,255))
fb.line(128,0,0,166,color565(0,255,0))
tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
sleep(2)

for _ in range(1000):
    x = urandom.randint(1, 128)
    y = urandom.randint(1, 166)
    tft.pixel(x,y,color565(*RED))
