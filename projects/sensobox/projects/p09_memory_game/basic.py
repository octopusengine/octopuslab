from sensobox.button import a_instance as left_btn, b_instance as right_btn
from sensobox.display import instance as display
from time import sleep_ms

import random

values = []
display_left = "****"
display_right = "vvvv"
left = True
right = False

for i in range(4):
    values.append(random.getrandbits(1))
    
for b in values:
    display.show(display_left if b else display_right)
    sleep_ms(400)
    display.show("    ")
    sleep_ms(400)
@left_btn.on_press
def a():
    check(left)
    
@right_btn.on_press
def b():
    check(right)
    
def check(side):
    display.show(display_left if side else display_right)
    sleep_ms(100)
    display.show("    ")
    v = values.pop(0)
    if v != side:
        wrong()
    elif len(values) == 0:
        win()
        
def win():
    for _ in range(3):
        display.show("nice")
        sleep_ms(300)
        display.show("    ")
        sleep_ms(300)
        
def wrong():
    for _ in range(3):
        display.show("----")
        sleep_ms(300)
        display.show("    ")
        sleep_ms(300)
