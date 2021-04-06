# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')
"""
print("mqtt-led.py > mqtt 'hello world' example")

from time import sleep
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt import MQTT
from utils.pinout import set_pinout
from components.led import Led
from utils.octopus import disp7_init
from gc import mem_free
bd = bytes.decode


print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)
d7 = disp7_init() # 8 x 7segment display init

sleep(2)
for i in range(9):
    d7.show(10-i)
    sleep(0.2)
d7.show("")


def simple_blink():
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


def mqtt_handler(topic, msg):
    print("MQTT handler {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:", end='')
        data = bytes.decode(msg)

        if data[0] == 'N':  # oN
            print("-> on")
            led.value(1)
        elif data[0] == 'F':  # ofF 
            print("-> off")
            led.value(0)

    if "disp7" in topic:
        print("disp7:")
        data = bd(msg)
        d7.show(data)


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
simple_blink()

print("send alive message")
c.publish("octopus/device", m.client_id) # topic, message (value) to publish

print("--- RAM free ---> " + str(mem_free()))
print("--- main loop >")
while True:
    c.check_msg()
    # sleep(5)
