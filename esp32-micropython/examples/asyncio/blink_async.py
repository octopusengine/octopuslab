# octopusLAB simple asyncio example
# ESP32board with "BUILT_IN_LED"

from util.led import Led
# from util.octopus import led # short way
from util.pinout import set_pinout

pinout = set_pinout()           # set board pinout
led = Led(pinout.BUILT_IN_LED)  # BUILT_IN_LED = 2

print("---examples/asyncio/blink_async.py---")

import uasyncio

async def blink(period_ms):
    while True:
        led.blink(period_ms)

async def main():
    uasyncio.create_task(blink(700))
    await uasyncio.sleep_ms(10000)

# Running on a ROBOTboard
uasyncio.run(main())