from time import sleep
from machine import Pin
import usocket

import WiFiConfig  # Remember set SSID and password in WiFiConfig.py file
from WiFiConnect import WiFiConnect # Include wifi
from lib.microWebSrv import MicroWebSrv
# Import OctopusLab Robot board definition file
import octopus_robot_board as o # octopusLab main library - "o" < octopus

WSUDPPort = 12811
WSBindIP = None

# Robot Board v2 (and newer)
# pin_ws = Pin(o.WS_LED_PIN, Pin.OUT)
pin_led = Pin(o.BUILT_IN_LED, Pin.OUT)

def simple_blink():
    pin_led.value(1)
    sleep(0.1)
    pin_led.value(0)
    sleep(0.1)
simple_blink()

# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    simple_blink()
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    simple_blink()

w = WiFiConnect()
w.events_add_connecting(connecting_callback)
w.events_add_connected(connected_callback)
w.connect(WiFiConfig.WIFI_SSID, WiFiConfig.WIFI_PASS)

print("-----init-web-server-----")
# ---------------------------------------------------
"""
def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback
def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")
"""
# ---------------------------------------------------
print("start-wwwesp")
srv = MicroWebSrv(webPath='wwwesp/') #directory for your www
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
#srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=False)
# ---------------------------------------------------
