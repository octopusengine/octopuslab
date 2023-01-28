from sensobox.thermometer import instance as thermometer
from time import sleep
from sensobox.display import instance as display

# smycka programu
while True:
    temperature = thermometer.get_temp()
    print("Temperature {}".format(temperature))

    display.show_right(temperature)

    sleep(1)
