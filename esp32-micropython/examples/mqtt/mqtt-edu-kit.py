"""
# basic example: octopusLAB EDU kit - ESP32 - WiFi - MQTT

This requires configuration of wifi and MQTT broker connection (`/config/mqtt.json`)
https://docs.octopuslab.cz/basicdoc/#config

DeviceID is used as part of the MQTT topic

`octopus/device/98f4ab6f1b20/led` - accepts '0'/'1'
`octopus/device/98f4ab6f1b20/rgb` - accepts '#FF00FF' or 'rgb(255,0,255)' or 'RGBA(255,0,255,255)

"""

print("mqtt-edu-kit.py > mqtt 'mqtt edu-kit' example")

from time import sleep
from machine import Pin
from utils.pinout import set_pinout
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt import MQTT
from components.led import Led
from components.rgb import Rgb
from components.button import Button
from gc import mem_free


print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
built_in_led = Led(pinout.BUILT_IN_LED)

num_neo = 16 # 30 # number of Leds
np = Rgb(pinout.WS_LED_PIN,neo) 

ws_r = 0
ws_g = 0
ws_b = 0

boot_pin = Pin(0, Pin.IN)
boot_button = Button(boot_pin, release_value=1)


def parse_rgba_msg(msg):
    """
    parse rgba message to dict from following formats:
    #ff00C3
    #ff00C3FF
    RGBA(255,0,200,255) or rgba(255,0,200,255)
    RGB(255,0,200,255) or rgb(255,0,200)
    [255,0,200,255]
    [255,0,200]
    """
    ret = {
        'RED': 0,
        'GREEN': 0,
        'BLUE': 0,
        'ALPHA': 0
    }

    if msg.startswith('#'):
        try:
            #ff00C3
            ret['RED'] = int(msg[1:3],16)
            ret['GREEN'] = int(msg[3:5],16)
            ret['BLUE'] = int(msg[5:7],16)
            try:
                # add alpha if present
                ret['ALPHA'] = int(msg[7:9],16)
            except (IndexError, ValueError):
                ret['ALPHA'] = 255
        except (IndexError, ValueError):
            pass
        else:
            return ret
    components = []
    if (msg.startswith('rgb(') or  msg.startswith('RGB(')) and msg.endswith(')'):
        components = msg[4:-1].split(',')
    if (msg.startswith('rgba(') or  msg.startswith('RGBA(')) and msg.endswith(')'):
        components = msg[5:-1].split(',')
    try:
        ret['RED'] = int(components[0])
        ret['GREEN'] = int(components[1])
        ret['BLUE'] = int(components[2])
        try:
            # add alpha if present
            ret['ALPHA'] = int(components[3])
        except (IndexError, ValueError):
            ret['ALPHA'] = 255

    except (IndexError, ValueError):
        pass
    else:
        return ret
    print("Unable to parse RGBA value", msg)
    return ret


def rgb_color(red,green,blue):
    for i in range(num_neo):
        np.color((red, green, blue),i)


def mqtt_handler(topic, msg):
    global press_togg
    print("MQTT handler {0}: {1}".format(topic, msg))
    if "led" in topic:
        data = bytes.decode(msg)
        print("led:", data)

        if data[0] == '1':  # on
            built_in_led.value(1)
            press_togg = 1
        elif data[0] == '0':  # off
            built_in_led.value(0)
            press_togg = 0
     
    if "rgb" in topic:
        # parse message to RGBA 0-255
        data = parse_rgba_msg(bytes.decode(msg))
        print("rgb:", data)
        rgb_color(data['RED'], data['GREEN'], data['BLUE'])


press_togg = 0
@boot_button.on_press
def boot_button_on_press():
    global press_togg
    print('boot_button_on_press')
    c.publish("octopus/device/{0}/button".format(m.client_id),str(press_togg))
    press_togg = int(not press_togg)
    built_in_led.value(press_togg)
    sleep(1)


@boot_button.on_long_press
def boot_button_on_long_press():
    print('boot_button_on_long_press')


print("--- wifi_connect >")
net = WiFiConnect()
net.connect()

print("--- mqtt_connnect >")
# c = mqtt_connect_from_config(esp_id)
m = MQTT.from_config()
c = m.client

c.set_callback(mqtt_handler)
c.connect()
c.subscribe("octopus/device/{0}/#".format(m.client_id))
 
print("testing blink")
built_in_led.value(1)
sleep(1)
built_in_led.value(0)

print("send alive message")
c.publish("octopus/device", m.client_id) # topic, message (value) to publish

print("--- RAM free ---> " + str(mem_free()))
print("--- main loop >")
while True:
    c.check_msg()
    # sleep(5)

