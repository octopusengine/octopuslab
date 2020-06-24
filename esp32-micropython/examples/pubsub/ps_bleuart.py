# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub and ble-uart example

from time import sleep
from examples.pubsub.ps_init import pubsub

print("start: ps_bleuart.py")

from shell.terminal import getUid
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
    datas = data.decode("utf-8") # data string
    pubsub.publish('bleuart', datas)

    print(datas)
    if data == bf.UP:
        led.value(1)
    if data == bf.DOWN:
        led.value(0)

devName = 'octopus-uart-'+uID5
print("BLE ESP32 device name: " + devName)

uart = bleuart.BLEUART(name=devName, on_data_received=on_data_received)
uart.start()




