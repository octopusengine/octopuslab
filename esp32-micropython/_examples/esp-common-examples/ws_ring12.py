# ampy -p /COM5 put ws12.py main.py

import time
from machine import Pin

from util.pinout import set_pinout
pinout = set_pinout()

print("ws12 - test")

def neo_init(num_led):
    from neopixel import NeoPixel
    pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
    npObj = NeoPixel(pin, num_led)
    return npObj

n = 12
np = neo_init(n)

def wheel(pos):
     if(pos < 85):
         col = [pos*3, 255-pos*3,0]
     elif(pos < 170):
       pos = pos -85;
       col = [255-pos*3, 0, pos*3]
     else:
       pos = pos - 170
       col = [0,pos*3,255-pos*3]
     return col

def rainbow():
    for j in range(256):
        for i in range(n):
            np[i] = wheel(i*1+j) # & 255
            np.write()
            time.sleep_ms(5)

def cycle():
    for i in range(6 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (32, 32, 0)
        np.write()
        time.sleep_ms(50)

def fade():
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

def bounce():
    for i in range(5 * n):
        for j in range(n):
            np[j] = (0, 0, 8)
        if (i // n) % 2 == 0:
            np[i % n] = (128, 0, 200)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(50)

def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

while True:
    print("cycle")
    cycle()
    time.sleep_ms(1000)

    print("rainbow")
    rainbow()
    time.sleep_ms(1000)

    print("fade")
    fade()
    time.sleep_ms(1000)

    print("bounce")
    bounce()
    time.sleep_ms(1000)

    print("clear")
    clear()
    time.sleep_ms(2000)
