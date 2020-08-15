# octopusLAB - main.py - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_pwm.py
# 8.6.2020

print("---> BLE and BlueFruit mobile app. - pwm")
print("This is simple Micropython example | ESP32 & octopusLAB")

from utils.octopus_lib import getUid
uID5 = getUid(short=5)

from time import sleep
from machine import Pin,PWM
from components.iot.pwm_fade import fade_in
from components.led import Led
from components.button import Button
from time import ticks_ms, ticks_diff
from components.analog import Analog
from components.iot import Thermometer

led_light = False
led = Led(2)
duty = 0
led_button = Button(0, release_value=1)
anLight = Analog(36)
pwm = PWM(Pin(17, Pin.OUT), 500, duty) # PWM1
tt = Thermometer(32)
print("init-test")
print("light", anLight.get_adc_aver(8))
print("temp.",tt.get_temp())


led.blink()
sleep(3)
led.blink()

import blesync_server
import blesync_uart.server
import utils.ble.bluefruit as bf

@led_button.on_press
def on_press_button():
    print("on_press_button")
    global led_light

    led_light = not led_light
    print(led_light)
    if led_light:
        fade_in(pwm,600)
        duty = 600
    else:
        led.value(0)
        duty = 0

    pwm.duty(duty)


@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    global duty
    print(str(message), duty)

    if message == bf.UP:
        led.value(1)
        fade_in(pwm,600)
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

# server = blesync_server.Server(devName, blesync_uart.server.UARTService)

# server.start()

p = Pin(16, Pin.IN)
sfa = ticks_ms()
while True:
    if p.value():
        son = ticks_ms()
        led.value(1)
        if son-sfa > 6000:
            print("fade_on")
            fade_in(pwm,600)
            sfa = ticks_ms()

        duty = 600
        pwm.duty(duty)
        sleep(6)
        son = ticks_ms()
    else:
        led.value(0)
        sleep(0.2)
        duty = 0
    pwm.duty(duty)
