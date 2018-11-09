"""
This is simple usage of SSD1306 OLED display over I2C
needs external driver ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

analog value: an/maxbit*maxv

Installation:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
ampy -p /dev/ttyUSB0 put ./ssd1306.py
ampy -p /dev/ttyUSB0 put ./05-oled.py main.py
# reset device

"""
import machine
from machine import Pin
import ssd1306
import time

import octopus_robot_board as o #octopusLab main library - "o" < octopus

pin_an = Pin(o.PIN_ANALOG, Pin.IN)
adc = machine.ADC(pin_an)

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

while True:
   oled.fill(0)
   oled.text('OctopusLab', 20, 15)
   an = adc.read()
   oled.text("RAW: {0}".format(an), 20, 30)
   # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
   oled.text("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)
   oled.show()
   time.sleep_ms(1000)
