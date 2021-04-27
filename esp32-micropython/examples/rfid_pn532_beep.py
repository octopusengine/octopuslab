"""
This example uses PN531 RFID module connected to UART
 - we use UART 2 by default on  TX=PWM1/SERVO1, RX=PWM2/SERVO2
 - piezzo connected on octopus robot board on 12EN pin 25
 - 3 different tunes
   - SUCCESS - chord C
   - REFUSED - two low beeps
   - ERROR - deep tone 
"""

from time import sleep
# from machine import Pin
from machine import UART
from utils.pinout import set_pinout
from gc import mem_free

from components.rfid import PN532_UART
from components.buzzer import Buzzer
from components.buzzer.notes import *

print("--- RAM free ---> " + str(mem_free())) 
pinout = set_pinout()

# mocking database of identifiers
# list of str(10)
valid_uids = [
    '0839999976'
]

# we have piezzo connected on octopus robot board on 12EN pin 25
piezzo = Buzzer(25)

uart = UART(2, 115200) # UART 2 is by default on  TX=PWM1/SERVO1, RX=PWM2/SERVO2

# tx_pin = Pin(pinout.DEV1_PIN, Pin.OUT)
# rx_pin = Pin(pinout.DEV2_PIN, Pin.IN)
# uart.init(baudrate=115200, tx=pinout.DEV1_PIN, rx=pinout.DEV2_PIN, timeout=100)

pn532 = PN532_UART(uart, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")
while True:
    try:
        # Check if a card is available to read
        uid_raw = pn532.read_passive_target(timeout=0.25)
        print(".", end="")
        if uid_raw is not None:
            uid = '{:010d}'.format(int.from_bytes(uid_raw, 'little'))
            print("Found card with UID: ", uid)
            # note that play_melody is blocking
            if uid in valid_uids:
                piezzo.play_melody([[C5,8], [G5,8], [A5,8]])
            else:
                piezzo.play_melody([[C4,4], [0,16], [C4,4]])
        pn532.power_down()
    except RuntimeError as e:
        # skip errors - some bank cards raise this
        # File "octopus_pn532.py", line 259, in _read_frame
        # RuntimeError: ('Response checksum did not match expected value: ', 221)
        piezzo.play_melody([[C3,2]])
        print(e)
    sleep(0.25)
