# --- octopusLAB simple basic example ---
# ESP32 + Displays expander BOARD 2021/10
# 7segment display + 4x4 keypad


import time
from gc import mem_free
from machine import Pin, UART, I2C
from utils.pinout import set_pinout
from utils.octopus import disp7_init
from components.i2c_keypad import Keypad16

print("--- RAM free ---> " + str(mem_free())) 
pinout = set_pinout()

print("7segment display + 4x4 keypad")
KP_ADDRESS = 0x20 
KP_DELAY = 250

d7 = disp7_init()
i2c = I2C(0, scl=Pin(pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=100000)
kp = Keypad16(i2c, KP_ADDRESS, False)

lastKeyPress = 0
keyDelay = KP_DELAY
displayNum = ""


while True:
    try:
        key = kp.getKey()
    except OSError as e:
        print("Error while get key")
        print(e)
        key = None

    if key and time.ticks_ms() > lastKeyPress+keyDelay:
        lastKeyPress = time.ticks_ms()
        print(key)
        # ToDo action for "*"
        if key == '#': # Enter
            print("final number: ", displayNum)
        else:    
           displayNum += str(key)
           d7.show((8-len(displayNum))*" " + displayNum)

        if key == 'C': # Clear
           displayNum = ""
           d7.show(displayNum)
