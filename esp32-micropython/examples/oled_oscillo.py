# simple oled oscilloscope 
# freqency test

# signal pwmPin 16 > RC > analog read anIn 35

import machine
from utils.octopus import *
from utils.analog import Analog
import array as arr

octopus()

signalFreq = 1000
pixel2sample = 1
div = 100 # 4085 max > ymax
samples = 512

print("oled: ")
XMAX = 128
YMAX = 64
o = oled_init(XMAX, YMAX)      # init oled display
sleep(1)
o.clear()            # clear

pwmPin = machine.Pin(16)
signal = PWM(pwmPin) # servo2
signal.freq(signalFreq) # Hz 100-1000
signal.duty(512)
# signal.deinit()

anIn = Analog(35)

# data = [] # delta 104
data = {} # delta 126
"""
print("init array: ")
for sample in range(samples):
    data.append(0) 
"""

print("measure: ")
ar = anIn.read

Env.start = ticks_ms()
for sample in range(samples):
    data[sample] = ar()
    # data.append(anIn.get_adc_aver()) 6 samples for 100 Hz
    # data.append(anIn.read()) # for 100Hz ## delta 2277

delta = ticks_diff(ticks_ms(), Env.start)
print("delta_time: " + str(delta))

print("data: ")
for sample in range(samples):
    print(" ("+str(sample)+")", end="")
    print(str(data[sample]), end="") 
    o.pixel(int(sample/pixel2sample), int(data[sample]/div), 1)
o.show()




