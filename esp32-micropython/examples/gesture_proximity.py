# from https://github.com/liske/python-apds9960/blob/master/micropython/test_prox.py
# Copyright Thomas Liske 2018
# GPLv3

from time import sleep
from utils.octopus import i2c_init
from lib.apds9960 import uAPDS9960 as APDS9960

i2c = i2c_init()

apds = APDS9960(i2c, valid_id=[0x30])

apds.setProximityIntLowThreshold(50)

print("Proximity Sensor Test")
print("=====================")
apds.enableProximitySensor(False)

oval = -1
while True:
    sleep(0.25)
    val = apds.readProximity()
    if val != oval:
        print("proximity={}".format(val))
