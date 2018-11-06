# include this in boot.py or main.py as WIFIC
# and call WIFIconnect.do_connect() from the boot.py or main.py

# Don't forget to change the ssid and password under second comment

# Includes
import network
from time import sleep


def do_connect(ssid, password):
    # get an instance of the sta_if WiFi interface
    sta_if = network.WLAN(network.STA_IF)

    # check if we are already connected to a WiFi
    if sta_if.isconnected():
        print("Already connected")
        return

        # activate interface
    sta_if.active(True)

    # connect to network via provided ID
    print('connecting to "{}" network...'.format(ssid))
    sta_if.connect(ssid, password)

    while not sta_if.isconnected():
        print("  -- Waiting to connect")
        sleep(0.5)

    # print connection info - automatic
    # currently this prints out as if no connection was established - giving 0.0.0.0 sd ip
    # however, connection IS made and functional
    print('network config:', sta_if.ifconfig())

    # simple newline to separate from base information during boot
    print('')
