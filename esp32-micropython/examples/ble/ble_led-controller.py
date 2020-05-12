# octopusLAB - simple example
## BLE controll for examples/ble/ble_led.py

from time import sleep
from machine import Pin
from util.button import Button
import blesync_client
import blesync_uart.client
import util.ble.bluefruit as bf

built_in_led = Pin(2, Pin.OUT)
led_button = Button(0, release_value=1)

built_in_led.blink()
sleep(3)


@blesync_uart.client.UARTService.on_message
def on_message(service, message):
    print(message)


client = blesync_client.BLEClient(blesync_uart.client.UARTService)


def connect():
    while True:
        for device in blesync_client.scan():
            if device.adv_name == 'octopus-led-24de0': # set yout UID
                services = client.connect(addr_type=device.addr_type, addr=device.addr)
                return services[blesync_uart.client.UARTService][0]


uart_service = connect()

built_in_led.on()
sleep(0.5)
built_in_led.off()


@led_button.on_press
def on_press_top_button():
    uart_service.send(bf.RIGHT)