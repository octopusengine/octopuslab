from time import sleep_ms
from sensobox.led.shortcuts import led_green, led_amber, led_red

print("---led---")

while True:
    led_red.toggle()
    sleep_ms(250)
    led_red.toggle()
    led_amber.toggle()
    sleep_ms(250)
    led_amber.toggle()
    led_green.toggle()
    sleep_ms(250)
    led_green.toggle()

