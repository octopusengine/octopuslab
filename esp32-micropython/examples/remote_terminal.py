from time import sleep
from util.octopus import *
from util.shell.terminal import printTitle

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

loop = 0
run = True

while run:
    d7.show("1-{0}.{1}.".format(ip.split('.')[0], ip.split('.')[1]))
    sleep(2)
    d7.show("2-{0}.{1}".format(ip.split('.')[2], ip.split('.')[3]))
    sleep(2)
    loop += 1
    if loop == 3: run = False

