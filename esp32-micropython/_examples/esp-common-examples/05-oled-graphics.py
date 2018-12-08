"""
This is usage of SSD1306 OLED display with simple graphics elements
inspiration: https://www.pymadethis.com/article/oled-displays-i2c-micropython

needs external driver ssd1306.py
from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

Set your SCL and SDA pins in constants

Installation:
./octopus_robot_board.py
./lib/ssd1306.py
ampy -p /dev/ttyUSB0 put ./05-oled-graphics.py main.py
# reset device
"""

import machine
import time
import urandom
from lib import ssd1306

import octopus_robot_board as o #octopusLab main library - "o" < octopus

i2c = machine.I2C(-1, machine.Pin(o.I2C_SCL_PIN), machine.Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()

time.sleep_ms(300)

# reset display
oled.fill(0)
oled.show()

# write text on x, y
oled.text('octopusLAB', 20, 50)

oled.pixel(3, 4, 1)  # .pixel(x, y, c) # 3rd param is the colour
oled.hline(20, 3, 25, 1) # .hline(x, y, w, c)
oled.line(30, 20, 50, 30, 1) # .line(x1, y1, x2, y2, c)
oled.line(20, 30, 30, 50, 1) # .line(x1, y1, x2, y2, c)
oled.rect(50, 5, 30, 20, 1) # .rect(x, y, w, h, c)
oled.fill_rect(9, 30, 10, 15, 1) # .fill_rect(x, y, w, h, c)
oled.show()

def draw_icon(icon, posx, posy):
  for y, row in enumerate(icon):
    for x, c in enumerate(row):
        oled.pixel(x+posx, y+posy, c)

ICON_heart = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [ 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [ 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

ICON_arrow = [
    [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [ 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [ 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [ 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

ICON_test = [
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

draw_icon(ICON_heart, 0,0)
draw_icon(ICON_arrow, 100,0)
draw_icon(ICON_test, 100,30)
oled.show()

#xofs = urandom.getrandbits(100)
#yofs = urandom.getrandbits(50)
# ?value error
#oled.text(" --- "+str(xofs)+" ---", 20, 35)
#oled.show()
#draw_icon(ICON, xofs,yofs)
#oled.show()

"""
def random_heart():
    xofs = urandom.getrandbits(120)
    yofs = urandom.getrandbits(60)
    draw_icon(ICON, xofs,yofs)

for n in range(100):
    random_heart()

oled.show()
"""
