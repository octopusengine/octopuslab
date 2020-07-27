from machine import Pin

from util.button import Button

left_button = Button(36, release_value=1)
right_button= Button(34, release_value=1)
top_button = Button(39, release_value=1)
bottom_button = Button(35, release_value=1)

import util.ble.blesync_client
import util.ble.blesync_uart.client

built_in_led = Pin(2, Pin.OUT)


@blesync_uart.client.UARTService.on_message
def on_message(service, message):
    print(message)


client = blesync_client.BLEClient(blesync_uart.client.UARTService)


def connect():
    while True:
        for device in blesync_client.scan():
            if device.adv_name == 'robot':
                services = client.connect(addr_type=device.addr_type, addr=device.addr)
                return services[blesync_uart.client.UARTService][0]


uart_service = connect()

built_in_led.on()


@left_button.on_press
def on_press_left_button():
    uart_service.send(b'!B714')


@left_button.on_release
def on_release_left_button():
    uart_service.send(b'!B507')


@right_button.on_press
def on_press_right_button():
    uart_service.send(b'!B813')


@right_button.on_release
def on_release_right_button():
    uart_service.send(b'!B804')


@top_button.on_press
def on_press_top_button():
    uart_service.send(b'!B516')


@top_button.on_release
def on_release_top_button():
    uart_service.send(b'!B507')


@bottom_button.on_press
def on_press_bottom_button():
    uart_service.send(b'!B615')


@bottom_button.on_release
def on_release_bottom_button():
    uart_service.send(b'!B606')
