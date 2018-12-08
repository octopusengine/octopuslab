# Demo to connect fo WiFi and blink BUILTIN led due connecting
# OctopusLAB 2018
# Usage
# to run this example use either
# ampy put 08-blink-wifi main.py
# or
# ampy put 08-blink-wifi
# and then run from REPL by using
# __import__('08-blink-wifi')

# Include wifi
from WiFiConnect import WiFiConnect

# Remember set SSID and password in WiFiConfig.py file
import WiFiConfig

# Include machine GPIO
from machine import Pin
from time import sleep

# Import OctopusLab Robot board definition file
import octopus_robot_board as o # octopusLab main library - "o" < octopus

# Set up LED
led = Pin(o.BUILT_IN_LED, Pin.OUT)

# Turn off led by default
led.value(0)


# Define function callback for connecting event
def led_blink_connecting_callback():
    for _ in range(0, 2):
        led.value(1)
        sleep(0.1)
        led.value(0)
        sleep(0.1)


# Define function callback for connecting event
def led_blink_connected_callback(sta):
    led.value(1)


def print_connected_callback(sta):
    print(sta.ifconfig())


w = WiFiConnect()
w.events_add_connecting(led_blink_connecting_callback)
w.events_add_connected(print_connected_callback)
w.events_add_connected(led_blink_connected_callback)

w.connect(WiFiConfig.WIFI_SSID, WiFiConfig.WIFI_PASS)
