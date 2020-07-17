import time
import network
import urequests
from machine import SPI, I2C, Pin
from epaper1in54 import EPD
import framebuf
from uQR import QRCode
from Keypad_I2C import keypad
from lib.esp8266_i2c_lcd import I2cLcd
from util.wifi_connect import WiFiConnect

# Defaults
# Delay for another key
keyDelay = 250

# Delay for rate update, in sec
rateUpdate = 60

# Delay how offten will check blockchain for payment
processPaymentCheckRate = 10

# Crypto
#crypto = ['BTC', 'LTC']
crypto = ['BTC', 'LTC', 'TEST']
cryptoIndex = 0

fiatCurrency = 'CZK'
cryptoCurrency = crypto[cryptoIndex]

# Coins
addresses = dict()
addresses['BTC']  = { 'protocol': 'bitcoin',  'address': '3CCHj2et6TFDB3k9MnqWQeM7nM3HLwnhnq' }
addresses['LTC']  = { 'protocol': 'litecoin', 'address': 'MMtoZZY92Ze7EuBbu5KfVjEwUAeuvdcrLW' }
addresses['VTC']  = { 'protocol': 'vertcoin', 'address': '3FqN2Qpvhq4uZ7o94qq7K859HBhdqBhsjY' }
addresses['TEST'] = { 'protocol': 'bitcoin',  'address': '2N143V8ZuwU7E1XH3TaExDHs1MiyWF3aSMh'}

# Block explorer
explorers = dict()
explorers['BTC']  = { 'domain': 'btc4.trezor.io'  }
explorers['LTC']  = { 'domain': 'ltc4.trezor.io'  }
explorers['VTC']  = { 'domain': 'vtc4.trezor.io'  }
explorers['TEST'] = { 'domain': 'tbtc1.trezor.io' }

# Periferie
spi = SPI(1, sck=Pin(18), mosi=Pin(23))

i2c_sda = Pin(21, Pin.IN,  Pin.PULL_UP)
i2c_scl = Pin(22, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(

LCD_ADDRESS=63
LCD_ROWS=4
LCD_COLS=16

lcd = I2cLcd(i2c, LCD_ADDRESS, LCD_ROWS, LCD_COLS)

# Display
eink = EPD(spi, Pin(5), Pin(2), None, Pin(34))
eink.init()
eink.clear_frame_memory(255)

# Keypad
kp = keypad(i2c, 0x23)

# Frame buffers
ebuf = bytearray(200 * 200 // 8)
efb  = framebuf.FrameBuffer(ebuf, 200, 200, framebuf.MONO_HLSB)

def profile(func, *args, **kargs):
    start = time.ticks_ms()
    res = func(*args, **kargs)
    print("{0} took: {1}ms".format(func.__name__, time.ticks_ms() - start))
    return res

def efb_show():
    profile(eink.set_frame_memory, ebuf, 0, 0, 200, 200)
    profile(eink.display_frame)

def display_qr(matrix, offset_x=0, offset_y=0, scale=3):
    efb_pixel = efb.pixel
    for y in range(len(matrix)*scale):
        for x in range(len(matrix[0])*scale):
            value = not matrix[y//scale][x//scale]
            efb_pixel(x+offset_x, y+offset_y, value)

    profile(efb_show)

def display_text_lcd(text, x, y):
    if lcd is None:
        return

    lcd.move_to(x, y)

    if x - len(text) < LCD_COLS:
        text+=" " * (LCD_COLS - x - len(text))

    lcd.putstr(text)

def display_amount_lcd(text, amount, x, y):
    if lcd is None:
        return

    lcd.move_to(x, y)
    if len(text) < LCD_COLS:
        text+=" " * (LCD_COLS-len(text))

    lcd.putstr(text)
    lcd.move_to(x, y+1)

    if len(amount) < LCD_COLS:
        amount+=" " * (LCD_COLS-len(amount))

    lcd.putstr(amount)

def display_rate_lcd(rate):
    if lcd is None:
        return

    lcd.move_to(0, 0)
    text = "{0} {1}/{2}".format(rate, fiatCurrency, cryptoCurrency)
    if len(text) < LCD_COLS:
        text+=" " * (LCD_COLS-len(text))
    lcd.putstr(text)

efb.fill(1)
efb.text("Bitcoin Machine", 0, 0, 0)
efb.text("Booting...", 0, 10, 0)

efb_show()

# QR
qr = QRCode(border = 2)

display_text_lcd("Connect wifi", 0, 0)

efb.text("Connecting...", 0, 20, 0)
efb_show()

wlan = WiFiConnect()
#wlan.connect()
#wlan.connect("PCC WiFi", "")
#wlan.connect("www.petrkr.net 2G", "heslokleslo")
#wlan.connect("satoshilabs-guest", "satoshiho navstevnici")
wlan.connect("IoT", "octopus19")
#wlan.connect("ParalelniPolis", "vejdiven")
#wlan.connect("MS-KONFERENCE", "wifiMFFUKakce")
#wlan.connect("makersMFP2019", "makersgonnamake")

print("OK")

def getPaymentURI():
    if cryptoCurrency not in addresses:
        return "unknown"

    proto = addresses[cryptoCurrency]['protocol']
    addr  = addresses[cryptoCurrency]['address']
    return "{0}:{1}".format(proto, addr)


basePaymentURI = getPaymentURI()
baseRateURI= "https://coinmate.io/api/ticker?currencyPair="

def getPrice(pair):
    if cryptoCurrency in ['BTC','LTC']:
        uri = "{0}{1}".format(baseRateURI, pair)
        rate = urequests.get(uri)
        if rate:
            return rate.json()['data']['ask']

    if cryptoCurrency is 'TEST':
        return 1000 # Fixed rat 1000 for testnet

    uri = "https://api.coinmarketcap.com/v1/ticker/{0}/?convert=CZK".format(addresses[cryptoCurrency]['protocol'])
    try:
        rate = urequests.get(uri)
    except Exception as e:
        print("Error getting rate")
        print(e)
        return None
    if rate:
        return round(float(rate.json()[0]['price_czk']), 4)

    return None


def renderDonation():
    qr.clear()
    qr.add_data("{0}?label='Donation'".format(basePaymentURI))
    display_text_lcd("Rendering QR..", 0, 1)
    matrix = qr.get_matrix()

    # Clear eInk
    efb.fill(1)
    efb.text("Bitcoin Machine", 35, 5, 0)
    efb.text("Donation", 70, 180, 0)
    profile(display_qr, matrix, 25, 20, 4)
    display_text_lcd("", 0, 1)

display_text_lcd("Bitcoin machine", 0, 0)
renderDonation()

value = '0'

lastKeyPress = 0

# To get update after power-up, we need set this to minus
lastRateUpdate = -(rateUpdate*1000)
currentRate = 0

def updateRate(force=False):
    if processingPayment:
        return

    global lastRateUpdate
    if (time.ticks_ms() < lastRateUpdate + (rateUpdate*1000) and not force):
        return

    global currentRate

    display_text_lcd("Updating rate", 0, 1)

    lastRateUpdate = time.ticks_ms()
    rate = getPrice("{0}_{1}".format(cryptoCurrency, fiatCurrency))
    if rate:
        print("Setting new exchange rate {0}".format(rate))
        currentRate = rate
    else:
        print("Error get exchange rate, using old one")

    display_rate_lcd(rate)
    display_text_lcd("", 0, 1)

def getTransactions(address):
    url = "https://{0}/api/address/{1}".format(explorers[cryptoCurrency]['domain'], address)
    addr = urequests.get(url)
    if addr:
        if 'transactions' not in addr.json():
            return []
        else:
            return addr.json()['transactions']

acceptPayment = True
processingPayment = False
addressTxCount = 0

lastProcessPaymentCheck = 0
def processPayment():
    global lastProcessPaymentCheck

    if time.ticks_ms() < lastProcessPaymentCheck + (processPaymentCheckRate*1000):
        return

    lastProcessPaymentCheck = time.ticks_ms()

    global processingPayment
    global acceptPayment

    if not processingPayment:
        return

    if acceptPayment:
        return

    txs = getTransactions(addresses[cryptoCurrency]['address'])
    txcount = len(txs)
    print("Actual transaction count: {0}".format(txcount))

    if txcount > addressTxCount:
        txid = txs[0]
        display_text_lcd("PAID", 0, 0)
        efb.fill_rect(15, 70, 160, 30, 0)
        efb.fill_rect(18, 73, 154, 24, 1)
        efb.text("PAID", 80, 82, 0)

        efb.fill_rect(10, 100, 170, 25, 0)
        efb.fill_rect(13, 103, 164, 19, 1)
        efb.text("{0}...{1}".format(txid[:8], txid[-8:]), 18, 109, 0)

        efb_show()

        processingPayment = False
        acceptPayment = True

abortPayment = 0

while True:
    updateRate()

    processPayment()
    try:
        key = kp.getKey()
    except OSError as e:
        print("Error while get key")
        print(e)
        key = None

    if key and time.ticks_ms() > lastKeyPress+keyDelay:
        lastKeyPress = time.ticks_ms()
        print(key)

        if key == 'A':
            if not acceptPayment:
                abortPayment+=1
                if abortPayment > 10:
                    acceptPayment = True
                    processingPayment = False
                    abortPayment = 0
                    display_text_lcd("Aborted", 0, 0)
                    time.sleep(2)
                    updateRate(True)
                    renderDonation()

                continue

            if len(value) == 0:
                continue

            value = value[:-1]
            if value:
                display_amount_lcd("Amount ({0})".format(fiatCurrency), str(int(value) / 100), 0, 30)
            else:
                value = '0'
                display_amount_lcd("Amount ({0})".format(fiatCurrency), '0.00', 0, 30)

        if not acceptPayment:
            continue

        if key == 'B':
            value = '0'
            display_amount_lcd("Amount ({0})".format(fiatCurrency), '0.00', 0, 30)

        if key == 'C':
            cryptoIndex += 1
            if cryptoIndex == len(crypto):
                cryptoIndex = 0

            cryptoCurrency = crypto[cryptoIndex]
            print("Change crypto to {0}".format(cryptoCurrency))

            display_text_lcd("Crypto {0}".format(cryptoCurrency),0 ,0)

            basePaymentURI = getPaymentURI()
            updateRate(True)
            renderDonation()

            value = '0'


        if key == 'D':
            print("Amount: {0}".format(int(value) / 100))
            cryptoValue = round((int(value)/100) / currentRate, 8)
            if lcd:
                display_text_lcd("Rendering QR..", 0, 0)

            efb.fill(1)
            efb.text("Amount: {0} {1}".format(int(value) / 100, fiatCurrency), 0, 170, 0)
            efb.text("Amount: {0} {1}".format(cryptoValue, cryptoCurrency), 0, 185, 0)
            profile(qr.clear)
            qr.add_data("{0}?label='payment'&amount={1}".format(basePaymentURI, cryptoValue))
            matrix = profile(qr.get_matrix)
            profile(display_qr, matrix, 15, 0, 4)

            #display_rate_lcd(currentRate)
            #display_amount_lcd("Amount ({0})".format(fiatCurrency), '0.00', 0, 30)
            lcd.clear()

            display_text_lcd("Waiting payment", 0, 0)
            value = '0'

            try:
                addressTxCount = len(getTransactions(addresses[cryptoCurrency]['address']))
                processingPayment = True
                acceptPayment = False
            except Exception as e:
                print("Error when getting transaction count")
                print(e)

        if key >= '0' and key <= '9':
            value+=key
            display_amount_lcd("Amount ({0})".format(fiatCurrency), str(int(value) / 100), 0, 30)