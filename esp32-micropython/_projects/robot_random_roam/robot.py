from machine import Pin, Timer, PWM, SPI
from util.pinout import set_pinout
from time import sleep_ms
from random import randrange
from hcsr04 import HCSR04

pinout = set_pinout()

MAX_SPEED = 800
CRUISING_SPEED = 450
APPROACH_SPEED = 350
TURN_SPEED = 450
RANDOM_TURN_MIN = 600  # ms
RANDOM_TURN_MAX = 1000  # ms
COLLISION_THRESHOLD = 30  # cm
APPROACH_THRESHOLD = 100 #cm
MAX_SPEED_THRESHOLD = 250 #cm
LR_COMPENSATION = +10  # %, -10 slows L motor comared to R
ULTRASONIC_SAMPLING = 1000  # ms, how often detect obstacle

moto_L1 = Pin(pinout.MOTOR_1A, Pin.OUT)
moto_L2 = Pin(pinout.MOTOR_2A, Pin.OUT)
moto_L  = PWM(Pin(pinout.MOTOR_12EN, Pin.OUT), freq=500, duty = 0)


moto_R3 = Pin(pinout.MOTOR_3A, Pin.OUT)
moto_R4 = Pin(pinout.MOTOR_4A, Pin.OUT)
moto_R  = PWM(Pin(pinout.MOTOR_34EN, Pin.OUT), freq=500, duty = 0)

echo = HCSR04(trigger_pin=pinout.PWM2_PIN, echo_pin=pinout.PWM1_PIN)


def compensate_speed_left(speed):
    return speed + int(speed/100 * LR_COMPENSATION/2)

def compensate_speed_right(speed):
    return speed - int(speed/100 * LR_COMPENSATION/2)

def forward(speed):
    moto_L1.value(0)
    moto_L2.value(1)

    moto_R3.value(0)
    moto_R4.value(1)

    moto_L.duty(compensate_speed_left(speed))
    moto_R.duty(compensate_speed_right(speed))

def stop():
    moto_L.duty(0)
    moto_R.duty(0)


def turn_left(ms):
    moto_L1.value(1)
    moto_L2.value(0)

    moto_R3.value(0)
    moto_R4.value(1)

    moto_L.duty(compensate_speed_left(TURN_SPEED))
    moto_R.duty(compensate_speed_right(TURN_SPEED))
    sleep_ms(ms)
    stop()


def turn_right(ms):
    moto_L1.value(0)
    moto_L2.value(1)

    moto_R3.value(1)
    moto_R4.value(0)

    moto_L.duty(compensate_speed_left(TURN_SPEED))
    moto_R.duty(compensate_speed_right(TURN_SPEED))
    sleep_ms(ms)
    stop()

def random_turn():
    if randrange(2):
        print('TURN LEFT')
        turn_left(randrange(RANDOM_TURN_MIN, RANDOM_TURN_MAX))
    else:
        print('TURN RIGHT')
        turn_right(randrange(RANDOM_TURN_MIN, RANDOM_TURN_MAX))


def start():
    while True:
        stop()
        distance = echo.distance_cm()
        if distance < 0 or distance > MAX_SPEED_THRESHOLD:
            print('MAX_SPEED')
            forward(MAX_SPEED)
        elif distance > APPROACH_THRESHOLD:
            print('CRUISING')
            forward(CRUISING_SPEED)
        elif distance > COLLISION_THRESHOLD:
            print('APPROACH')
            forward(APPROACH_SPEED)
        else:  # distance < COLLISION_THRESHOLD
            stop()
            random_turn()
        sleep_ms(ULTRASONIC_SAMPLING)
