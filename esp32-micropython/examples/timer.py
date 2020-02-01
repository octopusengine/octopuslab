# octopusLAB simple example
# run: import examples.timer

print("timer - example")

from time import sleep
from machine import Timer
timerCounter = 0
tim1 = Timer(0)

def timer_init(per= 10000): # period 10 s (10000 ms)
    print("timer_init")
    print("timer tim1 is ready - periodic - 10s")
    print("for deactivite: tim1.deinit()")
    tim1.init(period=per, mode=Timer.PERIODIC, callback=lambda t:timerAction())

def timerAction():
    global timerCounter 
    print("timerAction " + str(timerCounter))
    timerCounter += 1
    print("timerCounter: " + str(timerCounter)) 

timer_init()

while True:
   # another code
   sleep(1)
    

