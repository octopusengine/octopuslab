from time import ticks_ms, ticks_diff
from machine import Pin
from components.led import Led

led_pin = Pin(2, Pin.OUT)
led = Led(2)

num = 100000

print("--- test 1: for 100k led.value")
start = ticks_ms()
for _ in range(num):
    led.value(1)
    led.value(0)

stop = ticks_ms()
print(start, "-", stop, ":", stop-start)
print("-"*20)


print("--- test 2: for 10k Pin.on/off")
start = ticks_ms()
for _ in range(num):
    led_pin.on()
    led_pin.off()

stop = ticks_ms()
print(start, "-", stop, ":", stop-start)
print("-"*20)


print("--- test 2: @native for 100k led.value")

@micropython.native
def test_native():
    for _ in range(num):
        led_pin.on()
        led_pin.off()

start = ticks_ms()
test_native()
stop = ticks_ms()
print(start, "-", stop, ":", stop-start)
print("-"*20)


print("--- test 2: @viper for 100k led.value")

@micropython.viper
def test_viper():
    for _ in range(100000):
        led_pin.on()
        led_pin.off()

start = ticks_ms()
test_viper()
stop = ticks_ms()
print(start, "-", stop, ":", stop-start)
print("-"*20)
