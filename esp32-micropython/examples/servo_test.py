# servo test - example
from time import sleep
from util.pinout import set_pinout

from util.servo import Servo
# todo: PWM double setup error

pinout = set_pinout()


# s1 = Servo(pinout.PWM1_PIN)
# s2 = Servo(pinout.PWM2_PIN)
s3 = Servo(pinout.PWM3_PIN)

angles = [-50, 0, 50]
angles = [0, 20, 50]

while True:
    for a in angles:
        # s1.set_degree(a)
        # s2.set_degree(a)
        s3.set_degree(a)
        sleep(1)
