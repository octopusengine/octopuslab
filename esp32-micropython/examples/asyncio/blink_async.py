# octopusLAB simple asyncio example
# ESP32board with "BUILT_IN_LED"

from util.led import Led
# from util.octopus import led # short way
from util.pinout import set_pinout

pinout = set_pinout()           # set board pinout
led = Led(pinout.BUILT_IN_LED)  # BUILT_IN_LED = 2

print("---examples/asyncio/blink_async.py---")

import uasyncio

async def ablink(period_ms):
    while True:
        led.value(1)
        await uasyncio.sleep_ms(period_ms)
        led.value(0)
        await uasyncio.sleep_ms(period_ms)

async def main():
    uasyncio.create_task(ablink(700))
    await uasyncio.sleep_ms(10000)

# Running on a ROBOTboard
uasyncio.run(main())
