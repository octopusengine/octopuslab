from utils.octopus_lib import w
from esp import espnow

wc = w()

# A WLAN interface must be active to send()/recv()
# w0 = network.WLAN(network.STA_IF)
# w0.active(True)

print("--- espNow init ---")
e = espnow.ESPNow()
e.init()
# peer = b'0\xae\xa4XC\xa0'   # MAC address of peer's wifi interface
mac = ""
e.add_peer(mac)

print(e.irecv())
for msg in e:
    print(msg)
    if (msg[1] == b'end')
        break
