"""
Hybrid reader 125kHz + 13MHz
RDM6300 + PN532
"""


from time import sleep
from machine import Pin
from machine import UART
from utils.pinout import set_pinout
from gc import mem_free

from components.rfid import PN532_UART

print("--- RAM free ---> " + str(mem_free())) 
pinout = set_pinout()

uart_pn = UART(2, 115200) # UART 2 is by default on  TX=PWM1/SERVO1, RX=PWM2/SERVO2

tx_pin = Pin(pinout.DEV1_PIN, Pin.OUT)
rx_pin = Pin(pinout.DEV2_PIN, Pin.IN)

uart_rdm = UART(1, 9600, tx=pinout.DEV1_PIN, rx=pinout.DEV2_PIN, timeout=100)

pn532 = PN532_UART(uart_pn, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")
while True:
    print(".", end="")

    # Read PN532
    uid_raw = pn532.read_passive_target(timeout=0.1)
    if uid_raw is not None:
        uid = "{:010d}".format(int.from_bytes(uid_raw, "little"))
        print("Found 13MHz card with UID:", uid)
    pn532.power_down()

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