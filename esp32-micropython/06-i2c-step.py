"""
This is simple usage of 28BYJ-48 step motor on ULN2803 driver via PFC8574 I2C expander

Set your expander address and motor id in constants

Installation:
ampy -p /dev/ttyUSB0 put ./sm28byj48.py
ampy -p /COM6 put ./06-i2c-step.py main.py
# reset device

"""
from machine import Pin, I2C
from lib.sm28byj48 import SM28BYJ48

import octopus_robot_board as o #octopusLab main library - "o" < octopus

#PCF address = 35 #33-0x21/35-0x23
ADDRESS = 0x23
# motor id 1 or 2
MOTOR_ID = 1

i2c_sda = Pin(o.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(o.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
motor1 = SM28BYJ48(i2c, ADDRESS, MOTOR_ID)

# turn right 90 deg
motor1.turn_degree(90)
# turn left 90 deg
motor1.turn_degree(90, 1)
