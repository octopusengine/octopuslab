# octopusLAB - TFT128x160 and ESP32board - 2020/06
import urandom
from utils.pinout import set_pinout
pinout = set_pinout()

from ST7735 import TFT, TFTColor
from assets.sysfont import sysfont
from machine import SPI, Pin
from time import sleep_ms, ticks_ms
from math import pi
from utils.octopus_lib import w

from components.button import Button
from utils.transform import Point2D

print("buttons init>")
pin_dwn    = Pin(35, Pin.IN)
button_dwn = Button(pin_dwn, release_value=1)
pin_top    = Pin(39, Pin.IN)
button_top = Button(pin_top, release_value=1)
pin_lef    = Pin(36, Pin.IN)
button_lef = Button(pin_lef, release_value=1)
pin_rig    = Pin(34, Pin.IN)
button_rig = Button(pin_rig, release_value=1)

SPI_SCLK = 18
SPI_MISO = 19
SPI_MOSI = 23

DC = 17   # PWM1
RST = 16  # PWM2
CS = 5    # SCE0

print("--- TFT 128x160px test ---")

spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(SPI_SCLK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
tft=TFT(spi, DC, RST, CS)
tft.initr()
tft.rgb(True)

tft.fill(TFT.BLACK)
v = 30
tft.text((0, v), "octopus LAB (1)", TFT.RED, sysfont, 1, nowrap=True)
v += sysfont["Height"]

tft.fill(TFT.BLACK)
tft.rotation(1)

# size = 3
cursor = Point2D(63,81)
matrix = Point2D(63/3,81/3)
mx = {} # set

tft.fill(TFT.BLACK)
tft.fillrect((cursor.x, cursor.y), (4, 4), TFT.WHITE)

def position(dx,dy):
    global mx # cursor, fb, tft
    cursor.x = cursor.x + dx*3
    cursor.y = cursor.y + dy*3
    matrix.x = matrix.x + dx
    matrix.y =  matrix.y + dy
    mx[matrix.x] = matrix.y 
    print(cursor.x,cursor.y)
    tft.fill(TFT.BLACK)
    tft.fillrect((cursor.x, cursor.y), (4, 4), TFT.WHITE)


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
