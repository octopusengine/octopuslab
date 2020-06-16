# octopusLAB simple example
# HW: ESP32board + burtton 0 (boot) interupt

from machine import Pin
import pubsub

counter=0

@pubsub.publisher("value")
def irq_handler(v):
    global counter
    counter += 1
    print("IRQ ", counter)

    return counter
 

button0 = Pin(0, Pin.IN)
button0.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

while True:
    pass