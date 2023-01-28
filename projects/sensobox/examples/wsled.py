from time import sleep_ms
from sensobox.wsled.shortcuts import wsled
from sensobox import colors # definice barev v /lib > RED, GREEN, BLUE, ORANGE, BLACK (nesvítí)

wsled.color(colors.RED)
sleep_ms(1000)
wsled.color(colors.GREEN)
sleep_ms(1000)
wsled.color(colors.BLUE)       # zobrazení barvy, rgb.RED/rgb.GREEN ...
sleep_ms(1000)
wsled.color(colors.BLACK)

while True:
    for i in range(255):
        wsled.color((i,i,i))
        sleep_ms(2)
    for i in range(255, 0, -1):
        wsled.color((i,i,i))
        sleep_ms(2)

wsled.color(rgb.BLACK)


