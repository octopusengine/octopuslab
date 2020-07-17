# octopusLAB simple example
# ESP32board with "BUILT_IN_LED"

from components.led import Led
# from utils.octopus import led # short way
from utils.pinout import set_pinout

pinout = set_pinout()           # set board pinout
led = Led(pinout.BUILT_IN_LED)  # BUILT_IN_LED = 2

print("---examples/blink.py---")
# start main loop

while True:
    led.blink()