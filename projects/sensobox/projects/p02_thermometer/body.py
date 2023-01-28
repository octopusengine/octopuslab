from time import sleep_ms
from sensobox.wsled import instance as ws
from sensobox.thermometer import instance as thermometer
from sensobox.display import instance as display
import colors_rgb as rgb # definice barev v /lib > RED, GREEN, BLUE, ORANGE, BLACK (nesvítí)

# the loop which constantly checks if the light needs to be changed
while True:
    temperature = thermometer.get_temp()
    display.show_right(temperature)
    if temperature < 35.5:
        ws.color((0, 0, 100))
    elif temperature < 37.5:
        ws.color((0, 100, 0))
    else:
        ws.color((100, 0, 0))
	sleep_ms(1)
