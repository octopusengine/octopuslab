# https://github.com/dhylands/python_lcd

import assets.lcd_chars as ch

from util.octopus import lcd2_init
lcd = lcd2_init()

lcd.custom_char(0, ch.happy)
lcd.putchar(chr(0))

lcd.custom_char(1, ch.clock)
lcd.putchar(chr(1))
