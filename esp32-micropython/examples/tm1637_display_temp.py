from time import sleep_ms

from machine import Pin
import tm1637

# 4 digits display - dot is treated as middle digit
tm = tm1637.TM1637Decimal(clk=Pin(22), dio=Pin(21))
tm.show(" .   ")
sleep_ms(100)
tm.show("  .  ")
sleep_ms(100)
tm.show("   . ")
sleep_ms(100)
tm.show("    .")
sleep_ms(100)
tm.show("    ")

sleep_ms(200)

temp = -36.40
# write temperature on most right postition on the display
disp_list = [" ", " ", " ", " ", " "]
str_temp = str(temp)[0:5] # trim in case of more than 5 chars (one for decimal point)
# use negative index to access characters from the last
for i in range(1, len(str_temp)+1):
    disp_list[-i] = str_temp[-i]

tm.show("".join(disp_list))

