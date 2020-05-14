# octopusLAB
## uPyShell:~/$ run examples/ble/ble_led.py

print("---> BLE - led")
print("This is simple Micropython example | ESP32 & octopusLAB")
print("-"*39)

import blesync_server
import blesync_uart.server
import util.ble.bluefruit as bf

from util.shell.terminal import getUid
uID5 = getUid(short=5)

from time import sleep
from util.led import Led
led = Led(2)

led.blink()
sleep(3)
led.blink()


@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    if message == bf.UP:
        led.value(1)
    if message == bf.DOWN:
        led.value(0)
    if message == bf.RIGHT:
        led.toggle()

    service.send(conn_handle, message)


_connections = []


@blesync_server.on_connect
def on_connect(conn_handle, addr_type, addr):
    _connections.append(conn_handle)
    # built_in_led.on()
    print("@blesync_server.on_connect")


@blesync_server.on_disconnect
def on_disconnect(conn_handle, addr_type, addr):
    _connections.remove(conn_handle)
    if not _connections:
        # built_in_led.off()
        print("@blesync_server.on_disconnect")


devName = 'octopus-led-'+uID5
print("BLE ESP32 device name: " + devName)

server = blesync_server.Server(devName, blesync_uart.server.UARTService)

server.start()
