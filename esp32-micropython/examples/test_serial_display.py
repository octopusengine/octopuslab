# The MIT License (MIT)
# Copyright (c) 2021 Jan Copak
# octopusLAB pubsub example

# from examples.pubsub.ps_init import pubsub
from time import sleep
from machine import UART
from utils.octopus_lib import octopusASCII

print("ESP32 + serial display test")

# init
uart = UART(2, 115200) #UART2 > #U2TXD(SERVO1/PWM1_PIN) #  9600/115200

def show_text(text, row):
    uart.write('R')
    uart.write(str(row))
    sleep(0.03)
    uart.write('Q')
    uart.write(text)
    uart.write('*')
    sleep(0.05)

uart.write('C')  # test quick clear display 
uart.write('G0') # setrotation (default 1)
uart.write('W1') # setcolor white
# 01234 BLACK,WHITE,YELLOW,RED,GREEN
# 56789 MAROON,MAGENTA,CYAN,NAVY,DIMGRAY

r = 1
for ol in octopusASCII:
    print(" "*5 + str(ol))    
    show_text(str(ol), r)
    r += 1 

uart.write('h175') # horizontal line
uart.write('W2')
show_text("    OctopusLab", 9)
uart.write('W1')
show_text(" serial display 21", 10)
uart.write('h245')

uart.write('W7')
show_text("test", 12)
uart.write('W1')
for i in range(100):
   show_text(str(100-i), 0)
   show_text(str(i), 13)
   sleep(0.5)



