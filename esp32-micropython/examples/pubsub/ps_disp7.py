# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo, Jan Copak
# octopusLAB pubsub example

from examples.pubsub.ps_init import pubsub
from util.octopus import disp7_init

d7 = disp7_init()  # 8 x 7segment display init

def display_num(value):
    d7.show(value)

pubsub.subscribe('value', display_num)
