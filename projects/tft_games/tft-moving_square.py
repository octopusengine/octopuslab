# octopusLAB - TFT128x160 and ESP32board - 2020/06
from machine import Pin, SPI, SDCard
from time import sleep, sleep_ms
import urandom
from utils.pinout import set_pinout
pinout = set_pinout()
from colors_brg import *

import framebuf
from lib import st7735
from lib.rgb import color565

from components.button import Button
from utils.transform import Point2D

print("buttons init>")
button_dwn = Button(34, release_value=1)
button_top = Button(36, release_value=1)
button_lef = Button(35, release_value=1)
button_rig = Button(39, release_value=1)

# size = 3
cursor = Point2D(63,81)
matrix = Point2D(63/3,81/3)
mx = {} # set

def position(dx,dy):
    global mx # cursor, fb, tft
    cursor.x = cursor.x + dx*3
    cursor.y = cursor.y + dy*3
    matrix.x = matrix.x + dx
    matrix.y =  matrix.y + dy
    mx[matrix.x] = matrix.y 
    print(cursor.x,cursor.y)
    fb.fill(color565(*BLACK))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
    tft.fill_rectangle(cursor.x,cursor.y, 6, 6, color565(*RED))
    # tft.pixel(cursor.x,cursor.y,color565(*RED))


@button_dwn.on_press
def on_press_dwn():
    print("dwn")
    position(0,1)

@button_top.on_press
def on_press_top():
    print("top")
    position(0,-1)

@button_lef.on_press
def on_press_lef():
    print("left")
    position(-1,0)

@button_rig.on_press
def on_press_rig():
    print("right")
    position(1,0)


print("spi.TFT 128x160 init >")

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)

cs = Pin(5, Pin.OUT)  #SCE0() > PWM3(25)
dc = Pin(16, Pin.OUT)  #PWM2(16) > DEV2(33) //RAM > SPI_CS0_PIN(5)/ IO26?
rst = Pin(17, Pin.OUT) #PWM1(17) > DEv3(27)
tft = st7735.ST7735R(spi, cs = cs, dc = dc, rst = rst)

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

sleep(0.6)

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
