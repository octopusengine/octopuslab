# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

from examples.pubsub.ps_init import pubsub

from time import sleep
from util.octopus import oled_init
from util.display_segment import fourDigits

o = oled_init()

print("ps_oled:")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

o.clear()
o.contrast(10)
o.hline(0,53,128,1)
o.text("octopusLAB 2020", 3, 1)
o.show()
sleep(2)

def display_show(text):
    o.clear()
    o.text("octopusLAB 2020", 3, 1)
    o.hline(0,53,128,1)
    o.text(str(text), 3, 55)
    o.show()

pubsub.subscribe('value', display_show)
