from hcsr04 import HCSR04
from time import sleep_ms

sensor = HCSR04(trigger_pin=19, echo_pin=18)


while True:
    print(sensor.distance_cm())
    sleep_ms(50)
