# basic example: octopusLAB - ESP32 - WiFi - MQTT
print("mqtt-btn-led.py > mqtt 'hello world' example")

from time import sleep
from machine import Pin
from utils.pinout import set_pinout
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.mqtt import MQTT
from components.led import Led
from components.button import Button
from gc import mem_free


print("--- RAM free ---> " + str(mem_free())) 

pinout = set_pinout()
built_in_led = Led(pinout.BUILT_IN_LED)


boot_pin = Pin(0, Pin.IN)
boot_button = Button(boot_pin, release_value=1)


def mqtt_handler(topic, msg):
    global press_togg
    print("MQTT handler {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:", end='')
        data = bytes.decode(msg)

        if data[0] == '1':  # oN
            print("-> on")
            built_in_led.value(1)
            press_togg = 1
        elif data[0] == '0':  # ofF 
            print("-> off")
            built_in_led.value(0)
            press_togg = 0

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
