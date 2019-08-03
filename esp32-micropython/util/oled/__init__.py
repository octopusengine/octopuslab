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
        print("__init__()")
        print(ox)
        print(oy)
        self.oled = ssd1306.SSD1306_I2C(ox, oy, i2c)

    def test(self):
        self.oled.text('oled display OK', OLED_x0, 3)
        self.oled.hline(0,52,128,1)
        self.oled.text("octopusLAB 2019",OLED_x0,OLED_ydown)
        self.oled.show()    
       