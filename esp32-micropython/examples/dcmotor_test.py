# octopusLAB simple example

from machine import Pin, PWM
from time import sleep
from util.pinout import set_pinout
pinout = set_pinout()

#from motor import *
#moto_run(300) ## 300-1000

moto_L1 = Pin(pinout.MOTOR_1A, Pin.OUT)
moto_L2 = Pin(pinout.MOTOR_2A, Pin.OUT)
moto_L  = PWM(Pin(pinout.MOTOR_12EN, Pin.OUT), freq=500, duty = 0)

MOTO_R_Correction = 45
moto_R3 = Pin(pinout.MOTOR_3A, Pin.OUT)
moto_R4 = Pin(pinout.MOTOR_4A, Pin.OUT)
moto_R  = PWM(Pin(pinout.MOTOR_34EN, Pin.OUT), freq=500, duty = 0)


def moto_stop():
    motors(0, 0)


def moto_run(speed, forward=True):
    motors(speed, speed, forward)


def motors(speedL, speedR, forward=True):
    moto_L1.value(forward)
    moto_L2.value(not forward)
    moto_L.duty(speedL)

    moto_R3.value(not forward)
    moto_R4.value(forward)
    moto_R.duty(speedR)



moto_run(300)
sleep(2)
moto_run(600)
sleep(3)
moto_run(900)
sleep(5)
moto_stop()


