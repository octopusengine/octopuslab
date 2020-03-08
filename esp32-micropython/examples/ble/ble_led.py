# octopusLAB - main.py - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_led.py

print("---> BLE and BlueFruit mobile app. - led")
print("This is simple Micropython example | ESP32 & octopusLAB")

from time import sleep
from util.led import Led
led = Led(2)

led.blink()
sleep(3)
led.blink()

from util.ble import bleuart
import util.ble.bluefruit as bf

def on_data_received(connection, data):
    print(str(data))
    if data == bf.UP:
        led.value(1)
    if data == bf.DOWN:
        led.value(0)


uart = bleuart.BLEUART(name='octopus-led', on_data_received=on_data_received)
uart.start()