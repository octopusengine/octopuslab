# get bitcoin

from time import sleep
import urequests, json
from utils.octopus import w
from shell.terminal import printTitle

w()

def bitcoin_usd():

    res = urequests.get("https://api.coinpaprika.com/v1/tickers/btc-bitcoin")
    btcusd = res.json()['quotes']["USD"]["price"]
    return float(btcusd)

printTitle("get_bitcoin.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()    

while True:
    btc = bitcoin_usd()
    print(btc)
    sleep(10)
