# simple basic example - ESP32 + serial "Arduino" 320x240 TFT display
from machine import UART

uart = UART(2, 115200) #UART2 > #U2TXD(SERVO1/PWM1_PIN)

comm = "C"
try:
    comm = (_ARGS[0])
    print("comm   = ", str(comm))
except Exception as e:
    print("Exception: {0}".format(e))

uart.write(comm)      



