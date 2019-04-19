"""
This is simple usage of HD44780 LCD display over I2C
Connect to wifi using config
either deploy config/wifi.json or use setup() in REPL to create one

Uses library from https://github.com/dhylands/python_lcd
Namely esp8266_i2c_lcd and lcd_api

TODO make wifi connection non blocking
- if wrong credentials are provided, REPL will not start (long timeout)
  it's hard to re-run setup() to fix credentials

Installation:
ampy -p /dev/ttyUSB0 put ./config
ampy -p /dev/ttyUSB0 put ./lib
ampy -p /dev/ttyUSB0 put ./util
ampy -p /dev/ttyUSB0 put ./05-oled.py main.py
# reset device

"""
import machine
import time
import ujson
from lib.esp8266_i2c_lcd import I2cLcd
LCD_ADDRESS=0x27
LCD_ROWS=2
LCD_COLS=16

i2c = machine.I2C(-1, machine.Pin(22), machine.Pin(21), freq=100000) # 100kHz, because of PCF
lcd = I2cLcd(i2c, LCD_ADDRESS, LCD_ROWS, LCD_COLS)

# test_whole display
lcd.clear()

# write text on x, y
lcd.putstr('LCD OctopusLAB')
time.sleep_ms(1000)

counter = 0
while True:
    lcd.move_to(0, LCD_ROWS-1)
    lcd.putstr("Count: {0}".format(counter))
    counter+=1
    time.sleep(1)
