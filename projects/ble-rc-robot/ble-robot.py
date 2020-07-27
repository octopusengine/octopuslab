print("---> BLE and BlueFruit mobile app. - robot")
print("This is simple Micropython example | ESP32 & octopusLAB")

speed = 900

from util.shell.terminal import getUid
uID5 = getUid(short=5)

from time import sleep
from util.pinout import set_pinout
pinout = set_pinout()

from util.rgb import Rgb
ws = Rgb(pinout.PWM3_PIN)
ws.simpleTest()


print("DCmotors init")
from util.dcmotors import Motor, Steering
motor_r = Motor(pinout.MOTOR_1A, pinout.MOTOR_2A, pinout.MOTOR_12EN)
motor_l = Motor(pinout.MOTOR_3A, pinout.MOTOR_4A, pinout.MOTOR_34EN)
steering = Steering(motor_l, motor_r)

from util.led import Led
led = Led(2)

from machine import Pin

import util.ble.blesync_server
import util.ble.blesync_uart.server


@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    if message == b'!B516':
        steering.center(1000)
    elif message == b'!B507':
        steering.center(0)
    elif message == b'!B615':
        steering.center(-1000)
    elif message == b'!B606':
        steering.center(0)
    elif message == b'!B813':
        steering.right(1000)
    elif message == b'!B804':
        steering.right(0)
    elif message == b'!B714':
        steering.left(1000)
    elif message == b'!B705':
        steering.left(0)

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


blesync_server.Server.start('robot', blesync_uart.server.UARTService)
