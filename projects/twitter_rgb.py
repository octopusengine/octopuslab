# simple basic api example - ESP32 + WS rgb color from twitter: #cheerlights

from utils.octopus import *
import urequests

url = 'http://api.thingspeak.com/channels/1417/field/2/last.txt'

def twitter_rgb():
    response = urequests.get(url)
    text = response.text

    if text and text[0] == '#':
        color = text[1:7]

        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)

        return red, green, blue
    return 0, 0, 0
