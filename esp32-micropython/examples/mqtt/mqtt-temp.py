# basic example: octopusLAB - ESP32 - WiFi - MQTT
print("mqtt Temperature sensor example")

from time import sleep
import machine, ubinascii
from machine import Timer
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt import MQTT
# from umqtt.simple import MQTTClient
from utils.pinout import set_pinout
from components.led import Led
from utils.octopus import disp7_init
from components.iot import Thermometer
from gc import mem_free

bd = bytes.decode
print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
led = Led(pinout.BUILT_IN_LED)
ts = Thermometer()
# d7 = disp7_init()       # 8 x 7segment display init

esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)


def simple_blink():
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


timer_interval = 1 # minutes
it = 0 # every 10 sec.

def timer10s():
    global it
    it += 1
    print(">" + str(it))

    if (it == 6*timer_interval): # 6 = 1min / 60 = 10min 
        try:
           temp = ts.get_temp()
           print("temp:", temp)
           c.publish("octopus/device/" + esp_id + "/temp1",str(temp)) # topic, message (value) to publish
        except Exception as e:
           print("config Exception: {0}".format(e))
        it = 0


def mqtt_handler(topic, msg):
    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:")
        data = bd(msg)

        if data[0] == '1':  # on
            print("-> on")
            led.value(1)
        elif data[0] == '0':  # off
            print("-> off")
            led.value(0) 
    
    if "disp7" in topic:
        print("disp7:")
        data = bd(msg)
        # d7.show(data)
        

print("--- wifi_connect >")
net = WiFiConnect()
net.connect()

print("--- timer init >")
tim1 = Timer(0)
print("for stop: tim1.deinit()")
tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timer10s())

print("--- mqtt_connnect >")
m = MQTT.from_config()
c = m.client

c.set_callback(mqtt_handler)
c.connect()
c.subscribe("octopus/device/{0}/#".format(esp_id))
 
print("mqtt log and test blink")
c.publish("octopus/device",esp_id) # topic, message (value) to publish
simple_blink()

print("--- RAM free ---> " + str(mem_free()))
print("--- main loop >")
while True:
    c.check_msg()
