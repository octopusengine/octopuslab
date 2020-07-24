# stopwatch

from time import sleep
from utils.octopus import button_init, button, disp7_init
from shell.terminal import printTitle

BB = button_init(0) # button boot = 0
# debounce: read 10 samples, only tolerate one false reading
debounce = 9

d7 = disp7_init()

select = 0
sec = 0
run = False

printTitle("stopwatch.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
    # print(select)
    if run:
        sec += 1
        d7.show(sec/10)
        print(sec/10)
        sleep(0.1)

    if button(BB)[0] >= debounce:
        beep()
        select += 1 
        sleep(0.3)

        if select == 1:
            run = True
           
        if select == 2:
            run = False

        if select == 3:
            sec = 0
            d7.show("0.0")

        if select > 3:
            select = 1
            run = True



