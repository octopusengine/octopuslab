"""
This is simple usage of SSD1306 OLED display over I2C
Connect to wifi using config
either deploy config/wifi.json or use setup() in REPL to create one

TODO make wifi connection non blocking
- if wrong credentials are provided, REPL will not start (long timeout)
  it's hard to re-run setup() to fix credentials

Installation:
ampy -p /dev/ttyUSB0 put ./config
ampy -p /dev/ttyUSB0 put ./lib
ampy -p /dev/ttyUSB0 put ./util
ampy -p /dev/ttyUSB0 put ./05-oled.py main.py
# reset device

"""
import machine
import time
import ujson
from lib import ssd1306

# TODO make import nicer
from util.wifi_connect import WiFiConnect # Include wifi

# TODO move to config
import octopus_robot_board as o #octopusLab main library - "o" < octopus

i2c = machine.I2C(-1, machine.Pin(o.I2C_SCL_PIN), machine.Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()

time.sleep_ms(300)

# reset display
oled.fill(0)
oled.show()

# write text on x, y
oled.text('OLED test', 20, 20)
oled.show()
time.sleep_ms(1000)

# for i in range(1,10+1):
#    oled.fill(0)
#    oled.text('OctopusLab', 20, 15)
#    oled.text(" --- "+str(10-i)+" ---", 20, 35)
#    oled.show()
#    time.sleep_ms(1000)


# Wifi connect

# TODO move to separate module
pin_led = machine.Pin(o.BUILT_IN_LED, machine.Pin.OUT)

def simple_blink(delay):
    pin_led.value(1)
    time.sleep(delay/2)
    pin_led.value(0)
    time.sleep(delay/2)

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink(1)
    oled.text(sta.ifconfig()[0], 2, 50)
    oled.show()

    # print(sta.ifconfig())

def connecting_callback():
    simple_blink(0.2)

# Load config
# TODO move to separate module
def load_wifi_config():
    # TODO check format
    try:
        with open("config/wifi.json", "r") as entry:
            result = ujson.load(entry)
    except OSError as ex:
        return None
    else:
        entry.close()
        return result

w = WiFiConnect()
w.events_add_connecting(connecting_callback)
w.events_add_connected(connected_callback)
wc = load_wifi_config()
if wc:
    w.connect(wc['wifi_ssid'], wc['wifi_pass'])
else:
    oled.text("No wifi config. Run setup().", 2, 50)
    oled.show()
