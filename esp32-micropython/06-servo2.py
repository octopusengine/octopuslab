"""
octopusLab - ROBOTboard

This is simple usage of two servo

Installation:
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./06-servo.py main.py
# reset device

"""

from machine import Pin, PWM
from time import sleep

import octopus_robot_board as o #octopusLab main library - "o" < octopus

pwm_center = int(o.SERVO_MIN + (o.SERVO_MAX-o.SERVO_MIN)/2)

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def set_degree(servo, angle):
    servo.duty(map(angle, 0,150, o.SERVO_MIN, o.SERVO_MAX))

pin_servo1 = Pin(o.PWM1_PIN, Pin.OUT)
servo1 = PWM(pin_servo1, freq=50, duty=pwm_center)
pin_servo2 = Pin(o.PWM2_PIN, Pin.OUT)
servo2 = PWM(pin_servo2, freq=50, duty=pwm_center)
sleep(1)

"""
#test servo 1
servo1.duty(o.SERVO_MIN)
sleep(1/2)
servo1.duty(o.SERVO_MAX)
sleep(1/2)

for i in range(o.SERVO_MIN,o.SERVO_MAX,2): #step 2
    servo1.duty(i)
    sleep(1/20)

servo1.duty(o.SERVO_MIN)

#test servo 2
servo2.duty(o.SERVO_MIN)
sleep(1/2)
servo2.duty(o.SERVO_MAX)
sleep(1/2)

for i in range(o.SERVO_MIN,o.SERVO_MAX,1): #step 2
    servo2.duty(i)
    sleep(1/20)

servo2.duty(o.SERVO_MIN)

ang = 90
servo1.duty(map(ang, 0,180, o.SERVO_MIN, o.SERVO_MAX))
sleep(1)
"""
pause = 1

for _ in range(3):
   set_degree(servo1,60)
   set_degree(servo2,60)
   sleep(pause)
   set_degree(servo1,120)
   set_degree(servo2,120)
   sleep(pause)
   set_degree(servo1,90)
   set_degree(servo2,45)
   sleep(pause)

set_degree(servo1,90)
set_degree(servo2,90)
