from util.pinout import set_pinout
from util.octopus import disp7_init
from util.rgb import Rgb

from time import sleep
pinout = set_pinout()

from hcsr04 import HCSR04
d7 = disp7_init()
ws = Rgb(4)

print("ulrasonic distance sensor")

# servo1: 17, servo2: 16, 4 # t16 / e17

# Echo module
echo = HCSR04(trigger_pin=pinout.PWM2_PIN, echo_pin=pinout.PWM1_PIN)

while True:
    echo_cm = echo.distance_cm()
    d7.show(int(echo_cm))
    if echo_cm > 15:
        ws.color((32,0,0))
        print("---treshold---")
    else:
        ws.color((0,32,0))
    print(echo_cm)
    sleep(0.5)
