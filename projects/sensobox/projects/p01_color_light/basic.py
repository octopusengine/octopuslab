from machine import Pin
from sensobox.wsled import instance as ws
import colors_rgb as rgb # definice barev v /lib > RED, GREEN, BLUE, ORANGE, BLACK (nesvítí)
from sensobox.button import a_instance as next_btn, b_instance as prev_btn

# define color scheme
COLOR_SCHEME = [
    (0, 0, 100),
    (0, 100, 0),
    (100, 0, 0),
    (0, 100, 100),
    (100, 100, 0),
    (100, 0, 100),
    (100, 100, 100)
]

current_color = 0

# changing the current color to the next one
@next_btn.on_press
def next_color():
    global current_color
    if current_color == len(COLOR_SCHEME) - 1:
        current_color = 0
    else:
        current_color += 1
    ws.color(COLOR_SCHEME[current_color])

# switching the current color to the previous on    
@prev_btn.on_press
def prev_color():
    global current_color
    if current_color == 0:
        current_color = len(COLOR_SCHEME) - 1
    else:
        current_color -= 1
    ws.color(COLOR_SCHEME[current_color])
