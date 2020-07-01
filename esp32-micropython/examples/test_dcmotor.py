# ROBOTboard example - DC motors

from time import sleep
from util.pinout import set_pinout
pinout = set_pinout()

from util.dcmotors import Motor, Steering
motor_r = Motor(pinout.MOTOR_1A, pinout.MOTOR_2A, pinout.MOTOR_12EN)
motor_l = Motor(pinout.MOTOR_3A, pinout.MOTOR_4A, pinout.MOTOR_34EN)
steering = Steering(motor_l, motor_r)

speed = 800

steering.center(0)
steering.center(speed)
sleep(1)
steering.center(-speed)
sleep(1)
steering.right(speed/2)
sleep(1)
steering.left(speed/3)
sleep(1)
steering.center(0)
