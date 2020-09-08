# octopusLAB
from machine import Pin
from time import sleep, sleep_ms
import urandom
from utils.octopus import oled_init
from components.oled import threeDigits

import blesync_server
import blesync_uart.server
import utils.ble.bluefruit as bf

from utils.octopus_lib import getUid
uID5 = getUid(short=5) 

print("OctopusLAB edu shield 1, 2 x butn, OLED, BLE")

# from utils.pinout import set_pinout
# pinout = set_pinout()

from components.button import Button
from components.led import Led

led = Led(2)
led2 = Led(16)
led3 = Led(17)
oled = oled_init()

led.blink(100)
led2.blink(100)
led3.blink(100)



print("thread_blink")
import _thread

def tblink(num=20,period_ms=50):
    for _ in range(num):
        led.value(1)
        sleep_ms(period_ms)
        led.value(0)
        sleep_ms(period_ms)


_thread.start_new_thread(tblink, ())



print("buttons")

boot_pin = Pin(0, Pin.IN)
boot_button = Button(boot_pin, release_value=1)

pin34 = Pin(34, Pin.IN)
pin35 = Pin(35, Pin.IN)
# pin36 = Pin(36, Pin.IN)
# pin39 = Pin(39, Pin.IN)

right_button = Button(pin35, release_value=1)
left_button = Button(pin34, release_value=1)
status = 123

def oled_num(oled,num):
    threeDigits(oled,num,False,False)
    print(num)


def left_action():
    global status
    led2.value(1)
    status = status - 1
    oled_num(oled,status)


def right_action():
    global status
    led3.value(1)
    status = status + 1
    oled_num(oled,status)


def clear_action():
    _thread.start_new_thread(tblink, (3,200))
    print("clear_action: ", end = ' ')
    led2.value(0)
    led3.value(0)
    oled.fill(0)    
    sleep(1)
    oled.show()
    print("DONE")


def save_action():
    _thread.start_new_thread(tblink, ())
    print("save_action")



@boot_button.on_press
def boot_button_on_press():
    print('boot_button_on_press')

@boot_button.on_long_press
def boot_button_on_long_press():
    print('boot_button_on_long_press')
    clear_action()

@boot_button.on_release
def boot_button_on_release():
    print('boot_button_on_release')


@right_button.on_press
def right_button_on_press():
    print('right_button_on_press')
    right_action()

@right_button.on_release
def right_button_on_release():
    print('right_button_on_release')
    led3.value(0)


@right_button.on_long_press
def right_button_on_long_press():
    print('right_button_on_long_press')
    save_action()
    led3.blink()
    led3.value(0)


@left_button.on_press
def left_button_on_press():
    print('right_left_on_press')
    left_action()


@left_button.on_release
def left_button_on_release():
    print('left_button_on_release')
    led2.value(0)


@left_button.on_long_press
def left_button_on_long_press():
    print('left_button_on_long_press')
    save_action()
    led2.blink()
    led2.value(0)

print("BLE")

@blesync_uart.server.UARTService.on_message
def on_message(service, conn_handle, message):
    if message == bf.UP:
        led2.blink()
        led3.blink()
    if message == bf.DOWN:
        clear_action()
    if message == bf.RIGHT:
        right_action()
    if message == bf.LEFT:
        left_action()

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


devName = 'octopus-oled-'+uID5
print("BLE ESP32 device name: " + devName)

server = blesync_server.Server(devName, blesync_uart.server.UARTService)

print("start")

server.start()

