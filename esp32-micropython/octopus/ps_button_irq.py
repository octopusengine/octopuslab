# octopusLAB simple example
# HW: ESP32board + button 0 (boot) interupt
# import octopus.ps_button_irq

from machine import Pin
import pubsub

counter=0

@pubsub.publisher("btn_value")
def irq_handler(v):
    global counter
    counter += 1
    print("IRQ ", counter)

    return counter
 

button0 = Pin(0, Pin.IN) # default BOOT btn
button0.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

# while True:
#    pass
