"""
octopusLab - ROBOTboard
Test PCF8574 - i2c 8bit expander
This is simple usage of SSD1306 OLED display over I2C
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

Installation:
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./ssd1306.py
ampy -p /COM6 put ./07-i2c-test.py main.py
# reset device

"""
import machine
import ssd1306
import time
import os

import octopus_robot_board as o #octopusLab main library - "o" < octopus

i2c = machine.I2C(-1, machine.Pin(o.I2C_SCL_PIN), machine.Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#address = 35 #33-0x21/35-0x23
addr = 0x23
REG = 7

oled.fill(0) # reset display
# write text on x, y
oled.text('i2c test:', 20, 20)
oled.show()

i2c.scan()

try:
    i2c.writeto(addr, b'123')
    #i2c.mem_write(b"\x01", ADDRESS, REG)
    oled.text('ok', 20, 50)
except Exception as e:
    oled.text(str(e), 0, 50)

oled.show()
