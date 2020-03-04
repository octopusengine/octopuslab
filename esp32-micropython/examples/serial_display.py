# simple basic example - ESP32 + serial "Arduino" 320x240 TFT display
from machine import UART

print("ESP32 + serial display test")

uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
uart.write('C')      #test quick clear display 

uart.write('R0')     # row 0 (first)
uart.write('QoctopusLAB ESP32 test*')
uart.write('R2')     # row 2
uart.write('W3')     # color 3 (RED)
uart.write('Q  --- ok ---  *')

uart.write('W2')     # color 2 (YELLOW)
uart.write('P10.10') # one yellow point x = 100, y = 50
uart.write('h100')   # horizontal line, y = 100
uart.write('W7')     # color 7 (CYAN)
uart.write('v150')   # vertical line, x = 150

uart.write('W1')     # color 1 (WHITE)

