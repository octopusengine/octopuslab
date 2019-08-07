# octopusLAB simple xexample
# HW: ESP32board + EDUshield1 + i2c OLED display

octopus()            # include main library
o = oled_init()      # init oled display
L,R = button_init()  # prepare buttons
# button(L)  
# (0, 10)  ## loop 10x  > count on / off

def horizontal(step=2):
   if button(L)[0] > 8: var.h -= step ## debounce 10x, 9 is OK
   if button(R)[0] > 8: var.h += step
   return var.h

var.h = 63
var.y = 20

from assets.icons9x9 import ICON_clr, ICON_arrow 
# draw_icon(o,ICON_heart,115,15)

while True:
   var.hold = horizontal(5)
   draw_icon(o, ICON_arrow ,var.hold, var.y)
   sleep(0.05)
   draw_icon(o, ICON_clr, var.hold, var.y)
