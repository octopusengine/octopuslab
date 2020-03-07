# basic library for class Analog input 
# octopusLAB 2019

"""
# ROBOTboard example
 
from util.pinout import set_pinout
pinout = set_pinout()

from util.dcmotors import Motor, Steering
motor_r = Motor(pinout.MOTOR_1A, pinout.MOTOR_2A, pinout.MOTOR_12EN)
motor_l = Motor(pinout.MOTOR_3A, pinout.MOTOR_4A, pinout.MOTOR_34EN)

steering = Steering(motor_l, motor_r)
speed = 800

steering.center(0)
steering.center(-speed)
steering.right(speed)
steering.left(speed) 
"""

from machine import PWM, Pin


class Motor:
    def __init__(self, pin_1, pin_2, pin_3):
        # TODO add corrections
        self._pin_1 = Pin(pin_1, Pin.OUT)
        self._pin_2 = Pin(pin_2, Pin.OUT)
        self._pin_3_pwm = PWM(Pin(pin_3, Pin.OUT), freq=500, duty=0)

    def speed(self, value):
        forward = value >= 0
        self._pin_1.value(forward)
        self._pin_2.value(not forward)
        self._pin_3_pwm.duty(abs(value))



# TODO add steering which achieve speed (for real transport, for example racing cars)

class Steering:
    '''
    Very simple steering
    '''
    def __init__(self, motor_l, motor_r):
        self.motor_l = motor_l
        self.motor_r = motor_r

    def left(self, value):
        self.motor_l.speed(0)
        self.motor_r.speed(value)

    def right(self, value):
        self.motor_r.speed(0)
        self.motor_l.speed(value)

    def center(self, value):
        self.motor_l.speed(value)
        self.motor_r.speed(value)