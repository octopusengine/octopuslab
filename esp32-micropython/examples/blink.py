# octopusLAB simple example
# ESP32board with "BUILT_IN_LED"
# run: import examples.blink

from util.led import Led
from util.pinout import set_pinout

pinout = set_pinout()           # set board pinout
led = Led(pinout.BUILT_IN_LED)  # BUILT_IN_LED = 2

print("---examples/blink.py---")

while True:
    led.blink()