from time import sleep
from util.octopus import *

d7 = disp7_init()

d7.show("Connect")
iface = w_connect()
#iface = lan_connect()

printTitle("remote terminal")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()    

import webrepl
webrepl.start()

print("IP Address: ")
ip = iface.ifconfig()[0]
print(ip)

while True:
    d7.show("1-{0}.{1}.".format(ip.split('.')[0], ip.split('.')[1]))
    sleep(2)
    d7.show("2-{0}.{1}".format(ip.split('.')[2], ip.split('.')[3]))
    sleep(2)

