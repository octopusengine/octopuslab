from time import sleep
from sensobox.ultrasonic.shortcuts import ultrasonic
from sensobox.display.shortcuts import display

while True:
    distance = ultrasonic.distance_cm()
    print(distance)
    display.show_right(distance)
    sleep(1)

