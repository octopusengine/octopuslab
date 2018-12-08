"""
This example usage of DS18B20 "Dallas" temperature sensor and SSD1306 OLED display
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
needs external module temperature.py from https://boneskull.com/micropython-on-esp32-part-1/

Set your sensor pin number in constants

Installation:
lib/ssd1306.py
lib/temperature.py
ampy -p /dev/ttyUSB0 put ./09-temperature-oled.py main.py
# reset device
"""

import machine
import time
from lib import ssd1306
from lib.temperature import TemperatureSensor
import octopus_robot_board as o # octopus ROBOTboard pinout

ts = TemperatureSensor(o.ONE_WIRE_PIN)

i2c = machine.I2C(-1, machine.Pin(o.I2C_SCL_PIN), machine.Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()
time.sleep_ms(300)

oled.fill(0) # reset display
oled.show()

while True:
    temp = ts.read_temp()
    # print to console
    print(temp)
    # print on display
    oled.fill(0) # reset display
    oled.text('octopus LAB', 20, 20)
    oled.text('Temp: %.1f C' % temp, 20, 35)
    oled.show()
    time.sleep_ms(1000)
