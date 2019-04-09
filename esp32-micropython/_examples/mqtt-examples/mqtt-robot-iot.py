# octopusLAB - ESP32 - MQTT
# robotBoard / IoTboard > testing
#
"""
import upip
upip.install('micropython-umqtt.robust')
"""
ver = "0.1" 
# last update 9.4.2019

from time import sleep
from machine import Pin, Timer
from neopixel import NeoPixel
import machine
import ubinascii
from util.octopus_lib import *
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config
from util.pinout import set_pinout
from umqtt.simple import MQTTClient
from lib.temperature import TemperatureSensor  

printLog(1,"boot device >")
pinout = set_pinout()

pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
esp_id = ubinascii.hexlify(machine.unique_id()).decode()
rel = Pin(pinout.RELAY_PIN, Pin.OUT)

rtc = machine.RTC() # real time
tim1 = Timer(0)     # for main 10 sec timer
bd = bytes.decode

np = NeoPixel(pin_ws, 1)
ws_r = 0
ws_g = 0
ws_b = 0

printLog(2,"init - variables and functions >")

# hard-code config / daefault
Debug = True        # TODO: debugPrint()?
minute = 10         # 1/10 for data send
timeInterval = 1
wifi_retries = 100  # for wifi connecting

# Defaults - sensors
isTemp = 1          # temperature
isLight = 0         # light (lux)
isMois = 0          # moisture
isAD = 0            # AD input voltage
isADL = 0           # AD photoresistor

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)

mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_ssl  = False # Consider to use TLS!

print("mqtt-robot-iot.py > second IoT test")
print("ver. "+ver)                 
print("id: "+ esp_id)

# url config: TODO > extern.
urlApi ="http://www.octopusengine.org/api/hydrop/"

def simple_blink():
    pin_led.value(1)
    sleep(0.1)
    pin_led.value(0)
    sleep(0.1)

# Default WS led light RED as init
np[0] = (128, 0, 0)
np.write()
simple_blink()

it = 0 # every 10 sec.
def timerSend():
    global it
    it = it+1
    if Debug: print(">"+str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0

def timerInit():
    tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerSend())         

def timeSetup():
    if Debug: print("time setup >")
    urltime=urlApi+"/get-datetime.php"
    try:
        response = urequests.get(urltime)
        dt_str = (response.text+(",0,0")).split(",")
        print(str(dt_str))
        dt_int = [int(numeric_string) for numeric_string in dt_str]
        rtc.init(dt_int)
        print(str(rtc.datetime()))
    except:
        print("Err. Setup time from WiFi")

def sendData():
    print("sendData()") 
    if isTemp:  
        temp10 = int(ts.read_temp()*10)
        #publishTopic = "/octopus/device/{0}/temp/{1}".format(esp_id,temp)
        #print(str("publishTopic: ".publishTopic))
        c.publish("/octopus/device/{0}/temp/".format(esp_id),str(temp10/10)) 

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    np[0] = (0, 128, 0)
    np.write()
    simple_blink()
    print(sta.ifconfig())

def connecting_callback(retries):
    np[0] = (0, 0, 128)
    np.write()
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

        np[0] = (ws_r, ws_g, ws_b)
        np.write()

    if "relay" in topic:
        data = bd(msg)   

        if data[0] == 'N':  # oN
            print("R > on")
            rel.value(1)
        elif data[0] == 'F':  # ofF 
            print("R > off")
            rel.value(0) 

        np[0] = (ws_r, ws_g, ws_b)
        np.write()   

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

print("mqtt log and test blink")
c.publish("log: /octopus/device/",esp_id) # topic, message (value) to publish
simple_blink()

timeSetup()
timerInit()
#displMessage("IoT",1)

if isTemp:
    print("test temperature > sendData()")
    ts = TemperatureSensor(pinout.ONE_WIRE_PIN)
    temp = ts.read_temp()
    # print to console
    print(temp)
    sendData() 

printLog(3,"start main loop >")

while True:
    c.check_msg()