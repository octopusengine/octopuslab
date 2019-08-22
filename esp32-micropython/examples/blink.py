# octopusLAB simple example
# ESP32board with "BUILT_IN_LED"
# import examples.blink

# from util.octopus import octopus, button_init, button, led
from util.octopus import *
octopus()       # include main library

print("---examples/blink.py---")

#def run():
while True:
    led.blink()

#run()