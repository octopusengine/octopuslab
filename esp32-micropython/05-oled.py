"""
This is simple usage of SSD1306 OLED display over I2C
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

Set your SCL and SDA pins in constants

Installation:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
ampy -p /dev/ttyUSB0 put ./ssd1306.py
ampy -p /dev/ttyUSB0 put ./05-oled.py main.py
# reset device

"""
import machine
import ssd1306
import time

import octopus_robot_board as o #octopusLab main library - "o" < octopus

i2c = machine.I2C(-1, machine.Pin(o.I2C_SCL_PIN), machine.Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()

time.sleep_ms(300)

# reset display
oled.fill(0)
oled.show()

# write text on x, y
oled.text('OLED test', 20, 20)
oled.show()
time.sleep_ms(2000)

for i in range(1,10+1):
   oled.fill(0)
   oled.text('OctopusLab', 20, 15)
   oled.text(" --- "+str(10-i)+" ---", 20, 35)
   oled.show()
   time.sleep_ms(1000)
