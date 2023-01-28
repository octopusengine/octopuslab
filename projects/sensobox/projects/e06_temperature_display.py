from sensobox.thermometer.shortcuts import thermometer
from sensobox.display.shortcuts import display
from time import sleep

# smycka programu
while True:
    temperature = thermometer.get_temp()
    display.show_right(temperature)
    sleep(1)
    

