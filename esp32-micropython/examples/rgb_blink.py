# octopusLAB simple example
# ESP32board with "RGB WS LED"
# run: import examples.rgb_blink

from components.rgb import Rgb
from utils.pinout import set_pinout

pinout = set_pinout()           # set board pinout
from utils.io_config import get_from_file
io_conf = get_from_file()

ws = Rgb(pinout.WS_LED_PIN,io_conf.get('ws'))

print("---examples/rgb_blink.py---")

# start main loop
while True:
   ws.simpleTest()