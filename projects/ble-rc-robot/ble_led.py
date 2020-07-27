print("---> BLE-BLE led controller")

from util.shell.terminal import getUid
uID5 = getUid(short=5)

from time import sleep
from util.pinout import set_pinout
pinout = set_pinout()

from util.rgb import Rgb
ws = Rgb(pinout.PWM3_PIN)
ws.simpleTest()


from util.led import Led
led = Led(2)

from machine import Pin
import util.ble.blesync_server
import util.ble.blesync_uart.server


@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    if message == b'!B516':
        led.value(1)
    elif message == b'!B507':
        led.value(0)


    service.send(conn_handle, message)


class Connections:
    _connections = []

    @blesync_server.on_connect
    @classmethod
    def on_connect(cls, conn_handle, addr_type, addr):
        cls._connections.append(conn_handle)
        built_in_led.on()

    @blesync_server.on_disconnect
    @classmethod
    def on_disconnect(cls, conn_handle, addr_type, addr):
        cls._connections.remove(conn_handle)
        if not cls._connections:
            built_in_led.off()


blesync_server.Server.start('octopus_led', blesync_uart.server.UARTService)
