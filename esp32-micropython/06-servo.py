"""
octopusLab - ROBOTboard

This is simple usage of servo

Installation:
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./06-servo.py main.py
# reset device

"""

from machine import Pin, PWM
from time import sleep

import octopus_robot_board as o #octopusLab main library - "o" < octopus

pin_servo = Pin(o.PWM1_PIN, Pin.OUT)
pwm = PWM(pin_servo, freq=50, duty=70)
# duty for servo is between 40 - 115

SERVO_MIN = 40
SERVO_MAX= 120

pwm.duty(SERVO_MAX)
sleep(1)
pwm.duty(SERVO_MIN)
sleep(1)

for i in range(SERVO_MIN,SERVO_MAX,2): #step 2
    pwm.duty(i)
    sleep(1/10)

pwm.duty(SERVO_MIN)
