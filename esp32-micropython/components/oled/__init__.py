# Oled display - ssd1306

__version__ = "1.0.2"

from time import sleep_ms
from machine import Pin
import ssd1306
from components.display_segment import *

OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7
IMAGE_WIDTH = 63 # default size
IMAGE_HEIGHT = 63

class Oled(ssd1306.SSD1306_I2C):
    def __init__(self, i2c, addr=0x3c, ox = OLEDX, oy = OLEDY):
        self.ox = ox
        self.oy = oy
        super().__init__(ox, oy, i2c, addr=addr)

    def clear(self,how=0):
        self.fill(how)
        self.show()

    def test(self):
        self.text('oled display OK', OLED_x0, 3)
        self.hline(0,52,self.ox,1)
        self.text("octopusLAB 2019", OLED_x0, OLED_ydown)
        self.show()

    def draw_icon(self, icon, posx, posy):
        for y, row in enumerate(icon):
            for x, c in enumerate(row):
                self.pixel(x+posx, y+posy, c)
        self.show()

    def draw_image(self, file="assets/octopus_image.pbm",iw = IMAGE_WIDTH, ih = IMAGE_HEIGHT):
        import framebuf
        with open(file, 'rb') as f:
            f.readline() # Magic number
            f.readline() # Creator comment
            f.readline() # Dimensions
            data = bytearray(f.read())
            # fbuf.fill(0)
            fbuf = framebuf.FrameBuffer(data, iw, ih, framebuf.MONO_HLSB)
            # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
            self.invert(1)
            self.blit(fbuf, 0, 0)
        self.show()

    def oledSegment(self,num,point=False,deg=False):
        threeDigits(num,point,deg)

"""
def oledSegmentTest(oled):
    print("oled segment test >")
    oled.fill(0)
    oled.text('octopusLAB test', OLED_x0, 3)
    for num in range(100):
        oledSegment(oled,100-num)
        sleep_ms(50)
"""
