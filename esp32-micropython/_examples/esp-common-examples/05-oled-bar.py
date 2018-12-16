"""
This is usage of SSD1306 OLED display with simple graphics elements

"""

import machine
import time
import urandom
from lib import ssd1306
from assets.icons9x9 import ICON_clr, ICON_wifi

from util.pinout import set_pinout
pinout = set_pinout()

i2c_sda = machine.Pin(pinout.I2C_SDA_PIN, machine.Pin.IN,  machine.Pin.PULL_UP)
i2c_scl = machine.Pin(pinout.I2C_SCL_PIN, machine.Pin.OUT, machine.Pin.PULL_UP)

IMAGE_WIDTH = 63
IMAGE_HEIGHT = 63

i2c = machine.I2C(-1, i2c_scl, i2c_sda)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# reset display
oled.fill(0)
oled.show()

# write text on x, y
#oled.text('octopusLAB', 20, 47)
oled.text('octopusLAB', 0, 1)

sevenSeg = [      #seven segment display
#0,1,2,3,4,5,6
 [1,1,1,1,1,1,0], #0      +----0----+
 [0,1,1,0,0,0,0], #1      |         |
 [1,1,0,1,1,0,1], #2      5         1
 [1,1,1,1,0,0,1], #3      |         |
 [0,1,1,0,0,1,1], #4      +----6----+
 [1,0,1,1,0,1,1], #5      |         |
 [1,0,1,1,1,1,1], #6      4         2
 [1,1,1,0,0,0,0], #7      |         |
 [1,1,1,1,1,1,1], #8      +----3----+
 [1,1,1,1,0,1,1], #9
 [1,1,0,0,0,1,1], #deg
 [0,0,0,0,0,0,1]  #-
]

def oneDigit(seg,x,y,a): #segment /x,y position / a=size
    oled.hline(x,y,a,seg[0])
    oled.vline(x+a,y,a,seg[1])
    oled.vline(x+a,y+a,a,seg[2])
    oled.hline(x,y+a+a,a,seg[3])
    oled.vline(x,y+a,a,seg[4])
    oled.vline(x,y,a,seg[5])
    oled.hline(x,y+a,a,seg[6])

def threeDigits(d,point,deg): #display number 0-999 / point 99.9 / degrees
    d100=int(d/100)
    d10=int((d-d100*100)/10)
    d1= d-d100*100-d10*10
    oneDigit(sevenSeg[d100],x0,y0,aa)
    oneDigit(sevenSeg[d10],x0+aa+int(aa/2),y0,aa)
    oneDigit(sevenSeg[d1],x0+(aa+int(aa/2))*2,y0,aa)
    if point:
       oled.fill_rect(x0+(aa+int(aa/2))*2-5,y0+aa+aa,2,3,1) #test poin
    if deg:
       oneDigit(sevenSeg[10],x0+(aa+int(aa/2))*3,y0,aa) #test deg
    oled.show()

def draw_icon(icon, posx, posy):
  for y, row in enumerate(icon):
    for x, c in enumerate(row):
        oled.pixel(x+posx, y+posy, c)


aa = 16
y0 = 16
x0 = aa+5
xb0 = 0 # display bar possition
yb0 = 58
ydown = 57

def displMessage(mess,timm):
    oled.fill_rect(0,ydown,128,10,0)
    oled.text(mess, x0, ydown)
    oled.show()
    time.sleep_ms(timm*1000)

def displBar(by,num,timb,anim):
    oled.fill_rect(xb0,by-1,128,5+2,0) # clear
    for i in range(10):               # 0
        oled.hline(xb0+i*13,by+2,9,1)
    for i in range(num):               # 1
        oled.fill_rect(xb0+i*13,by,10,5,1)
        if anim:
           oled.show()
           time.sleep_ms(20) # animation
    oled.show()
    time.sleep_ms(timb)

displMessage("init >",1)

#--- start
displMessage("start >",1)

#oled.text("wifi",85, 1)
#draw_icon(ICON_wifi, 85+34 ,0)
oled.text("wifi",99, 1)
for _ in range(5):
    draw_icon(ICON_clr, 88 ,0)
    oled.show()
    time.sleep_ms(200)
    draw_icon(ICON_wifi, 88 ,0)
    oled.show()
    time.sleep_ms(300)

threeDigits(210,True,True)

for i in range(20):
    ir = urandom.randint(1, 10)
    displBar(yb0,ir,300,1)

#draw_icon(ICON_heart, 0,0)
#draw_icon(ICON_arrow, 100,0)
#draw_icon(ICON_test, 100,30)
