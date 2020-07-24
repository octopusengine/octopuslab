# octopusLAB simple example
# HW: ESP32board + burtton 0 (boot) interupt

from utils.octopus import led
from machine import Pin

counter=0

def irq_handler(v):
    global value, counter
    counter += 1
    print("IRQ ", counter)
    #led.toggle()

    led.value(value)
    if(value == 0):
        value = 1
    else:
        value = 0

value = 0

button0 = Pin(0, Pin.IN)
button0.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

while True:
    pass