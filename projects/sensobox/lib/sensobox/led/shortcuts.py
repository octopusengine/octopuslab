from . import Led
from sensobox.pinout import PIN_LED_RED, PIN_LED_AMBER, PIN_LED_GREEN

led_green = Led(PIN_LED_GREEN)
led_amber = Led(PIN_LED_AMBER)
led_red = Led(PIN_LED_RED)
