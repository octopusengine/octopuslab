# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')

install into lib esp8266_i2c_lcd and lcd_api
https://github.com/dhylands/python_lcd
"""
print("mqtt-lcd1602.py > mqtt 'hello world' example")

from time import sleep
from machine import Pin
import machine
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config

from umqtt.simple import MQTTClient
import ubinascii

from util.pinout import set_pinout
pinout = set_pinout()

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)

from lib.esp8266_i2c_lcd import I2cLcd
LCD_ADDRESS=0x27
LCD_ROWS=2
LCD_COLS=16

# Set up I2C
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN), freq=100000) # 100kHz because PCF is slow

if not 0x27 in i2c.scan():
    print("I2C LCD display not found!")
    raise Exception("No device")

lcd = I2cLcd(i2c, LCD_ADDRESS, LCD_ROWS, LCD_COLS)

esp_id = ubinascii.hexlify(machine.unique_id()).decode()                 
print(esp_id)

lcd.clear()
lcd.putstr("MQTT LCD")
lcd.move_to(0, 1)
lcd.putstr("ID:{0}".format(esp_id))

bd = bytes.decode

mqtt_clientid_prefix = "CHANGE PREFIX"
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_ssl  = True # TODO: put to config

def simple_blink():
    pin_led.value(1)
    sleep(0.25)
    pin_led.value(0)
    sleep(0.25)

def simple_blink_wifilcd():
    lcd.move_to(15, 0)
    lcd.putchar("W")
    sleep(0.5)
    lcd.move_to(15, 0)
    lcd.putchar(" ")
    sleep(0.5)

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    print(sta.ifconfig())
    lcd.move_to(15, 0)
    lcd.putchar("W")

def connecting_callback(retries):
    simple_blink()
    simple_blink_wifilcd()

def mqtt_sub(topic, msg):    
    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "lcd/clear" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        lcd.clear()

    if "lcd/rawtext" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        lcd.clear()
        lcd.putstr(data)

    if "lcd/line1text" in topic:
        data = bd(msg)
        print("line 1 text: {0}".format(data))
        lcd.move_to(0, 0)
        lcd.putstr(data[:LCD_COLS])

    if "lcd/line2text" in topic:
        data = bd(msg)
        print("line 2 text: {0}".format(data))
        lcd.move_to(0, 1)
        lcd.putstr(data[:LCD_COLS])

    if "lcd/write" in topic:
        data = bd(msg)
        print("text: {0}".format(data))
        lcd.putstr(data)

    if "lcd/set_cursor" in topic:
        data = bd(msg)
        x=0
        y=0
        print("Cursor set: {0}".format(data))
        try:
            if "x" in data:
                x = int(data.split('x')[0])
                y = int(data.split('x')[1])
            else:
                y = int(data)

            lcd.move_to(x, y)

        except Exception as e:
            print("Error parse message")
            print(e)


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

lcd.move_to(14, 0)

try:
    if c.connect() == 0:
        subStr = mqtt_root_topic+esp_id+"/#"
        c.subscribe(subStr)

        print("mqtt log")
        c.publish(mqtt_root_topic,esp_id) # topic, message (value) to publish

        simple_blink()
        lcd.putchar("M")

    else:
        lcd.putchar("E")
except Exception as e:
    print("Error connecting to MQTT")
    lcd.putchar("E")


print("> loop:")
while True:
    c.check_msg()
