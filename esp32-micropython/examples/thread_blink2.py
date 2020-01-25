# octopusLAB simple thread example
# ESP32board with "BUILT_IN_LED"


from util.octopus import led
import _thread
from time import sleep

print("---examples/thread_blink2.py---")

def testThread1():
  t1 = 0 # thread index
  while True:
    print("Hello from thread1: " + str(t1))
    t1 +=1
    sleep(3)


def testThread2():
  t2 = 0 # thread index
  while True:
    print("Hello from thread2: " + str(t2))
    t2 +=1
    sleep(7)

_thread.start_new_thread(testThread1, ())
_thread.start_new_thread(testThread2, ())

#def run():
while True:
    led.blink()
    print("main loop")

#run()