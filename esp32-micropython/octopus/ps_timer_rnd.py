# octopusLAB pub sub module for pubsub
# usage:
# import octopus.ps_timer_rnd

from time import sleep
from machine import Timer
from os import urandom
import pubsub


tim0 = Timer(0)
timCounter = 0


def timer_init(per= 10000):      # period 10 s 10000 ms (1s/1000)
    print("--- timer_init ---")  # for deactivate: tim0.deinit()
    tim0.init(period=per, mode=Timer.PERIODIC, callback=lambda t:timerAction())


def timerAction():
    global timCounter 
    value =  int(urandom(1)[0])
    print(str(timCounter) + " rnd: ", value)
    pubsub.publish('d7_text', value)
    timCounter += 1


sleep(3)
timer_init()
print("---/---")
