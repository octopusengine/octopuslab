# octopusLAB - main.py - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_pwm.py

print("---> BLE and BlueFruit mobile app. - pwm")
print("This is simple Micropython example | ESP32 & octopusLAB")

from util.shell.terminal import getUid
uID5 = getUid(short=5)

from time import sleep
from machine import Pin,PWM
from util.led import Led

led = Led(2)
duty = 0
pwm = PWM(Pin(4, Pin.OUT), 500, duty)

led.blink()
sleep(3)
led.blink()

from util.ble import bleuart
import util.ble.bluefruit as bf

def on_data_received(connection, data):
    global duty
    print(str(data), duty)

    if data == bf.UP:
        led.value(1)
        duty = 600
    
    if data == bf.DOWN:
        led.value(0)
        duty = 0
    
    if data == bf.LEFT:
        duty = duty - 50
        if duty < 0: 
            duty = 0
            led.value(0)
    
    if data == bf.RIGHT:
        duty = duty + 50
        if duty > 1000:
            duty = 1000
        led.value(1)

    pwm.duty(duty)


devName = 'octopus-pwm-'+uID5
print("BLE ESP32 device name: " + devName)

uart = bleuart.BLEUART(name=devName, on_data_received=on_data_received)
uart.start()
