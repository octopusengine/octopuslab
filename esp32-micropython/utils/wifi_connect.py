# Copyright OctopusLAB 2022
# MIT License
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

__version__ = "1.0.2"
__license__ = "MIT"


# Includes
import network
import json
from time import sleep, sleep_ms

class WiFiConnect:
    STA_IF = 0
    AP_IF = 1
    LAN_IF = 2

    def __init__(self, retries = 0):
        self._sta_if = network.WLAN(network.STA_IF)
        self._ap_if = network.WLAN(network.AP_IF)
        self._events_connecting = []
        self._events_connected = []
        self._events_disconnected = []
        self._events_timeout = []
        self._retries = retries
        self._connected = False
        self._config = None
        try:
            self.load_config()

            # old config detection
            if not "networks" in self._config:
                # Upgrading to new version
                self._config['version'] = 2
                self._config['networks'] = dict()

                ssid, psk = self._config['wifi_ssid'], self._config['wifi_pass']
                del self._config['wifi_ssid']
                del self._config['wifi_pass']
                self.save_config()
                self.add_network(ssid, psk)

        except Exception as e:
            self._config = dict()
            self._config['version'] = 2
            self._config['networks'] = dict()
            self.save_config()


    def _call_events_connecting(self, retry):
        for f in self._events_connecting:
            f(retry)


    def _call_events_connected(self, sta):
        for f in self._events_connected:
            f(sta)


    def _call_events_disconnected(self):
        for f in self._events_disconnected:
            f()


    def _call_events_timeout(self):
        for f in self._events_timeout:
            f()


    def _connect(self, ssid, password):
        retry = 1

        # activate interface
        if not self._sta_if.active():
            self._sta_if.active(True)

        # connect to network via provided ID
        self._sta_if.connect(ssid, password)

        while not self.connected:
            if retry == self._retries:
                break

            self._call_events_connecting(retry)
            retry+=1
            sleep_ms(100)


        # print connection info - automatic
        # currently this prints out as if no connection was established - giving 0.0.0.0 sd ip
        # however, connection IS made and functional
        self._connected = self.connected

        if self._sta_if.isconnected():
            self._call_events_connected(self._sta_if)
            return True
        else:
            self._call_events_timeout()
            self._sta_if.active(False)
            return False


    def events_add_connecting(self, func):
        self._events_connecting.append(func)


    def events_add_connected(self, func):
        self._events_connected.append(func)


    def events_add_disconnected(self, func):
        self._events_disconnected.append(func)


    def events_add_timeout(self, func):
        self._events_timeout.append(func)


    def load_config(self):
         with open('config/wifi.json', 'r') as cfg_file:
            self._config = json.loads(cfg_file.read())


    def save_config(self):
        with open('config/wifi.json', 'w') as cfg_file:
            json.dump(self._config, cfg_file)


    def add_network(self, ssid, password):
        self.load_config()
        self._config['networks'][ssid] = password
        self.save_config()


    def remove_network(self, ssid):
        self.load_config()
        if ssid in self._config['networks']:
            del self._config['networks'][ssid]
            self.save_config()


    def connect(self, ssid=None, password=None):
        # check if we are already connected to a WiFi
        if self._sta_if.isconnected():
            self._call_events_connected(self._sta_if)
            return True

        # Backward compatibility
        if ssid is not None:
            return self._connect(ssid, password)

        if not self._sta_if.active():
            self._sta_if.active(1)

        nets = self._sta_if.scan()

        # Try find known / saved network and connect to it
        for n in nets:
            ssid = n[0].decode()
            if ssid in self._config['networks']:
                if self._connect(ssid, self._config['networks'][ssid]):
                    return True

        # Return false if we was not able to connect to any saved network
        return False


    @property
    def ifconfig(self, interface=STA_IF):
        if interface == self.STA_IF:
            return self._sta_if.ifconfig()

        if interface == self.AP_IF:
            return self._ap_if.ifconfig()

        if interface == self.LAN_IF:
            raise NotImplementedError()

        raise ValueError()


    @property
    def connected(self):
        return self._sta_if.isconnected()


    def isconnected(self):
        print("Deprecated, use property connected")
        return self.connected


    def handle_wifi(self):
        if self._connected and not self.connected:
            self._connected = False
            self._call_events_disconnected()

        if not self._connected and self.connected:
            self._connected = True
            self._call_events_connected(self._sta_if)
