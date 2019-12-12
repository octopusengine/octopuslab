# octopusLAB simple example
# HW: ESP32board + EDUshield1 + i2c OLED display

from util.octopus import *
from util import printTitle

octopus()            # include main library
o = oled_init()      # init oled display
L, R, C = buttons_init()  # prepare buttons
# button(L)  
# (0, 10)  ## loop 10x  > count on / off

# load icon
from assets.icons9x9 import ICON_clr, ICON_arrow 
# draw_icon(o,ICON_heart,115,15)

# default coordinates for icon
x = 63
y = 20
# move step pixels with each button press
step = 5
# debounce: read 10 samples, only tolerate one false reading
debounce = 9

o.fill(0)
o.hline(0,51,128,1)
o.text("octopusLAB 2019",3,64-7)
o.show()

# draw first position
o.draw_icon(ICON_arrow, x, y)
# init helper var
old_x = x

printTitle("button2oled.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
   # get new position
   old_x = x
   if button(L)[0] >= debounce: x -= step
   if button(R)[0] >= debounce: x += step
   # only if changed
   if old_x != x:
      # clear current position
      o.draw_icon(ICON_clr, old_x, y)
      # draw new icon
      o.draw_icon(ICON_arrow, x, y)
   # sleep
   sleep(0.05)
