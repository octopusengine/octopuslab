import network
import time
from machine import Pin
from umqtt.robust import MQTTClient
from util.setup import setup

a1 = Pin(26,Pin.OUT)
a2 = Pin(12,Pin.OUT)
a12 = Pin(25,Pin.OUT)
a3 = Pin(14,Pin.OUT)
a4 = Pin(27,Pin.OUT)
a34 = Pin(13,Pin.OUT)
a1.value(0)
a2.value(0)
a12.value(1)
a3.value(0)
a4.value(0)
a34.value(1)

w = network.WLAN()
w.active(1)
w.connect("ssid", "psw")

while not w.isconnected():
    print(".")
    time.sleep_ms(250)

def mq_cb(topic, msg):
    if (msg == b"back"):
        a1.value(1)
        a2.value(0)
        a3.value(1)
        a4.value(0)
    if (msg == b"forward"):
        a1.value(0)
        a2.value(1)
        a3.value(0)
        a4.value(1)
    if (msg == b"right"):
        a1.value(1)
        a2.value(0)
        a3.value(0)
        a4.value(1)
    if (msg == b"left"):
        a1.value(0)
        a2.value(1)
        a3.value(1)
        a4.value(0)
    if (msg == b"stop"):
        a1.value(0)
        a2.value(0)
        a3.value(0)
        a4.value(0)

client = MQTTClient("", "ip")
client.connect()

client.set_callback(mq_cb)
client.subscribe('node/car')

while True:
    client.check_msg()