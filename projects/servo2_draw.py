# servo laser pointer - example

from time import sleep_ms
from utils.transform import *

from components.servo import Servo
# todo: PWM double setup error

s1 = Servo(17)
s2 = Servo(16)

dist = 100 # distance and size of board
delay = 5


def move_servo2(p1, p2, delay = delay):
    steps = move_2d_line(p1, p2)
    for step in steps:
        alfa = cosangle(step[0], dist, dist)[0]
        beta = cosangle(step[1], dist, dist)[0]
        print(step, alfa, beta)

        s1.set_degree(alfa)
        s2.set_degree(beta)
        sleep_ms(delay)


def run_test():
    p1 = 0, 0 # strart point
    p2 = 50, 50 # stop point
    move_servo2(p1, p2)

    p1 = 50, 50
    p2 = 0, 0
    move_servo2(p1, p2)

    move_servo2((0,0),(0,100))
    move_servo2((0,100),(100,100))
    move_servo2((100,100),(100,0))
    move_servo2((100,0),(0,0))

run_test()
