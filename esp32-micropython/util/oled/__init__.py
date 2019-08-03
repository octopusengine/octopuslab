# Oled display - ssd1306

from time import sleep_ms
from machine import Pin
from lib import ssd1306

OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7

class Oled(ssd1306.SSD1306_I2C):
    def __init__(self, i2c, ox=OLEDX, oy=OLEDY):
        self.ox = ox
        self.oy = oy
        super().__init__(ox, oy, i2c)

    def test(self):
        self.text('oled display OK', OLED_x0, 3)
        self.hline(0,52,self.ox,1)
        self.text("octopusLAB 2019",OLED_x0,OLED_ydown)
        self.show()

    def draw_icon(self, icon, posx, posy):
        for y, row in enumerate(icon):
            for x, c in enumerate(row):
                self.pixel(x+posx, y+posy, c)
        self.show()