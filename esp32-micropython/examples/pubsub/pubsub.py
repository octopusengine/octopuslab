# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo
# octopusLAB pubsub example


from pubsub import PubSub

pubsub = PubSub()

#######################################################################################
from machine import Pin


def irq_handler(pin):
    pubsub.publish('button', pin)


button_0 = Pin(0, Pin.IN)
button_0.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

#######################################################################################
from machine import Timer

tim = Timer(-1)
tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t: pubsub.publish('timer'))


#######################################################################################
class Counter:
    def __init__(self):
        self.value = 0

    def on_button(self, pin):
        self.value += 1
        pubsub.publish('counter', self.value)

    def on_timer(self):
        self.value += 100
        pubsub.publish('counter', self.value)


counter = Counter()

pubsub.subscribe('button', counter.on_button)
pubsub.subscribe('timer', counter.on_timer)

#######################################################################################
from util.octopus import disp7_init

d7 = disp7_init()  # 8 x 7segment display init


def display_num(value):
    d7.show(value)


pubsub.subscribe('counter', display_num)
