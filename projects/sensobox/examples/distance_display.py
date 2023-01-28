from time import sleep
from sensobox.display.shortcuts import display
from sensobox.ultrasonic.shortcuts import ultrasonic

print("---ulrasonic distance sensor---")

while True:
    cm = ultrasonic.distance_cm()
    cm = str(cm)
    display.show(cm)
    sleep(1)

