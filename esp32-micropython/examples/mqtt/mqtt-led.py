# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')
"""
print("mqtt-led.py > mqtt 'hello world' example")

from time import sleep
from machine import Pin
import machine
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt.mqtt_connect import read_mqtt_config
from umqtt.simple import MQTTClient
import ubinascii
from util.pinout import set_pinout


pinout = set_pinout()
pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)
esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)

bd = bytes.decode

mqtt_clientid_prefix = "CHANGE PREFIX"
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_ssl  = True # Consider to use TLS!

def simple_blink():
    pin_led.value(1)
    sleep(0.5)
    pin_led.value(0)
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
            pin_led.value(1)
        elif data[0] == 'F':  # ofF 
            print("-> off")
            pin_led.value(0) 

print("wifi_config >")
wifi_config = read_wifi_config()
wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else 250 )
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])

print("mqtt_config >")
mqtt_clientid = mqtt_clientid_prefix + esp_id

c = MQTTClient(mqtt_clientid, mqtt_host)
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
