# octopusLAB pub sub module for 8 x 7 segment display
# usage:
# import octopus.ps_display7

import pubsub
from utils.octopus import disp7_init

d7 = disp7_init()  # 8 x 7segment display init


@pubsub.subscriber("d7_text")
def display_num(d7_text):
    d7.show(d7_text)


print("--- starting pubsub: ps_disp7 (d7_text) ---")
