# ROBOTboard example - DC motors

from time import sleep
from util.pinout import set_pinout
pinout = set_pinout()

from util.dcmotors import Motor, Steering
motor_r = Motor(pinout.MOTOR_1A, pinout.MOTOR_2A, pinout.MOTOR_12EN)
motor_l = Motor(pinout.MOTOR_3A, pinout.MOTOR_4A, pinout.MOTOR_34EN)
steering = Steering(motor_l, motor_r)

# _ARGS
# ToDo parse: speed=800,pin=25
speed = 800
try:
    speed = (int(_ARGS[0]))
    print("speed  = ", str(speed ))
except Exception as e:
    print("Exception: {0}".format(e))


steering.center(0)
steering.center(speed)
sleep(1)
steering.center(-speed)
sleep(1)
steering.center(0)

