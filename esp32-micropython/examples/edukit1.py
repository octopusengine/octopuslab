# simple basic example - ESP32 - Micropython - EDU_KIT1
# ROBOTboard with "BUILT_IN_LED", "WS RGB_LED" and "disp7"
# 30.6.2020

from time import sleep
from components.led import Led
from components.rgb import Rgb
from utils.octopus import disp7_init, printOctopus
from utils.pinout import set_pinout

print("this is simple Micropython example | ESP32 & octopusLAB")
printOctopus()
pinout = set_pinout()  # set board pinout
from utils.io_config import get_from_file
io_conf = get_from_file()

led = Led(2)
led.blink()

ws = Rgb(pinout.WS_LED_PIN,io_conf.get('ws'))
ws.simpleTest()

d7 = disp7_init() # display init

def d7pause(ch = "-", sl = 0.5):
    for i in range(8):
        d7.show(" "*i + ch)
        sleep(sl)

sleep(2)
d7pause(sl=0.1)

ws.rainbow_cycle()
ws.color((0,0,0))

for i in range(9):
    d7.show(10-i)
    sleep(0.3)
d7.show("")
