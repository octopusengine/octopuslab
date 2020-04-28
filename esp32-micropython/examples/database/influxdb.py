# Influx DB Write counter example
# The MIT License (MIT)
# Copyright (c) 2017-2020 Jan Copak, Petr Kracik

from sys import exit
from time import sleep
from util.octopus import disp7_init
from machine import Pin, Timer, reset
from config import Config
from util.database.influxdb import InfluxDB
from util.wifi_connect import WiFiConnect

mem_free = gc.mem_free

keepalive=0
errorcount=0
reconnectcount=0

# Placeholder for influx instance
influx = None
net = None
display = None

config_setkeys = ["influx_url",
                  "influx_db",
                  "influx_user",
                  "influx_pass",
                  "influx_metric",
                  "influx_place"]

def timer30s():
    global errorcount
    global reconnectcount
    global keepalive
    print("Timer 30sec RUN")
    keepalive+=1

    print("Keepalive: {}, Error count: {}, Number of wifi reconnect: {}".format(keepalive, errorcount, reconnectcount))

    display.show("k{}".format(keepalive))
    if influx.write(keepalive=keepalive, errorcount=errorcount, reconnectcount=reconnectcount):
        errorcount = 0
    else:
        print("Error while sending to InfluxDb")
        errorcount+=1
        if errorcount > 4:
            print("Too much errors, reboot")
            reset()
        else:
            net.sta_if.disconnect()
            net.connect()
            reconnectcount+=1

        display.show("E{}r{}".format(errorcount, reconnectcount))


def timer_init(t):
    print("timer init > stop: tim1.deinit()")
    if influx is None:
        print("Influx not initialized. Check configuration")
        return

    t.init(period=30000, mode=Timer.PERIODIC, callback=lambda t:timer30s())


print("Press CTRL+C to skip booting")
for _ in range(0,3):
    print(".")
    sleep(1)


print("config/exampleinflux.json -->")
config = Config("exampleinflux", config_setkeys)

try:
    iurl = config.get("influx_url")
    idb = config.get("influx_db")
    iusr = config.get("influx_user")
    ipsw = config.get("influx_pass")
    imetric = config.get("influx_metric")
    iplace = config.get("influx_place")

    if iurl is None:
        raise Exception("Config error: InfluxDB URL is not set. Check configuration")

    if idb is None:
        raise Exception("Config error: InfluxDB Database is not set. Check configuration")
    
    if imetric is None:
        raise Exception("Config error: InfluxDB Metric is not set")
    

    influx = InfluxDB(iurl, idb, iusr, ipsw, imetric, place=iplace)
    print("influx: ", iurl, idb)
except Exception as e:
    print("config Exception: {0}".format(e))
    print("Use config.setup()")
    exit(1)

display = disp7_init()

display.show("wifiConn")
net = WiFiConnect()
net.connect()

display.show("timer on")
tim1 = Timer(0)     # for main 10 sec timer
timer_init(tim1)

# --- run ---
print("--- run --- RAM free: " + str(mem_free()))
