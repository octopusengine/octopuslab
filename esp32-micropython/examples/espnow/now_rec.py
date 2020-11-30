from utils.octopus_lib import w
from esp import espnow

wc = w()


print("--- espNow init ---")
en = espnow.ESPNow()
en.init()

remotemac = ""

en.add_peer(remotemac)
en.send("octopus Test")
