# octopusLAB - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_servo.py
# 13.6.2020

print("---> BLE and BlueFruit mobile app. - pwm")
print("This is simple Micropython example | ESP32 & octopusLAB")

from utils.octopus_lib import getUid
uID5 = getUid(short=5)

from time import sleep
from utils.pinout import set_pinout
from components.servo import Servo
pinout = set_pinout()

s1 = Servo(pinout.PWM1_PIN)
s2 = Servo(pinout.PWM2_PIN)
# s3 = Servo(pinout.PWM3_PIN)

import blesync_server
import blesync_uart.server 
import utils.ble.bluefruit as bf


angle1 = 45
angle2 = 45
s1.set_degree(angle1)
s2.set_degree(angle2)
angle_min = 10
angle_max = 150


@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    global angle1, angle2
    print(str(message), angle1, angle2)

    if message == bf.LEFT:
        angle1 = angle1 - 5
        if angle1 < angle_min: 
            angle1 = angle_min
        s1.set_degree(angle1)
    
    if message == bf.RIGHT:
        angle1 = angle1 + 5
        if angle1 > angle_max:
            angle1 = angle_max
        s1.set_degree(angle1)

    if message == bf.UP:
        angle2 = angle2 - 5
        if angle2 < angle_min: 
            angle2 = angle_min
        s2.set_degree(angle2)
    
    if message == bf.DOWN:
        angle2 = angle2 + 5
        if angle2 > angle_max:
            angle2 = angle_max
        s2.set_degree(angle2)

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

devName = 'octopus-servo-'+uID5
print("BLE ESP32 device name: " + devName)


server = blesync_server.Server(devName, blesync_uart.server.UARTService)
server.start()
