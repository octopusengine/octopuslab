import time
import machine
from machine import Pin, I2C
import network
from KeyPad_I2C import keypad
from umqtt.simple import MQTTClient
import ubinascii

# Configuration

wifi_ssid = "SSID"
wifi_pass = "PASS"

mqtt_clientid_prefix = ""
mqtt_host = "CHANGE_ME"
mqtt_ssl  = False # Consider to use TLS!

# Keyboard repeat timer
keyDelay = 250

esp_id = ubinascii.hexlify(machine.unique_id()).decode()

w = network.WLAN()
w.active(1)
w.connect(wifi_ssid, wifi_pass)

while not w.isconnected():
    print(".")
    time.sleep_ms(250)

def mqtt_sub(topic, msg):
    print("MQTT Topic {0}: {1}".format(topic, msg))

mqtt_clientid = mqtt_clientid_prefix + esp_id

c = MQTTClient(mqtt_clientid, mqtt_host)
c.set_callback(mqtt_sub)
c.connect()
c.subscribe("/octopus/device/{0}/#".format(esp_id))

i2c_sda = Pin(21, Pin.IN, Pin.PULL_UP)
i2c_scl = Pin(22, Pin.IN, Pin.PULL_UP)

i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000)

kp = keypad(i2c, 0x23)

lastKeyPress = 0

while True:
    c.check_msg()
 
    try:
        key = kp.getKey()
    except OSError as e:
        print(e)

    if key and time.ticks_ms() > lastKeyPress+keyDelay:
        lastKeyPress = time.ticks_ms()
        print(key)
        c.publish("/octopus/{0}/keypad/key".format(esp_id), key)
