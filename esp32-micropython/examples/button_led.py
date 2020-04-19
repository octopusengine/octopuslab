# octopusLAB test - 2020
# simple test Button lib

from time import sleep
from machine import Pin
from util.button import Button

led_button = Button(0, release_value=1)
built_in_led = Pin(2, Pin.OUT)

built_in_led.on()
sleep(1)
built_in_led.off()

@led_button.on_press
def on_press_top_button():
    print("on_press_top_button")
    built_in_led.on()
    sleep(3)
    built_in_led.off()
