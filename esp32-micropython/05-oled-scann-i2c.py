"""
octopusLAB - I2C devices scanner:
This is simple usage of SSD1306 OLED display over I2C
needs external driver ssd1306.py
from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
Installation:
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./ssd1306.py
ampy -p /COM6 put ./05-oled-scann-i2c.py main.py
# reset device
"""

from machine import Pin, I2C
import ssd1306
import time
import os

import octopus_robot_board as o #octopusLab main library - "o" < octopus

i2c_sda = Pin(o.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(o.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#address = 35 #33-0x21/35-0x23
ADDRESS = 0x23
REG = 7

# reset display
oled.fill(0)
oled.show()

# write text on x, y
oled.text('i2c scann:', 10, 10)
oled.show()
time.sleep_ms(1000)

devices = i2c.scan()
oled.fill(0)

row = 0
if len(devices) == 0:
    oled.text('no i2c device', 10, 20)
else:
    oled.text('i2c found: '+str(len(devices)), 10, 10)
    for device in devices:
       # print("Decimal address: ",device," | Hexa address: ",hex(device))
       oled.text(str(row+1)+': '+str(device)+'('+str(hex(device))+')', 10, 20+row*10)
       row =row + 1
oled.text('octopusLab 2018', 5, 20+row*10+5)
oled.show()

"""
try:
    i2c.writeto(ADDRESS, REG, stop=False)
    #i2c.mem_write(b"\x01", ADDRESS, REG)
    oled.text('ok', 20, 50)
except Exception:
    oled.text('---Err?---', 20, 50)
oled.show()
"""
