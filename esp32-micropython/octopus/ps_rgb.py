# octopusLAB pub sub module for led
# usage:
# import octopus.ps_rgb

import pubsub
from components.rgb import Rgb

rgb = Rgb(15) # robot board default
rgb.color((0,0,0))

@pubsub.subscriber("rgb_color")
def rgb_col(rgb_color):
    rgb.color(rgb_color)


print("--- starting pubsub: ps_rgb (rgb_color) ---")
