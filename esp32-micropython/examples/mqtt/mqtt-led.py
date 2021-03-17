# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')
"""
print("mqtt-led.py > mqtt 'hello world' example")

from time import sleep
import machine, ubinascii
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt.mqtt_connect import mqtt_connect_from_config
# from umqtt.simple import MQTTClient
from utils.pinout import set_pinout
from components.led import Led
from gc import mem_free

bd = bytes.decode
print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)

esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)


def simple_blink():
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


def mqtt_sub(topic, msg):
    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:")
        data = bd(msg)

        if data[0] == 'N':  # oN
            print("-> on")
            led.value(1)
        elif data[0] == 'F':  # ofF 
            print("-> off")
            led.value(0) 


print("--- wifi_connect >")
net = WiFiConnect()
net.connect()

print("--- mqtt_connnect >")
c = mqtt_connect_from_config(esp_id)

c.set_callback(mqtt_sub)
c.connect()
c.subscribe("octopus/device/{0}/#".format(esp_id))
 
print("mqtt log and test blink")
c.publish("octopus/device",esp_id) # topic, message (value) to publish
simple_blink()

print("--- RAM free ---> " + str(mem_free()))
print("--- main loop >")
while True:
    c.check_msg()
