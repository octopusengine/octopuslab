# octopusLAB pub sub module for led
# usage:
# import octopus.ps_led
# pubsub.publish('led_value', VALUE)


from components.led import Led
import pubsub

led = Led(2)

@pubsub.subscriber("led_value")
def led_val(led_value):
    led.value(led_value)


print("--- starting pubsub: ps_led (led_value) ---")
