# octopusLAB
## uPyShell:~/$ run examples/ble/ble_led.py

print("---> BLE and BlueFruit mobile app. - led")
print("This is simple Micropython example | ESP32 & octopusLAB")

from util.shell.terminal import getUid
uID5 = getUid(short=5)

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
    if data == bf.RIGHT:
        led.toggle()


devName = 'octopus-led-'+uID5
print("BLE ESP32 device name: " + devName)

uart = bleuart.BLEUART(name=devName, on_data_received=on_data_received)
uart.start()
