# get bitcoin

from time import sleep
import urequests, json
from util.octopus import w, disp7_init
from util.shell.terminal import printTitle

keep_alive = 0
w()
d7 = disp7_init()

def d7pause(ch = "-", sl = 0.5):
    for i in range(8):
        d7.show(" "*i + ch)
        sleep(sl)

def bitcoin_usd():
    btcusd=888

    try:
        res = urequests.get("https://api.coinpaprika.com/v1/tickers/btc-bitcoin"                                                                                                             )
        btcusd = res.json()['quotes']["USD"]["price"]

    except:
        x=0
    return int(btcusd)

printTitle("get_bitcoin.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
    btc = bitcoin_usd()
    print(btc)
    d7.show(btc)
    sleep(10)
    d7pause(sl = 0.6)
    d7pause(sl = 0.3)
    d7.show(keep_alive)
    sleep(1)
    d7pause(sl = 0.3)
    d7.show("btc-usd")
    keep_alive += 1
