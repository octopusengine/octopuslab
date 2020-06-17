# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

from time import sleep
from machine import Timer
from os import urandom
import pubsub

timerCounter = 0
periodic_ms = 2000

timer = Timer(0)

def timer_init(per= 10000): # period 10 s (10000 ms)
    print("timer_init")
    print("timer is ready - periodic: "+ str(int(periodic_ms/1000)) + "s")
    print("for deactivite: tim1.deinit()")
    timer.init(period=per, mode=Timer.PERIODIC, callback=lambda t:timerAction())

def timerAction():
    global timerCounter 
    timerCounter += 1
    print("timerCounter: " + str(timerCounter)) 
    value = timerCounter
    pubsub.publish('value', value)

timer_init()

print("ok - running")








