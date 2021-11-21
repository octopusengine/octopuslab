from time import sleep
from machine import UART
from utils.pinout import set_pinout
from gc import mem_free
from components.rfid import PN532_UART

print("--- RAM free ---> " + str(mem_free())) 
pinout = set_pinout()

uart = UART(2, 115200)
#UART1:
#uart.init(baudrate=115200, tx=pinout.TXD1, rx=pinout.RXD1, timeout=100)
#UART2:
uart.init(baudrate=115200, tx=pinout.PWM1_PIN, rx=pinout.PWM2_PIN, timeout=100)

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
        card_id = ""
        for i in uid:
           card_id += str(hex(i))[2:]

        print("Found card with UID:", card_id)
        #piezzo.beep()
    pn532.power_down()
    sleep(1.0)
