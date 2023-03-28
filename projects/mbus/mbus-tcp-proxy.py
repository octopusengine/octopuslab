#import time

# TODO: use network manager?
WIFI_SSID="..."
WIFI_PASS="..."

from machine import UART, Pin
from network import WLAN
import usocket
from time import sleep

ser = UART(1, 2400, bits=8, parity=0, stop=1, tx=4, rx=36)

w = WLAN()
w.active(True)
w.connect(WIFI_SSID, WIFI_PASS)

print("Connecting wifi...")

while not w.isconnected():
    print(".")
    sleep(1)

print("Connected")

print("Creating socket on {}:1234".format(w.ifconfig()[0]))
s = usocket.socket()
s.setblocking(False)
s.bind(("0.0.0.0", 1234))
s.listen()

clients = list()
removal = list()

def read_socket():
    while True:
        try:
            c = s.accept()
            c[0].settimeout(0.1)
            clients.append(c[0])
            print("New client {}:{}".format(c[1][0],c[1][1]))
        except OSError:
            pass
        
        serdata = ser.read(256)

        for c in clients:
            try:
                if serdata:
                    print("Got serial data: {}".format(serdata))
                    c.send(serdata)

                data, host = c.recvfrom(256)
                if not data:
                    c.close()
                    removal.append(c)
                    continue

                print("{}:{}: {}".format(host[0], host[1], data))
                ser.write(data)
            except OSError:
                pass
        
        for r in removal:
            print("Removing client")
            clients.remove(r)
        
        removal.clear()


print("Running socket")
read_socket()
