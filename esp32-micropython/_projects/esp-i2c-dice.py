"""
This is simple usage of PFC8574 I2C expander
Set your expander address

ampy -p /COM6 put 06-i2c-dice.py main.py
"""
from micropython import const
from machine import Pin, I2C
import time
import urandom

from util.pinout import set_pinout
pinout = set_pinout()

#PCF address = 35 #33-0x21/35-0x23
ADDRESS = 0x20 #0x20(000) 0x23(100)
# motor id 1 or 2
MOTOR_ID = 1
i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(

dice = (
const(0b11101111),
const(0b11100111), #1
const(0b01101011), #2-
const(0b01100011), #3-
const(0b01011010), #4
const(0b01000010), #5
const(0b00011000)  #6
)

tempData = bytearray(1)

print("start dice")

while True:
    tempData[0] = dice[0]
    i2c.writeto(ADDRESS, tempData)
    time.sleep_ms(2000)

    for i in range(7):
      print(str(i)+": "+str(dice[i]))
      tempData[0] = dice[i]
      #i2c.writeto(ADDRESS, bytearray([b0]))
      i2c.writeto(ADDRESS, tempData)
      time.sleep_ms(200)
          
    ir = urandom.randint(1, 6)
    print("R: "+str(dice[ir]))
    tempData[0] = dice[ir]
    i2c.writeto(ADDRESS, tempData)
    time.sleep_ms(3000)
