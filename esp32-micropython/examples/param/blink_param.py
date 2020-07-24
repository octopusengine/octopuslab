# octopusLAB simple example
# ESP32board with "BUILT_IN_LED"
# parameter: delay [ms]

from components.led import Led
# from utils.octopus import led # short way
from utils.pinout import set_pinout

print("---examples/blink_param.py---")

# _ARGS
# ToDo parse: delay=1000,pin=25
delay = 1000
try:
    delay = (int(_ARGS[0]))
    print("delay = ", str(delay))
except Exception as e:
    print("Exception: {0}".format(e))

pinout = set_pinout()           # set board pinout
led = Led(pinout.BUILT_IN_LED)  # BUILT_IN_LED = 2


# start main loop
while True:
    led.blink(delay)
