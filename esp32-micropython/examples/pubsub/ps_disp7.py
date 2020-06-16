# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

import pubsub
from util.octopus import disp7_init

d7 = disp7_init()  # 8 x 7segment display init


@pubsub.subscriber("value")
def display_num(value):
    d7.show(value)
    


