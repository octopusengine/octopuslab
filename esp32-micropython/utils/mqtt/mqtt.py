__version__ = "0.1.0"

import machine, ubinascii
from umqtt.simple import MQTTClient


class MQTT():
    def __init__(self, broker, ssl, username, password, prefix='', client_id=None):
        if client_id is None:
            client_id = ubinascii.hexlify(machine.unique_id()).decode()
        self.client_id = client_id
        self.full_client_id = '{}{}'.format(prefix, client_id)
        print('Using MQTT client_id "{}", full_client_id "{}"'.format(self.client_id, self.full_client_id))
        self.broker = broker
        self.client = MQTTClient(self.full_client_id, self.broker, ssl=ssl, user=username, password=password)

    @classmethod
    def from_config(cls, config_name="mqtt"):
        '''
        If client_id is not provided, read machine unique id
        '''
        print('Reading MQTT configuration from {}.json'.format(config_name))

        from config import Config
        config = Config(config_name)

        murl = config.get("mqtt_broker")
        if not murl:
            raise ValueError("MQTT config error: `mqtt_broker` is not set. Check configuration file '{}.json'".format(config_name))
        mssl = config.get("mqtt_ssl")
        if mssl is None:
            mssl = 1  # enable ssl by default
        mssl = 1 if mssl else 0  # normalize vlue to 0/1
        musr = config.get("mqtt_user")
        if not musr:
            raise ValueError("MQTT config error: `mqtt_user` is not set. Check configuration file '{}.json'".format(config_name))
        ipsw = config.get("mqtt_pass")
        if not ipsw:
            raise ValueError("MQTT config error: `mqtt_pass` is not set. Check configuration file '{}.json'".format(config_name))
        mprefix = config.get("mqtt_client_prefix")
        if not mprefix:
            mprefix = ''
        mclientid = config.get("mqtt_client_id")
        # if not set, None will be passed to init and will drop to default id generated from device id
    
        return cls(murl, mssl, musr, ipsw, mprefix, mclientid)
