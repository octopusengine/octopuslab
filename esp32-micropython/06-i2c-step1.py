"""
This is simple usage of SSD1306 OLED display over I2C
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

Set your SCL and SDA pins in constants

Installation:
ampy -p /dev/ttyUSB0 put ./ssd1306.py
ampy -p /COM6 put ./07-i2c-test.py main.py
# reset device

"""
from machine import Pin, I2C
import time
import os

# If you have OLED you can uncomment this and all oled lines
#import ssd1306

import octopus_robot_board as o #octopusLab main library - "o" < octopus

i2c_sda = Pin(o.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(o.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
#oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#PCF address = 35 #33-0x21/35-0x23
ADDRESS1 = 0x21
ADDRESS2 = 0x23
REG = 7


# test_whole display
#oled.fill(1)
#oled.show()

time.sleep_ms(300)

# reset display
#oled.fill(0)
#oled.show()

# write text on x, y
#oled.text('i2c scann:', 10, 10)
#oled.show()
time.sleep_ms(1000)

devices = i2c.scan()
#oled.fill(0)

#if len(devices) == 0:
#    oled.text('no i2c device', 10, 20)
#else:
#    oled.text('i2c found: '+str(len(devices)), 10, 10)
#    row = 0
#    for device in devices:
#       # print("Decimal address: ",device," | Hexa address: ",hex(device))
#       oled.text(str(row+1)+': '+str(device)+'('+str(hex(device))+')', 10, 20+row*10)
#       row =row + 1

#oled.show()
time.sleep(2)
step = dict()

step[0] = int("00010000",2)
step[1] = int("00110000",2)
step[2] = int("00100000",2)
step[3] = int("01100000",2)
step[4] = int("01000000",2)
step[5] = int("11000000",2)
step[6] = int("10000000",2)
step[7] = int("10010000",2)

tempData = bytearray(1)

try:
    while True:
      #test = ubinascii.hexlify(data[, sep])
      for i in range (0, 8):
        tempData[0] = step[i]
        i2c.writeto(ADDRESS1, tempData)
        time.sleep(1/1000)

      #oled.text('ok', 20, 50)
except Exception as e:
    print(e)
#    oled.text(str(e), 0, 50)

#oled.show()
