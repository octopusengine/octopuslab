# octopusLAB simple example 2019
# HW: ESP32 + i2c OLED display
# ampy -p /COM6 put examples/oled_random_lines.py main.py
# start: import examples/oled_random_lines

from utils.octopus import oled_init
from shell.terminal import printTitle
from os import urandom

o = oled_init()      # init oled display
o.fill(0)            # clear

# default coordinates for position
x = 0
y = 0

printTitle("oled_random_lines.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
   old_x = x
   old_y = y
   # get new position
   x = int(urandom(1)[0]/2)
   y = int(urandom(1)[0]/4)

   o.line(old_x, old_y, x, y, 1)
   o.show()
   # sleep(0.1) # slow or fast
