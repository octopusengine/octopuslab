from util.pinout import set_pinout
from time import sleep
pinout = set_pinout()

from hcsr04 import HCSR04

print("ulrasonic distance sensor")

# servo1: 17, servo2: 16, 4 # t16 / e17

# Echo module
echo = HCSR04(trigger_pin=pinout.PWM2_PIN, echo_pin=pinout.PWM1_PIN)

while True:
    echo_cm = echo.distance_cm()
    print(echo_cm)
    sleep(1)

"""
DEBUG = True

def debug(msg):
    if DEBUG:
        print("DEBUG: " + msg)

if echo_cm < ECHO_Treshold and echo_cm > 2 and motoRun:
    debug("Distance less than threshols {0}. Stopping motors!".format(ECHO_Treshold))
"""