# octopusLAB example - 2019
# oled dice
# esp32 board and EDU shield1 with oled display

from micropython import const
from util.octopus import printLog, printFree, oled_init, button_init, button
from time import sleep
import urandom

dice = (
(0,0,0,0,0,0,0,0,0),
(0,0,0,0,1,0,0,0,0),
(1,0,0,0,0,0,0,0,1),
(1,0,0,0,1,0,0,0,1),
(1,0,1,0,0,0,1,0,1),
(1,0,1,0,1,0,1,0,1),
(1,1,1,0,0,0,1,1,1)
)
# 1 2 3
# 4 5 6
# 7 8 9
size = 8

def show_dice(num):
    di = 0
    oled.clear()
    # print(dice[num])
    for oR in range(3):
        for oC in range(3):
            # print(di, oR, oC)
            oled.fill_rect(20*oR+35,20*oC+10,size,size, dice[num][di])
            di += 1
    oled.show()

oled = oled_init()
bL = button_init()
bR = button_init(35)

print("start dice")
sleep(1)
oled.clear()

for d in range(6):
    show_dice(d+1)
    sleep(0.3)

def runAuto():
    ir = urandom.randint(1, 6)
    # print(ir)
    show_dice(ir)
    sleep(1)

while True:
    if button(bL)[0] > 8:
      ir = urandom.randint(1, 6)
      print(ir)
      show_dice(ir)
      sleep(0.1)

    if button(bR)[0] > 8:
        while True:
            runAuto()