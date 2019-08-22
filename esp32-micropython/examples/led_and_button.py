# octopusLAB simple example
# ESP32board with "BUILT_IN_LED" and boot button0
# import examples.led_and_button

# from util.octopus import octopus, button_init, button, led
from util.octopus import *

octopus()

print("---examples/led_and_button.py---")

but = button_init(0) # 0 boot pin / or pin 34 > esp32 shield1
# led = Led()        # default

def run():
    while True:
        if button(but)[0] > 8:
            led.value(1)
        else:
            led.value(0)

run()