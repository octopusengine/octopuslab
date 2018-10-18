from machine import Pin
from time import sleep

pin_diody = Pin(2, Pin.OUT)
while True:
    pin_diody.value(0)
    sleep(1/2)
    pin_diody.value(1)
    sleep(1/2)