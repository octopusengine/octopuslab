# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

from time import sleep
from examples.pubsub.ps_init import pubsub

print("start: ps_rgb.py")

from util.rgb import Rgb
rgb = Rgb(15) # robot board default

rgb.color((0,0,0))


while True:
    rgb.color((128,0,0))
    pubsub.publish('value', 1)
    sleep(1)

    rgb.color((0,128,0))
    pubsub.publish('value', 2)
    sleep(1)

    rgb.color((0,0,128))
    pubsub.publish('value', 3)
    sleep(1)

