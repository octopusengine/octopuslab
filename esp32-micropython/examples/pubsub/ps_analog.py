# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

from time import sleep
from examples.pubsub.ps_init import pubsub

print("start: ps_analog.py")

from util.analog import Analog
an2 = Analog(36)

# publish test
#pubsub.publish('value', 123)
sleep(3)

while True:
    value =  an2.get_adc_aver(8)
    #print(value)
    pubsub.publish('value', value)
    sleep(0.2)

