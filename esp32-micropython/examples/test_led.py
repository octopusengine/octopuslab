print("--- octopusLAB: test_led ---")

print("-> init")
from components.led import Led
led = Led(2)

print("-> blink()")
led.blink()

print("-> value() | toggle()")
led.value(1)
led.toggle()

print("-"*30)
