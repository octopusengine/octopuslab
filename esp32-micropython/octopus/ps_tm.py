# octopusLAB simple example
# HW: ESP32 + TM1638 shield

from machine import Timer
from utils.pinout import set_pinout
from machine import Pin
pinout = set_pinout()
from lib.tm1638 import TM1638
import pubsub

# right OCTOBUS SCI:
# STB = MOSI 23
# CLK = MISO 19
# DIO = SCLK 18

print("--- pubsub: tm1638 init ---> publish('btn_value') ")

tm = TM1638(stb=Pin(pinout.SPI_MOSI_PIN), clk=Pin(pinout.SPI_MISO_PIN), dio=Pin(pinout.SPI_CLK_PIN))
tim0 = Timer(0)


@pubsub.subscriber("tm_display")
def ps_show(value):
    print("ps_tm disp: ",value)
    tm.show2(value)


def timer_init(per= 50):      # period 10 ms 10000 ms (1s/1000)
    print("--- pubsub: timer_init ---")  # for deactivate: tim0.deinit()
    tim0.init(period=per, mode=Timer.PERIODIC, callback=lambda t:timerAction())


old_kbd = 0
def timerAction():
    global old_kbd
    kbd = tm.keys()
    if kbd[0] > 0:
        if kbd[0] != old_kbd:
            # print("ps_tm: ",str(kbd)) 
            pubsub.publish('tm_button', kbd[0])
    old_kbd = kbd[0]



timer_init()
print("---/---")





