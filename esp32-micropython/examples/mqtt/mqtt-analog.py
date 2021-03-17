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
from components.led import Led

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)

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


def simple_blink():
    led.value(1)
    sleep(0.25)
    led.value(0)
    sleep(0.25)


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

# =====================================================

print("wifi_connect >")
net = WiFiConnect()
net.connect()

print("mqtt_config >")
mqtt_client_id_prefix = read_mqtt_config()["mqtt_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_user = read_mqtt_config()["mqtt_user"]
mqtt_psw = read_mqtt_config()["mqtt_psw"]
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]
mqtt_client_id = mqtt_client_id_prefix + esp_id

c = MQTTClient(mqtt_client_id, mqtt_host,ssl=mqtt_ssl,user=mqtt_user,password=mqtt_psw)
c.set_callback(mqtt_sub)
c.connect()


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
