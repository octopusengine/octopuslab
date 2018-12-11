from machine import Pin,TouchPad
from time import sleep

t1 = TouchPad(Pin(12))
t2 = TouchPad(Pin(13))

def readButton(threshold):
    b1 = t1.read()
    b2 = t2.read()
    print("Buttons (RAW: {0}, {1}): {2}\t{3}".format(b1, b2, "B1" if b1 < threshold else " ", "B2" if b2 < threshold else " "))

while True:
    readButton(100)
    sleep(0.2)
