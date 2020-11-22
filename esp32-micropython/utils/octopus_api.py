# this module is API library for Octopus FrameWork
# (aplication programming interface / web api or rest api)
# example - https://www.octopuslab.cz/api-esp/
# -----------------------------------------------------

__version__ = "1.0.2"


# getApiJson
def get_json(urlApi ="https://www.octopuslab.cz/data/", urlFile = "led2.json", debug = "True"):
    # "http://www.octopusengine.org/api/"
    from urequests import get
    from json import loads
    urljson=urlApi + urlFile
    aj = ""
    try:
        response = get(urljson)
        dt_str = (response.text)
        if debug: print(str(dt_str))
        j = loads(dt_str)
        #print(str(j))
        aj = j['light']
    except Exception as e:
        print("Err. read json from URL")
    return aj


def getApiTest():
    print("data from url ->")
    #print("https://urlApi/"+urljson)
    print("htts://public_unsecure_web/data.json")
    print(get_json())


# getApiText
def get_text(urlApi ="https://www.octopusengine.org/api"):
    from urequests import get
    urltxt=urlApi+"/text123.txt"
    try:
        response = get(urltxt)
        dt_str = response.text
    except Exception as e:
        print("Err. read txt from URL")
    return dt_str


# third party api example
def twitter_rgb():
    import urequests

    url = 'http://api.thingspeak.com/channels/1417/field/2/last.txt'
    response = urequests.get(url)
    text = response.text

    if text and text[0] == '#':
        color = text[1:7]

        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)

        return red, green, blue
    return 0, 0, 0


# note: 10-20 sec. pause is required
def bitcoin_usd():
    from time import sleep
    import urequests, json

    res = urequests.get("https://api.coinpaprika.com/v1/tickers/btc-bitcoin")
    btcusd = res.json()['quotes']["USD"]["price"]
    return float(btcusd)
