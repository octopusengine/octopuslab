from sensobox.wsled import instance as ws
import colors_rgb as rgb # definice barev v /lib > RED, GREEN, BLUE, ORANGE, BLACK (nesvítí)
from sensobox.button import a_instance as color_btn, b_instance as bright_btn
from sensobox.display import instance as display

# define color scheme
COLOR_SCHEME = [
    [0, 0, 100],
    [0, 100, 0],
    [100, 0, 0],
    [0, 100, 100],
    [100, 100, 0],
    [100, 0, 100],
    [100, 100, 100]
]

current_color = 0
# max brightness = 8
brightness = 0

# shifts current color to the next index
@color_btn.on_press
def next_color():
    global current_color
    if current_color == len(COLOR_SCHEME) - 1:
        current_color = 0
    else:
        current_color += 1
    update_color()
    
# shifts current brightness to the next index
@bright_btn.on_press
def next_brightness():
    global brightness
    if brightness == 8:
        brightness = 0
    else:
        brightness += 1
    update_color()
    
# calculates maximum possible brightness of the
# predefined color and sets it to the current brightness
def update_color():
    global current_color
    global brightness
    c0 = COLOR_SCHEME[current_color][0]
    c1 = COLOR_SCHEME[current_color][1]
    c2 = COLOR_SCHEME[current_color][2]
    b = brightness / 8
    m = max(c0, c1, c2)
    if m == 0:
        ws.color(0, 0, 0)
    else:
        q = 255 / m
        b *= q
        ws.color((int(c0*b), int(c1*b), int(c2*b)))
    display.show("b"+str(brightness)+"."+"c"+str(current_color))
