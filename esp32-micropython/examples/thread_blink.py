# octopusLAB simple thread example
# ESP32board with "BUILT_IN_LED"
# https://techtutorialsx.com/2017/10/02/esp32-micropython-creating-a-thread/


from util.octopus import led
import _thread
from time import sleep

print("---examples/thread_blink.py---")

def testThread1():
    while True:
        led.blink()
        sleep(1)

_thread.start_new_thread(testThread1, ())
