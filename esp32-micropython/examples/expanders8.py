# 2 x pcf 8-bit expander
# exb.addr = 58 (010) buttons
# exl.addr = 62 (011) leds

from time import sleep
from util.octopus import i2c_init
from util.i2c_expander import Expander8
from util.bits import neg, reverse, int2bin, get_bit, set_bit
# int2bin(reverse(b1))   >   '10011111'

i2c = i2c_init(True,200)
# i2c.scan() > devices:
# [35, 58, 62]

exb = Expander8(58)
exl = Expander8(62)

while True:
	buttons = exb.read()

	sleep1 = False

	if(get_bit(neg(buttons),0)):
		print("0")
		sleep1 = True

	if(get_bit(neg(buttons),1)):
		print("1")
		sleep1 = True

	if(get_bit(neg(buttons),2)):
		print("2")
		sleep1 = True

	if sleep1:
		exl.write_8bit(buttons)
		sleep(0.2)

	exl.write_8bit(buttons)