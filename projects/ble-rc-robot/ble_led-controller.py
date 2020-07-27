from time import sleep
from machine import Pin
from util.button import Button

led_button = Button(0, release_value=1)

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
            if device.adv_name == 'octopus_led':
                services = client.connect(addr_type=device.addr_type, addr=device.addr)
                return services[blesync_uart.client.UARTService][0]


uart_service = connect()

built_in_led.on()
sleep(1)
built_in_led.off()


@led_button.on_press
def on_press_top_button():
    uart_service.send(b'!B516')


@led_button.on_release
def on_release_top_button():
    uart_service.send(b'!B507')
