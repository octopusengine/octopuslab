# library for ws rgb neopisel led - single / strip / ring
# octopusLAB 2019
from time import sleep
from neopixel import NeoPixel

# WS neopixel:
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0) # = off

def setupNeopixel(pin,num):
   np = NeoPixel(pin, num)
   return np

def simpleRgb(np):
    np[0] = RED #R
    np.write()
    sleep(1)

    np[0] = GREEN #G
    np.write()
    sleep(1)

    np[0] = BLUE #B
    np.write()
    sleep(1)

    np[0] = (0, 0, 0)
    np.write()   

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def color_chase(np, num_pixels, color, wait):
    for i in range(num_pixels):
        np[i] = color
        np.write()
        sleep(wait)

def rainbow_cycle(np, num_pixels,wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            np[i] = wheel(rc_index & 255)
        np.write()

def neopixelTest(np, num_pixels):
        #https://github.com/maxking/micropython/blob/master/rainbow.py
        np.fill(RED)
        np.write()
        # Increase or decrease to change the speed of the solid color change.
        sleep(1)
        np.fill(GREEN)
        np.write()
        sleep(1)
        np.fill(BLUE)
        np.write()
        sleep(1)

        color_chase(np, num_pixels,RED, 0.1)  # Increase the number to slow down the color chase
        color_chase(np, num_pixels,YELLOW, 0.1)
        color_chase(np, num_pixels,GREEN, 0.1)
        color_chase(np, num_pixels,CYAN, 0.1)
        color_chase(np, num_pixels,BLUE, 0.1)
        color_chase(np, num_pixels,PURPLE, 0.1)

        rainbow_cycle(np, num_pixels,2)  # Increase the number to slow down the rainbow
        sleep(1)

        np.fill(BLACK)
        np.write()