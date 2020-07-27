
import esp32
from time import sleep

from components.iot import Thermometer
from utils.database.influxdb import InfluxDB
from utils.octopus import disp7_init
from utils.wifi_connect import WiFiConnect
from time import sleep

READ_RATE = 30  # per minute
SEND_RATE = 1  # per minute

ts = Thermometer()
disp7 = disp7_init()

net = WiFiConnect()
net.connect()

influx = InfluxDB.fromconfig()

c = 0
while True:
    temp  = ts.get_temp()
    print("Temperature {}".format(temp))
    disp7.show(temp)

    c = c % (60 // SEND_RATE)
    if c == 0:
        print("InfluxDB write")
        influx.write(temperature=temp)

    sleep(60 // READ_RATE)
    c += 1
