# Copyright OctopusLAB 2022
# MIT License
__version__ = "1.0.1"
__license__ = "MIT"


# Includes
import network
from time import sleep_ms
from sensobox.config import get_config

class Network:
    def __init__(self, retries = 0):
        self._sta_if = network.WLAN(network.STA_IF)
        self._ap_if = network.WLAN(network.AP_IF)
        self._events_connecting = []
        self._events_connected = []
        self._events_disconnected = []
        self._events_timeout = []
        self._retries = retries
        self._connected = False
        self._networks = get_config().get('wifi_networks', [])


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

        available_networks = []
        scanned_networks = self._sta_if.scan()
        for n in scanned_networks:
            available_networks.append(n[0].decode())

        # Try find known / saved network and connect to it
        for n in self._networks:
            if n.get('ssid') in available_networks:
                if self._connect(n.get('ssid'), n.get('psk')):
                    return True

        # Return false if we was not able to connect to any saved network
        return False


    @property
    def connected(self):
        return self._sta_if.isconnected()


    def is_connected(self):
        return self.connected


    def handle_wifi(self):
        if self._connected and not self.connected:
            self._connected = False
            self._call_events_disconnected()

        if not self._connected and self.connected:
            self._connected = True
            self._call_events_connected(self._sta_if)

