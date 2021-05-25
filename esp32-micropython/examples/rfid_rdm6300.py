"""
RFID reader 125kHz
RDM6300
"""

from time import sleep
from machine import UART
from gc import mem_free

print("--- RAM free ---> " + str(mem_free())) 

uart_rdm = UART(2, 9600) # UART 2 is by default on  TX=PWM1/SERVO1, RX=PWM2/SERVO2

print("Waiting for RFID card...")
while True:
    print(".", end="")

    # Read RDM6300
    # TODO implement protocol 
    # https://github.com/arduino12/rdm6300/blob/master/src/rdm6300.h
    # https://github.com/arduino12/rdm6300/blob/master/src/rdm6300.cpp
    uid = ""
    if uart_rdm.any():
        uid_raw = uart_rdm.read(14)
        print("Found 125kHz card with UID:", [hex(b) for b in uid_raw])
        # discard duplicities
        while uart_rdm.any():
            uart_rdm.read(14)
    sleep(0.1)