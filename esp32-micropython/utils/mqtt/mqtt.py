# function mqtt() for octopuLAB boards
# user is questioned in interactive mode
# from utils.mqtt import mqtt

#TODO DRY for filename
import machine, time, uos, ubinascii, ujson
from umqtt.simple import MQTTClient
from utils.mqtt_connect import read_mqtt_config
from utils.wifi_connect import read_wifi_config, WiFiConnect
from utils.pinout import set_pinout
ver = "0.23 / 5.7.2019"
esp_id = ubinascii.hexlify(machine.unique_id()).decode()

pinout = set_pinout()
pin_led = machine.Pin(pinout.BUILT_IN_LED, machine.Pin.OUT)
wifi_retries = 100  # for wifi connecting

def mainOctopus():
    from utils.Setup import mainOctopus as printOctopus
    printOctopus()

def simple_blink():
    pin_led.value(0)
    time.sleep(0.1)
    pin_led.value(1)
    time.sleep(0.1)     

def setupMenu():
    print()
    print('=' * 30)
    print('      M Q T T    S E T U P')
    print('=' * 30)
    print("[ms]  - mqtt broker and topics setup")
    print("[cv]  - set communications variables")
    print("[mt]  - mqtt simple test")
    print("[si]  - system info")
    print("[x]   - exit mqtt setup")

    print('=' * 30)
    sel = input("select: ")
    return sel

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

def mqtt():
    mainOctopus()
    print("Hello, this will help you initialize MQTT client")
    print("ver: " + ver + " (c)octopusLAB")
    print("id: " + esp_id)
    print("Press Ctrl+C to abort")
    
    # TODO improve this
    # prepare directory
    if 'config' not in uos.listdir():
       uos.makedirs('config')

    run= True
    while run:
        sele = setupMenu()

        if sele == "x":
            print("Setup - exit >")
            time.sleep_ms(2000)
            print("all OK, press CTRL+D to soft reboot")
            run = False

        if sele == "si": #system_info()
            from utils.sys_info import sys_info
            sys_info()

        if sele == "cv":
            print("------- Set 0/1/str for settings ------")
            wc = {}
            wc['name'] = input("device (host)name/describe: ")
            wc['time'] = int(input("get time from server? [1/0]: "))
            wc['mysql'] = int(input("send data to mysql db [1/0]: "))
            if wc['mysql']: wc['mysqlURL'] = input("mysql Write URL: ") 
            wc['mqtt'] = int(input("mqtt client [1/0]: "))
            wc['influx'] = int(input("send data to influx db [1/0]: "))
            if wc['influx']: wc['influxWriteURL'] = input("influx Write URL: ") 
            wc['timer'] = int(input("timer: "))            
                
            print("Writing to file config/mqtt_io.json")
            with open('config/mqtt_io.json', 'w') as f:
                ujson.dump(wc, f)

        if sele == "ms":
            print("Set mqtt >")
            print()
            mq = {}
            mq['mqtt_broker_ip'] = input("BROKER IP: ")
            mq['mqtt_ssl'] = int(input("> SSL (0/1): "))
            mq['mqtt_port'] = int(input("> PORT (1883/8883/?): "))
            mq['mqtt_clientid_prefix'] = input("CLIENT PREFIX: ")
            mq_user = input("Username: ")
            mq['mqtt_user'] = None if mq_user == "" else mq_user
            mq_pass = input("Password: ")
            mq['mqtt_pass'] = None if mq_pass == "" else mq_pass
            mq['mqtt_root_topic'] = input("ROOT TOPIC: ")

            print("Writing to file config/mqtt.json")
            with open('config/mqtt.json', 'w') as f:
                ujson.dump(mq, f)

        def mqtt_sub(topic, msg):  
            print("MQTT Topic {0}: {1}".format(topic, msg))                

        if sele == "mt":
            print("mqtt simple test:")   

            print("wifi_config >")
            wifi = WiFiConnect(250)
            wifi.events_add_connecting(connecting_callback)
            wifi.events_add_connected(connected_callback)
            print("wifi.connect")
            wifi_status = wifi.connect()

            # url config: TODO > extern.

            print("mqtt_config >")
            mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
            mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
            mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]
            mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]
            mqtt_user = read_mqtt_config()["mqtt_user"]
            mqtt_pass = read_mqtt_config()["mqtt_pass"]

            mqtt_clientid = mqtt_clientid_prefix + esp_id
            c = MQTTClient(mqtt_clientid, mqtt_host, ssl=mqtt_ssl, user=mqtt_user, password=mqtt_pass)
            c.set_callback(mqtt_sub)
            print("mqtt.connect to " + mqtt_host)
            c.connect()
            """
            # c.subscribe("/octopus/device/{0}/#".format(esp_id))
            subStr = mqtt_root_topic+"/"+esp_id+"/#"
            print("subscribe (root topic + esp id):" + subStr)
            c.subscribe(subStr)
            """

            mqtt_log_topic = mqtt_root_topic+"/log"
            print("mqtt log > " + mqtt_log_topic)
           
            print(mqtt_log_topic)
            # mqtt_root_topic_temp = "octopus/device"
            c.publish(mqtt_log_topic,esp_id) # topic, message (value) to publish      

   
