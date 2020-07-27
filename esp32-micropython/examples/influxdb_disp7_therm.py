"""
Example: reading temperature (DS18x20 on OneWire)
display current value on 7 segm. display and 
send data to InfluxDB as per config/influxdb.json
"""
from components.iot import Thermometer
from utils.database.influxdb import InfluxDB
from utils.octopus import disp7_init
from utils.wifi_connect import WiFiConnect
from time import sleep

ts = Thermometer()
disp7 = disp7_init()

net = WiFiConnect()
net.connect()

influx = InfluxDB.fromconfig()

while True:
    temp  = ts.get_temp()
    print("Temperature {}".format(temp))
    disp7.show(temp)
    influx.write(temperature=temp)
    sleep(5)
