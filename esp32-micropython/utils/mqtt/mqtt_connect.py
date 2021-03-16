# include this in boot.py or main.py as WiFiConnect
# from utils.mqtt.mqtt_connect import read_mqtt_config

"""
1) install mqtt:
connect to wifi
>>> import upip
>>> upip.install('micropython-umqtt.robust')
2) setup:
>>> setup()
> mqtt config

usage:
from utils.mqtt.mqtt_connect import read_mqtt_config
b = read_mqtt_config()["mqtt_broker_ip"]

TODO: connect()
mqtt_clientid = mqtt_clientid_prefix + esp_id

c = MQTTClient(mqtt_clientid, mqtt_host)
c.set_callback(mqtt_sub)
c.connect()

3) config
from config import Config
conf = Config("mqtt") > config/mqtt.json
...

"""
import json, ujson  # suspicious?

def read_mqtt_config():
    # TODO file does not exist
    f = open('config/mqtt.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)
