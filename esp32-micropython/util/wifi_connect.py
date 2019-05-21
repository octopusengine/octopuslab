# include this in boot.py or main.py as WiFiConnect

# Usage:
# from WiFiConnect import WiFiConnect
# w = WiFiConnect()
# w.events_add_connecting(function to callback connecting)
# w.events_add_connected(function to callback connected)
# w.connect(ssid, password)
#
# or add networks by
# w.add_network(ssid, password)
# and then use for connect to known networks
# w.connect()


# Includes
import network
import json
from time import sleep, sleep_ms

class WiFiConnect:
    def __init__(self, retries = 0):
        self.sta_if = network.WLAN(network.STA_IF)
        self.events_connecting = []
        self.events_connected = []
        self.events_disconnected = []
        self.events_timeout = []
        self.retries = retries
        self.__connected = False
        self.config = None
        try:
            self.load_config()

            # old config detection
            if not "networks" in self.config:
                # Upgrading to new version
                self.config['version'] = 2
                self.config['networks'] = dict()
                self.add_network(self.config['wifi_ssid'], self.config['wifi_pass'])

        except:
           self.config = dict()
           self.config['version'] = 2
           self.config['networks'] = dict()
           self.save_config()

    def __call_events_connecting__(self, retry):
        for f in self.events_connecting:
            f(retry)

    def __call_events_connected__(self, sta):
        for f in self.events_connected:
            f(sta)

    def __call_events_disconnected__(self):
        for f in self.events_disconnected:
            f()

    def __call_events_timeout__(self):
        for f in self.events_timeout:
            f()

    def __connect__(self, ssid, password):
        retry = 1

        # activate interface
        if not self.sta_if.active():
            self.sta_if.active(True)

        # connect to network via provided ID
        self.sta_if.connect(ssid, password)

        while not self.sta_if.isconnected():
            if retry == self.retries:
                break

            self.__call_events_connecting__(retry)
            retry+=1
            sleep_ms(100)
            

        # print connection info - automatic
        # currently this prints out as if no connection was established - giving 0.0.0.0 sd ip
        # however, connection IS made and functional
        self.__connected = self.sta_if.isconnected()

        if self.sta_if.isconnected():
            self.__call_events_connected__(self.sta_if)
            return True
        else:
            self.__call_events_timeout__()
            self.sta_if.active(False)
            return False

    def events_add_connecting(self, func):
        self.events_connecting.append(func)

    def events_add_connected(self, func):
        self.events_connected.append(func)

    def events_add_disconnected(self, func):
        self.events_disconnected.append(func)

    def events_add_timeout(self, func):
        self.events_timeout.append(func)

    def load_config(self):
         with open('config/wifi.json', 'r') as cfg_file:
            self.config = json.loads(cfg_file.read())

    def save_config(self):
        with open('config/wifi.json', 'w') as cfg_file:
            json.dump(self.config, cfg_file)

    def add_network(self, ssid, password):
        self.config['networks'][ssid] = password
        self.save_config()

    def remove_network(self, ssid):
        if ssid in self.config['networks']:
            del self.config['networks'][ssid]
            self.save_config()

    def connect(self, ssid=None, password=None):
        # check if we are already connected to a WiFi
        if self.sta_if.isconnected():
            self.__call_events_connected__(self.sta_if)
            return True

        # Backward compatibility
        if ssid is not None:
            return self.__connect__(ssid, password)

        if not self.sta_if.active():
            self.sta_if.active(1)

        nets = self.sta_if.scan()

        # Try find known / saved network and connect to it
        for n in nets:
            ssid = n[0].decode()
            if ssid in self.config['networks']:
                if self.__connect__(ssid, self.config['networks'][ssid]):
                    return True

        # Return false if we was not able to connect to any saved network
        return False

    def isconnected(self):
        return self.sta_if.isconnected()

    def handle_wifi(self):
        if self.__connected and not self.sta_if.isconnected():
            self.__connected = False
            self.__call_events_disconnected__()

        if not self.__connected and self.sta_if.isconnected():
            self.__connected = True
            self.__call_events_connected__(self.sta_if)


def read_wifi_config():
    print("==============WARNING==============")
    print("WARNING: This will be removed soon! ")
    print("==============WARNING==============")
    # TODO file does not exist
    f = open('config/wifi.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)
