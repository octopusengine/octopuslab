# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')

"""
print("mqtt-analog.py > mqtt 'hello world'")

from time import sleep, ticks_ms
from machine import Pin, ADC
import machine, time
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config
from umqtt.simple import MQTTClient
import ubinascii
from neopixel import NeoPixel
from util.pinout import set_pinout
pinout = set_pinout()

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)
pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
pin_analog = 36

adc = ADC(Pin(pin_analog))
adc.atten(ADC.ATTN_11DB)

ADC_SAMPLES=500
ADC_HYSTERESIS=50

esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)

np = NeoPixel(pin_ws, 1)
ws_r = 0
ws_g = 0
ws_b = 0
bd = bytes.decode

mqtt_clientid_prefix = read_mqtt_config()["mqtt_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]

def simple_blink():
    pin_led.value(1)
    sleep(0.25)
    pin_led.value(0)
    sleep(0.25)

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    print(sta.ifconfig())

def connecting_callback(retries):
    simple_blink()
          
def mqtt_sub(topic, msg):
    global ws_r
    global ws_g
    global ws_b

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

    if "wsled" in topic:
        data = bd(msg)
        if data[0] == 'R':
           ws_r = int(data[1:])
        elif data[0] == 'G':
           ws_g = int(data[1:])
        elif data[0] == 'B':
           ws_b = int(data[1:])
        if data[0] == '#':  
            ws_r = int(int(data[1:3], 16)/2)  
            ws_g = int(int(data[3:5], 16)/2)  
            ws_b = int(int(data[5:7], 16)/2)  
            
        np[0] = (ws_r, ws_g, ws_b)
        np.write()
    

print("wifi_config >")
wifi_config = read_wifi_config()
wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else 250 )
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])

print("mqtt_config >")
mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]

mqtt_clientid = mqtt_clientid_prefix + esp_id

c = MQTTClient(mqtt_clientid, mqtt_host, ssl=mqtt_ssl)
c.set_callback(mqtt_sub)


def get_adc_value():
    aval = 0

    for i in range(0, ADC_SAMPLES):
        aval += adc.read()

    return aval // ADC_SAMPLES


try:
    if c.connect() == 0:
        subStr = mqtt_root_topic+esp_id+"/#"
        c.subscribe(subStr)

        print("mqtt log")
        c.publish(mqtt_root_topic,esp_id) # topic, message (value) to publish

        simple_blink()

except Exception as e:
    print("Error connecting to MQTT")

aoldval=0

print("> loop:")
while True:
    c.check_msg()

    aval = get_adc_value()
    if abs(aoldval-aval) > ADC_HYSTERESIS:
        aoldval = aval
        print(aval)
        c.publish("octopus/{0}/adc/{1}".format(esp_id, pin_analog), str(aval))
