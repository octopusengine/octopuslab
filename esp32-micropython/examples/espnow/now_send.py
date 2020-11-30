from utils.octopus_lib import w
from esp import espnow

wc = w()


print("--- espNow init ---")
e = espnow.ESPNow()
e.init()

remotemac = ""

e.add_peer(remotemac)
e.send("octopus Test")
