print("--- octopusLAB: test_rgb ---")

print("-> pinout | io_config")
from utils.pinout import set_pinout
pinout = set_pinout()
from utils.io_config import get_from_file
io_conf = get_from_file()

print("-> init")
from components.rgb import Rgb
ws = Rgb(pinout.WS_LED_PIN,io_conf.get('ws'))

print("-> blink()")
ws.simpleTest()

print("-"*30)
