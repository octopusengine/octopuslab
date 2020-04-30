# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

from examples.pubsub.ps_init import pubsub
from machine import UART

print("ESP32 + serial display pubsub test")

uart = UART(2, 115200) #UART2 > #U2TXD(SERVO1/PWM1_PIN) #  9600/115200
# uart.write('C')      #test quick clear display 

def display_send(bleuart):
    uart.write(bleuart)

pubsub.subscribe('bleuart', display_send)
