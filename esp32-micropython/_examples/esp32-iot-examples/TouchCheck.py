from machine import Pin,TouchPad
from time import sleep
t1 = TouchPad(Pin(4))
t2 = TouchPad(Pin(33))

def assignPins(pin1, pin2)
    t1 = TouchPad(Pin(pin1))
    t2 = TouchPad(Pin(pin2))
    
def readButton(threshold, delay):
    b1 = 0.0
    b2 = 0.0

    while True:
        if t1.read() < threshold: 
            b1 = b1 + delay
        elif b1 != 0.0:
            print("Pin A pressed for %f" % b1)
            b1 = 0.0
        
        if t2.read() < threshold: 
            b2 += delay
        elif b2 != 0.0:
            print("Pin B pressed for %f" % b2)
            b2 = 0.0
            
        sleep(delay)
