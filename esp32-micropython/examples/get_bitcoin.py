# get bitcoin

from time import sleep
import urequests, json
from util.octopus import w
from shell.terminal import printTitle

w()

def bitcoin_usd():
    res = urequests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
    btcusd = res.json()[0]['price_usd']
    return float(btcusd)

printTitle("get_bitcoin.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()    

while True:
    btc = bitcoin_usd()
    print(btc)
    sleep(10)
