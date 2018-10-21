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
pwm.duty(150)
sleep(1)
pwm.duty(30)
sleep(1)

for i in range(30,150,2): #step 2
    pwm.duty(i)
    sleep(1/10)

pwm.duty(30)
