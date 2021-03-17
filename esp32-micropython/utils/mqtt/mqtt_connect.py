# micropython-umqtt.robust

import json, ujson  # suspicious?
from umqtt.simple import MQTTClient


def read_mqtt_config():
    # TODO file does not exist
    f = open('config/mqtt.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)


def mqtt_connect_from_config(esp_id="undefined"):
    mqtt_config = read_mqtt_config()

    mqtt_client_id_prefix = mqtt_config["mqtt_prefix"]
    mqtt_host = mqtt_config["mqtt_broker_ip"]
    mqtt_user = mqtt_config["mqtt_user"]
    mqtt_psw =  mqtt_config["mqtt_psw"]
    mqtt_ssl  = mqtt_config["mqtt_ssl"]

    mqtt_client_id = mqtt_client_id_prefix + esp_id

    c = MQTTClient(mqtt_client_id, mqtt_host,ssl=mqtt_ssl,user=mqtt_user,password=mqtt_psw)
    return c
