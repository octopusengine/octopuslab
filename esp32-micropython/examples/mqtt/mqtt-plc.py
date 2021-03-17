# PLC example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')
"""
from time import sleep
from machine import Pin
import machine, ubinascii
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt.mqtt_connect import read_mqtt_config
from umqtt.simple import MQTTClient
from utils.pinout import set_pinout
from utils.wifi_connect import WiFiConnect
from gc import mem_free
from utils.octopus_lib import i2c_init
from components.i2c_expander import Expander8
from utils.bits import neg, reverse, int2bin, get_bit, set_bit
from components.lm75 import LM75B
bd = bytes.decode

def ram_free():
	print("--- RAM free ---> " + str(mem_free())) 

print("mqtt-led.py > mqtt 'PLC' example")
ram_free()
pinout = set_pinout()
esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)


def simple_blink():
    exp8.write_8bit(set_bit(255,OUT1,0))
    sleep(0.2)
    exp8.write_8bit(set_bit(255,OUT1,1))
    sleep(0.2)


def mqtt_sub(topic, msg):
    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:")
        data = bd(msg)

        if data[0] == 'N':  # oN
            print("-> on")
            # led.value(1)
            exp8.write_8bit(set_bit(255,OUT1,0))
        elif data[0] == 'F':  # ofF 
            print("-> off")
            # led.value(0)
            exp8.write_8bit(set_bit(255,OUT1,1)) 

print("--- PLC shield ---")
print("-"*50)

print("- I2C:")
i2c = i2c_init(True,200)
print(i2c.scan())
# 34 expander / 73 therm. / 84 eeprom

lm = LM75B(i2c)
temp = lm.get_temp()
sleep(1)
print("- Temp: ", temp)

exp8 = Expander8(34,i2c)
IN1, IN2, IN3, IN4     = 0, 1, 2, 3
OUT1, OUT2, OUT3, OUT4 = 4, 5, 6, 7
print("- PCF:", exp8.read())

# bits4 = "0101"
# exp8.write_8bit(bits4)

for i in range(3):
    exp8.write_8bit(0)
    sleep(0.1)
    exp8.write_8bit(255)
    sleep(0.1)


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
c.subscribe("octopus/device/{0}/#".format(esp_id))

print("mqtt log and test blink")
print(c.publish("octopus/device/log",esp_id)) # topic, message (value) to publish
simple_blink()

ram_free()
print("> loop:")
while True:
    c.check_msg()
