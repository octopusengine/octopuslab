# this module is basic library for OctopusLAB FrameWork
# Pert Kracik, Jan Copak
# -----------------------------------------------------

__version__ = "1.0.9" # format: N.N.N, N<10 ->
libVerDate = "2022-02-18"
libVer100 = __version__[0] + __version__[2] + __version__[4]

TW = 50 # terminal width

def getOctopusLibVer():
    return "octopus lib.ver: " + __version__ + " | " + libVerDate

octopusASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   ) \ `)(' / ( ",
]


def printOctopus():
    print()
    for ol in octopusASCII:
        print(" "*5 + str(ol))
    print()


def printTitle(t,num = TW):
    print()
    print('=' * num)
    print(t.center(num))
    print('=' * num)


def printLog(i = 1,s = ""):
    print()
    print('-' * 35)
    print("[----- " + str(i) + " -----] " + s)


def getFree(echo = False):
    from gc import mem_free
    if echo:
        print("--- RAM free ---> " + str(mem_free()))
    return mem_free()


def printFree():
    getFree(True)


def printInfo(w=TW):
    print('-' * TW)
    print("| ESP UID: " + getUid() + " | RAM free: " + str(getFree()))
    print('-' * TW)


def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


def randint(min, max):
    import urandom
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val


def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)


def add0(sn): # 1 > 01
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str


def getUid(short = False): # full or short (5 chars: first 2 + last 3)
    import machine, ubinascii
    id = ubinascii.hexlify(machine.unique_id()).decode()
    if short:
        return id[:2]+id[-3:]
    else:
        return id


def get_hhmm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm


def get_hh_mm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+"-"+mm


def time_init():
    from ntptime import settime
    from machine import RTC

    rtc = RTC()
    # w()
    settime(zone=0)
    print("--- time: " + get_hhmm(rtc))


def time_init_o(urlApi ="https://www.octopusengine.org/api/hydrop"):
    from urequests import get
    printTitle("time setup from url")
    urltime=urlApi+"/get-datetime.php"
    print("https://urlApi/"+urltime)
    try:
        response = get(urltime)
        dt_str = (response.text+(",0,0")).split(",")
        print(str(dt_str))
        dt_int = [int(numeric_string) for numeric_string in dt_str]
        rtc.init(dt_int)
        #print(str(rtc.datetime()))
        print("time: " + get_hhmm())
    except Exception as e:
        print("Err. Setup time from URL")


def setlocal(h=2):
    import utime
    from machine import RTC
    rtc = RTC()
    localtime = utime.time() + h * 3600
    (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime(localtime)
    rtc.datetime((year, month, mday, 0, hour, minute, second, 0))


def spi_init():
    from machine import Pin, SPI
    from utils.pinout import set_pinout
    pinout = set_pinout()
    spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
    return spi


def i2c_init(HWorSW=0,freq=100000):
    from machine import Pin, I2C
    from utils.pinout import set_pinout
    pinout = set_pinout()
    # i = I2C(scl=Pin(22), sda=Pin(21), freq=f)
    # HW or SW: HW 0 - | SW -1
    i2c = I2C(HWorSW, scl=Pin(pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=freq)
    return i2c


def w_connect():
    from time import sleep_ms
    from utils.wifi_connect import WiFiConnect
    sleep_ms(200)
    w = WiFiConnect()
    if w.connect():
        print("--- WiFi: OK")
    else:
        print("--- WiFi: Connect error, check configuration")

    print('Network config:', w.sta_if.ifconfig())
    return w


def lan_connect():
    from time import sleep_ms
    import network
    if "ETH_CLOCK_GPIO17_OUT" in dir(network):
        lan = network.LAN(mdc = machine.Pin(23), mdio=machine.Pin(18), phy_type=network.PHY_LAN8720, phy_addr=1, clock_mode=network.ETH_CLOCK_GPIO17_OUT)
    else:
        lan = network.LAN(mdc = machine.Pin(23), mdio=machine.Pin(18), phy_type=network.PHY_LAN8720, phy_addr=1)

    lan.active(1)

    retry = 0
    while not lan.isconnected() or lan.ifconfig()[0] is '0.0.0.0':
        retry+=1
        sleep_ms(500)

        if retry > 20:
            break

    if not lan.isconnected():
        print("--- LAN: Connect error, check cable or DHCP server")
        return None

    print("--- LAN: OK")
    print('--- network config:', lan.ifconfig())
    return lan


def logDevice(urlPOST = "https://www.octopusengine.org/iot17/add18.php"):
    from time import sleep_ms
    from urequests import post
    header = {}
    header["Content-Type"] = "application/x-www-form-urlencoded"
    deviceID = getUid()
    place = "octoPy32"
    logVer =  int(libVer100)
    try:
        postdata_v = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, logVer,"log_ver")
        res = post(urlPOST, data=postdata_v, headers=header)
        sleep_ms(200)
        print("--- logDevice.ok")
        res.close()
    except Exception as e:
        print("--- Err.logDevice: {0}".format(e))


def w(logD=True, echo=True):
    MAC = "..."
    if echo:
        printInfo()
        printTitle("--- WiFi connect -> ")
    w = w_connect()
    if logD: logDevice()

    from ubinascii import hexlify
    try:
        MAC = hexlify(w.sta_if.config('mac'),':').decode()
    except:
        MAC = "Err: w.sta_if"
    if echo:
        print("--- MAC: ", MAC)
        getFree(True)
    return w


def ap_init(): # default IP 192.168.4.1
    printTitle("--- AP init > ")
    from utils.wifi_connect import WiFiConnect
    import ubinascii
    w = WiFiConnect()
    w.ap_if.active(True)
    mac = ubinascii.hexlify(w.ap_if.config('mac'),':').decode()
    w.ap_if.config(essid="octopus_ESP32_" + mac)
    print(w.ap_if.ifconfig())
    print("AP Running: " + w.ap_if.config("essid"))
    return w
