"""
This is simple usage of 28BYJ-48 step motor on ULN2803 driver via PFC8574 I2C expander
Set your expander address and motor id in constants
"""
from machine import Pin, I2C
from lib.sm28byj48 import SM28BYJ48

from utils.pinout import set_pinout
pinout = set_pinout()

#PCF address = 33 #33-0x21/35-0x23
ADDRESS = 0x21
# motor id 1 or 2
MOTOR_ID1 = 1
MOTOR_ID2 = 2

i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
motor1 = SM28BYJ48(i2c, ADDRESS, MOTOR_ID1)

while True:

   # turn right 180 deg
   motor1.turn_degree(90*2)

   # turn left 180 deg
   motor1.turn_degree(90*2, 1)
