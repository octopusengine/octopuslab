# prerequests
# import upip
# upip.install("micropython-ssd1306")

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

from machine import I2C, Pin
import network
from ssd1306 import SSD1306_I2C

wlan = network.WLAN()
wlan.active(1)
wlan.connect(WIFI_SSID, WIFI_PASS)

i2c = I2C(scl = Pin(4), sda=Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while 1:
    oled.fill(0)
    oled.text("Signal: {} dBi".format(wlan.status('rssi')), 0, 0)
    oled.fill_rect(0, 15, map(wlan.status('rssi'), -100, -30, 0, 120), 10, 1)
    oled.show()
    time.sleep_ms(250)
