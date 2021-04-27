from time import sleep
# from machine import Pin
from machine import UART
from utils.pinout import set_pinout
from gc import mem_free

from components.rfid import PN532_UART

print("--- RAM free ---> " + str(mem_free())) 
pinout = set_pinout()

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
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end="")
    if uid is not None:
        print("Found card with UID:", [hex(i) for i in uid])
    pn532.power_down()
    sleep(1.0)
