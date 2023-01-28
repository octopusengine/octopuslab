from time import sleep_ms
from sensobox.wsled.shortcuts import wsled
from sensobox import colors

wsled.color(colors.WHITE) # the same as ws.color((255, 255, 255))
sleep_ms(15)
wsled.color(colors.BLACK)

