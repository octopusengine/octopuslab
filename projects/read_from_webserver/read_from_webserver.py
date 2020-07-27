import urequests
from utils.octopus import disp7_init
from time import time, sleep
from utils.octopus import w
from components.servo import Servo
s1 = Servo(17)
from components.rgb import Rgb
from utils.pinout import set_pinout
pinout = set_pinout()
from utils.io_config import get_from_file
io_conf = get_from_file()
ws = Rgb(pinout.WS_LED_PIN,io_conf.get('ws'))
w()

# You can change it to what you want
# This server have /set.php?name=[name]&data=[data] wich will set data for the given name
# And get.php?name=[name] wich will give back the data
# At the root there is a simple form to put data
SERVER_URL = "http://ark.smee.ovh:8088/get.php?name=bryan"

d7 = disp7_init()
global cursor
cursor = 0
global total_text
total_text = "Octopus"
last_time = -10000
def set_text(text):
    global cursor
    global total_text
    cursor = 0
    total_text = text

def get_text():
    global cursor
    if (cursor + 8) > len(total_text):
        end_cursor = len(total_text)
    else:
        end_cursor = cursor + 8
    show_text = total_text[cursor:end_cursor]
    cursor += 1
    if cursor >= len(total_text):
        cursor = 0
        print("In the cursor reset")
    return show_text

while True:
    if (time() - last_time) > 5:
        response = urequests.get()
        text = response.text
        if total_text != response.text:
            if response.text[0] == '#':
                color = text[1:7]
                red = int(color[0:2], 16)
                green = int(color[2:4], 16)
                blue = int(color[4:6], 16)
                ws.color((red,green,blue))
            elif response.text[0] == 'M':
                angle = int(text[1:3])
                if angle < 0:
                    angle = 0
                elif angle > 120:
                    angle = 120
                s1.set_degree(angle)
            else:
                set_text(response.text)
        last_time = time()
    d7.show(get_text())
    sleep(0.5)
