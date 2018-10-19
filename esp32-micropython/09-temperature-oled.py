"""
This example usage of DS18B20 "Dallas" temperature sensor and SSD1306 OLED display
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
needs external module temperature.py from ??

Set your SCL and SDA pins in constants
Set your sensor pin number in constants

Installation:
ampy -p /dev/ttyUSB0 put ./ssd1306.py
ampy -p /dev/ttyUSB0 put ./temperature.py
ampy -p /dev/ttyUSB0 put ./09-temperature-oled.py main.py
# reset device
"""

import machine
import ssd1306
import time

from temperature import TemperatureSensor

ONE_WIRE_PIN = 32
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

ts = TemperatureSensor(ONE_WIRE_PIN)

i2c = machine.I2C(-1, machine.Pin(I2C_SCL_PIN), machine.Pin(I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()

time.sleep_ms(300)

# reset display
oled.fill(0)
oled.show()

while True:
    temp = ts.read_temp()
    # print to console
    print(temp)
    # print on display
    oled.fill(0) # reset display
    oled.text('T = %.1f C' % temp, 25, 20)
    oled.show()
    time.sleep_ms(500)
