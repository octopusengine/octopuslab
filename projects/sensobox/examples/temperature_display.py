from sensobox.thermometer.shortcuts import thermometer
from sensobox.display.shortcuts import display
from time import sleep

print("---thermometer---")

# smycka programu
while True:
    temp  = thermometer.get_temp()
    print("Temperature {}".format(temp))

    display.show_right(temp)

    sleep(1)

