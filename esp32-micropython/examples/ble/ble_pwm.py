# octopusLAB - main.py - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_pwm.py
# 8.6.2020

print("---> BLE and BlueFruit mobile app. - pwm")
print("This is simple Micropython example | ESP32 & octopusLAB")

from shell.terminal import getUid
uID5 = getUid(short=5)

from time import sleep
from machine import Pin,PWM
from util.led import Led

led = Led(2)
duty = 0
pwm = PWM(Pin(4, Pin.OUT), 500, duty) # PWM3

led.blink()
sleep(3)
led.blink()

import blesync_server
import blesync_uart.server 
import util.ble.bluefruit as bf

@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    global duty
    print(str(message), duty)

    if message == bf.UP:
        led.value(1)
        duty = 600
    
    if message == bf.DOWN:
        led.value(0)
        duty = 0
    
    if message == bf.LEFT:
        duty = duty - 50
        if duty < 0: 
            duty = 0
            led.value(0)
    
    if message == bf.RIGHT:
        duty = duty + 50
        if duty > 1000:
            duty = 1000
        led.value(1)

    pwm.duty(duty)
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

devName = 'octopus-pwm-'+uID5
print("BLE ESP32 device name: " + devName)

server = blesync_server.Server(devName, blesync_uart.server.UARTService)

server.start()
