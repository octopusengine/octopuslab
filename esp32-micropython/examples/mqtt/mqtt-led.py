# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')
"""
print("mqtt-led.py > mqtt 'hello world' example")

from time import sleep
from machine import Pin
import machine, ubinascii
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt.mqtt_connect import read_mqtt_config
from umqtt.simple import MQTTClient
from utils.pinout import set_pinout
from components.led import Led
from utils.wifi_connect import WiFiConnect

bd = bytes.decode

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)

esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)

mqtt_client_id_prefix = read_mqtt_config()["mqtt_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_psw = read_mqtt_config()["mqtt_psw"]
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]


def simple_blink():
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    print(sta.ifconfig())

def connecting_callback(retries):
    simple_blink()


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

print("wifi_connect >")
net = WiFiConnect()
net.connect()

print("mqtt_config >")
mqtt_client_id = mqtt_client_id_prefix + esp_id

c = MQTTClient(mqtt_client_id, mqtt_host, password=mqtt_psw)

c.set_callback(mqtt_sub)
c.connect()
c.subscribe("/octopus/device/{0}/#".format(esp_id))

# 
print("mqtt log and test blink")
c.publish("log: /octopus/device/",esp_id) # topic, message (value) to publish
simple_blink()

print("> loop:")
while True:
    c.check_msg()
