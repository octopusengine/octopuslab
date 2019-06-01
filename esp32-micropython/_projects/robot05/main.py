import machine, time
from time import sleep, ticks_ms, sleep_ms
from machine import Pin, Timer, PWM, SPI
from neopixel import NeoPixel
from hcsr04 import HCSR04

#from util.wifi_connect import read_wifi_config, WiFiConnect
#from util.mqtt_connect import read_mqtt_config
#from util.octopus_lib import *
#from umqtt.simple import MQTTClient

import gc

from util.pinout import set_pinout
pinout = set_pinout()

# Settings

DEBUG = True
BTN_Debounce   = 50  # How many reads
BTN_Tresh      = 40  # How many reads must be 1 to return pressed

ECHO_Treshold  =  7  # How many centimeters (and less) to stop
WS_Brightness  = 40

MOTO_R_Correction = 45

# Pin definitions

# IR
ir_L = Pin(39, Pin.IN)
ir_R = Pin(34, Pin.IN)

# Motors
moto_L1 = Pin(pinout.MOTOR_1A, Pin.OUT)
moto_L2 = Pin(pinout.MOTOR_2A, Pin.OUT)
moto_L  = PWM(Pin(pinout.MOTOR_12EN, Pin.OUT), freq=500, duty = 0)

moto_R3 = Pin(pinout.MOTOR_3A, Pin.OUT)
moto_R4 = Pin(pinout.MOTOR_4A, Pin.OUT)
moto_R  = PWM(Pin(pinout.MOTOR_34EN, Pin.OUT), freq=500, duty = 0)

# Button settings
button = Pin(35, Pin.IN)

# Echo module
echo = HCSR04(trigger_pin=pinout.DEV1_PIN, echo_pin=pinout.DEV2_PIN)

# WS Led
pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
np = NeoPixel(pin_ws, 1)
ws_r = 0
ws_g = 0
ws_b = 0


def debug(msg):
    if DEBUG:
        print("DEBUG: " + msg)

def readDebouncePin(pin):
    debounce = 0

    for _ in range(BTN_Debounce):
        debounce += pin.value()
        sleep_ms(1)

    debug("Debounce value: {0}".format(debounce))
    return debounce > BTN_Tresh


def moto_stop():
    motors(0, 0)


def moto_run(speed, forward=True):
    motors(speed, speed, forward)

def motors(speedL, speedR, forward=True):
    moto_L1.value(forward)
    moto_L2.value(not forward)

    moto_R3.value(not forward)
    moto_R4.value(forward)

    moto_L.duty(speedL)

    if speedR > MOTO_R_Correction:
        moto_R.duty(speedR - MOTO_R_Correction)
    else:
        moto_R.duty(0)

# Boot up robot

np[0] = (0, 0, WS_Brightness)
np.write()

def waitButton(state):
    while not readDebouncePin(button) == state:
        sleep_ms(1)
    
    return state

waitButton(False)

motoRun = False
while True:
    val = not readDebouncePin(button)
    ir_left  = not readDebouncePin(ir_L)
    ir_right = not readDebouncePin(ir_R)


    debug("Button: {0}".format(val))
    debug("Running: {0}".format(motoRun))
    debug("Left: {0}".format(ir_left))
    debug("Right: {0}".format(ir_right))

    if val:
        waitButton(True)
        motoRun = not motoRun

        if not motoRun:
            np[0] = (WS_Brightness, 0, 0)
            np.write()

    echo_cm = echo.distance_cm()

    if echo_cm < ECHO_Treshold and echo_cm > 2 and motoRun:
        debug("Distance less than threshols {0}. Stopping motors!".format(ECHO_Treshold))
        motoRun = False
        np[0] = (WS_Brightness, WS_Brightness, 0)
        np.write()


    if (ir_left or ir_right) and motoRun:
        debug("IR stop")
        motoRun = False
        np[0] = (WS_Brightness, 0, WS_Brightness)
        np.write()

    if motoRun:
        np[0] = (0, WS_Brightness, 0)
        np.write()

        moto_run(450)
    else:
        moto_stop()
