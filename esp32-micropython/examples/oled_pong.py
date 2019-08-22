# octopusLAB simple xexample
# HW: ESP32 + i2c OLED display
# import examples.oled_pong

from time import sleep_ms
from util.octopus import *
from util.display_segment import displayDigit

octopus()            # include main library
print("---examples/oled_pong.py---")

def displayNum(num):
    num = str(num)
    for n in range(len(num)):
        displayDigit(o, int(num[n]), n, 2, 6)

XMAX = 128
YMAX = 64
o = oled_init(XMAX, YMAX)      # init oled display
o.clear()            # clear

# default coordinates for position
x = int(XMAX/2)
y = int(YMAX/2)
size = 5

vx = 3
vy = 3

printTitle("oled_pong.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

def drawBall(oled, xold, yold, x, y):
   oled.fill_rect(xold, yold, size, size, 0)
   oled.fill_rect(x, y, size, size, 1)
   oled.show()

drawBall(o,x,y,x,y)   
score = 0

while True:
   xold = x
   yold = y
   x += vx
   y += vy
   if x > XMAX - size: vx = -vx
   if x < 0: vx = -vx
   if y > YMAX - size: vy = -vy
   if y < 0: 
      vy = -vy
      score += 1
      displayNum(score)

   drawBall(o,xold,yold,x,y)
   sleep_ms(3)


