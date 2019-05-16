#octopusLAB - ESP32 - WiFi and WS RGB LED signalizationn - MQTT
#

import machine
import ubinascii
from time import sleep
from machine import Pin, Timer, PWM, SPI
from neopixel import NeoPixel
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config
from util.octopus_lib import *
from umqtt.simple import MQTTClient
from util.iot_garden import * # fade_
from onewire import OneWire
from ds18x20 import DS18X20

from util.pinout import set_pinout
pinout = set_pinout()

ver = "16.5.2019-v:0.2"
print("mqtt-slave.py > ESP32")
print(ver)

# Defaults - sensors
isTemp = 1          # temperature
isLight = 0         # light (lux)
isMois = 0          # moisture
isAD = 0            # AD input voltage
isADL = 0           # AD photoresistor
is7seg = 1          # max 8x7 segm.display

# hard-code config / daefault
Debug = True        # TODO: debugPrint()?
minute = 10         # 1/10 for data send
timeInterval = 1
wifi_retries = 100  # for wifi connecting

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)
pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
fet = Pin(pinout.MFET_PIN, Pin.OUT)
rel = Pin(pinout.RELAY_PIN, Pin.OUT)

rtc = machine.RTC() # real time
tim1 = Timer(0)     # for main 10 sec timer

esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)

np = NeoPixel(pin_ws, 1)
ws_r = 0
ws_g = 0
ws_b = 0

bd = bytes.decode

ts = []
if isTemp:
    print("init dallas temp >")
    try:
        ds = DS18X20(OneWire(dspin))
        ts = ds.scan()

        if len(ts) <= 0:
            isTemp = False

        for t in ts:
            print(" --{0}".format(bytearrayToHexString(t)))
    except:
        isTemp = False
    print("Found {0} dallas sensors, temp active: {1}".format(len(ts), isTemp))

def getTemp():
    tw=999
    if isTemp:
        ds.convert_temp()
        sleep_ms(750)
        for t in ts:
            temp = ds.read_temp(t)
            tw = int(temp*10)
    return tw        

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

if is7seg:
    from lib.max7219_8digit import Display
    # spi
    try:
        #spi.deinit()
        #print("spi > close")
        spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
        ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
        d7 = Display(spi, ss)
    except:
        print("spi.ERR")

def simple_blink():
    pin_led.value(0)
    sleep(0.1)
    pin_led.value(1)
    sleep(0.1) 

def fade_sw_in(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(0)
          time.sleep_us((r-i)*m*2) # multH/L *2
          p.value(1)
          time.sleep_us(i*m)

def fade_sw_out(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(1)
          time.sleep_us((r-i)*m)
          p.value(0)
          time.sleep_us(i*m*2)      

def test7seg():     
     d7.write_to_buffer('octopus')
     d7.display()

def sendData():
    print("sendData()") 
    if isTemp:  
        temp10 = int(ts.read_temp()*10)
        publishTopic = "octopus/{0}/temp/{1}".format(esp_id,temp)
        print(str("publishTopic: ".publishTopic))        
        c.publish("/octopus/device/{0}/temp/".format(esp_id),str(temp10/10))      

it = 0 # every 10 sec.
def timerSend():
    global it
    it = it+1
    if Debug: print(">"+str(it))

    if is7seg:
        if isTemp:
            d7.write_to_buffer(str(it)+"-"+str(int(getTemp())))
            d7.display()    

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    #np[0] = (0, 128, 0)
    #np.write()
    simple_blink()
    print(sta.ifconfig())


def connecting_callback(retries):
    #np[0] = (0, 0, 128)
    #np.write()
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
            #c.publish(mqtt_root_topic+esp_id,1)

        elif data[0] == 'F':  # ofF 
            print("-> off")
            pin_led.value(0) 
            #c.publish(mqtt_root_topic+esp_id,0)

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

    if "pwm" in topic:
        data = bd(msg)   

        if data[0] == '1':
           #pwm = int(data[1:])
            print("led1 - pwm fade in >")
            fade_sw_in(fet,500,5)
            #fet.value(1) 

        if data[0] == '0':
           #pwm = int(data[1:])
            print("led0 - pwm fade out >")
            fade_sw_out(fet,500,5) 
            #fet.value(0)    

    if "8x7seg" in topic:
        data = bd(msg)  
        try:
            d7.write_to_buffer(data)
            d7.display() 
        except:
               print("mqtt.8x7seg.ERR")     
                
# Default WS led light RED as init
np[0] = (100, 0, 0)
np.write()
simple_blink()
simple_blink()
np[0] = (0, 0, 0)
np.write()        

print("init i/o >")
if is7seg:
    test7seg() 

print("wifi_config >")
wifi_config = read_wifi_config()
wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else 250 )
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
print("wifi.connect >")
wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])

# url config: TODO > extern.

print("mqtt_config >")
mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]
#mqtt_ssl  = False # Consider to use TLS!
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]

mqtt_clientid = mqtt_clientid_prefix + esp_id
#c = MQTTClient(mqtt_clientid, mqtt_host, ssl=mqtt_ssl)
c = MQTTClient(mqtt_clientid, mqtt_host)
c.set_callback(mqtt_sub)
print("mqtt.connect > ")
c.connect()
# c.subscribe("/octopus/device/{0}/#".format(esp_id))

subStr = mqtt_root_topic+"/"+esp_id+"/#"
print("subscribe (root topic + esp id):" + subStr)
c.subscribe(subStr)

print("mqtt log")
# mqtt_root_topic_temp = "octopus/device"
c.publish(mqtt_root_topic,esp_id) # topic, message (value) to publish

# timeSetup()
timerInit()

print("test temp: " + str(getTemp()))

print("> loop:")
while True:
    c.check_msg()