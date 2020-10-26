# simple basic example - ESP32 + 7segment display
print("--- octopusLAB: test_display7.py ---")


print("-> imports")
from time import sleep
from machine import Pin, SPI
from utils.pinout import set_pinout
from components.display7 import Display7

print("-> spi-init")
pinout = set_pinout()
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
#spi.deinit() #print("spi > close")

print("-> display7-init")
d7 = Display7(spi, ss) # 8 x 7segment display init
d7.write_to_buffer('octopus')
d7.display()
sleep(3)

print("-> display7-test")
for i in range(6):
    d7.show(5-i)
    sleep(0.5)

print("-"*30)


