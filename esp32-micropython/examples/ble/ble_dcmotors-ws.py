# octopusLAB - main.py - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_dcmotors.py

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

led.blink()
steering.center(speed)
sleep(2)
led.blink()
steering.center(0)

print("BLE init")
from util.ble import bleuart
import util.ble.bluefruit as bf



def on_data_received(connection, data):
    steering.center(0)

    print(str(data))
    if data == bf.UP:
        #led.value(1)
        steering.dynamicLR(speed,-speed)
    if data == bf.DOWN:
        #led.value(0)
        steering.dynamicLR(-speed,speed)
    if data == bf.LEFT:
       steering.dynamicLR(speed,0)
    if data == bf.RIGHT:
       steering.dynamicLR(0,-speed)

    sleep(0.2)


devName = 'octopus-robot-'+uID5
print("BLE ESP32 device name: " + devName)

uart = bleuart.BLEUART(name=devName, on_data_received=on_data_received)
uart.start()

while True:
    sleep(0.1)
