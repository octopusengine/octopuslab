# This file is part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2020 Jan Copak, Petr Kracik, Vasek Chalupnicek

__version__ = "1.0.5"

# from sys import modules
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from machine import Pin, Timer, RTC
#from os import urandom
from utils.pinout import set_pinout
from utils.io_config import get_from_file
from shell.terminal import printTitle, printLog, printHead


# olab = Env()  # for initialized equipment
pinout = set_pinout()     # set board pinout
io_conf = get_from_file() # read configuration for peripherals
rtc = RTC()  # real time


class Env:  # for temporary global variables and config setup
    from ubinascii import hexlify
    from machine import unique_id, freq
    ver = "1.04"  # version - log: num = ver*100
    verDat = "10.09.2020 #998"
    debug = True
    logDev = True
    autoInit = True
    autoTest = False
    uID = hexlify(unique_id()).decode()
    MAC = "..."
    freq = freq()
    TW = 50  # terminal width
    isTimer = True
    timerFlag = 0
    timerCounter = 0
    timerLed = True
    timerBeep = False

    # wsc = web_server control
    wscWS = True  # WS RGB LED
    wscPWM = False # PWM LED - IoT board / hydroponics
    wscRelay = False
    wscLed = True  # only this simple test is defa 1
    wscExp8 = False

if Env.isTimer:
    tim1 = Timer(0)

# ------------- common terminal function ------------
def getVer():
    return "octopusLAB - lib.version: " + Env.ver + " > " + Env.verDat


def printInfo(w=Env.TW):
    print('-' * w)
    print("| ESP UID: " + Env.uID + " | RAM free: " + str(getFree()))
    print('-' * w)


def o_help():
    from shell import cat
    printOctopus()
    print("Welcome to MicroPython on the ESP32 octopusLAB board")
    print("("+getVer()+")")
    printTitle("basic commands - list, examples", 53)
    cat("util/octopus_help.txt", False)
    printInfo()


def o_info():
    from os import statvfs
    from gc import mem_free
    printTitle("basic info > ")
    print("This is basic info about system and setup")

    print("> machine.freq: "+str(Env.freq) + " [Hz]")
    printLog("memory")
    print("> ram free: "+str(mem_free()) + " [B]")
    #print("> flash: "+str(os.statvfs("/")))
    ff =int(statvfs("/")[0])*int(statvfs("/")[3])
    print("> flash free: "+str(int(ff/1000)) + " [kB]")
    printLog("device")
    try:
        with open('config/device.json', 'r') as f:
            d = f.read()
            f.close()
            print(" > config/device: " + d)
            # device_config = json.loads(d)
    except Exception as e:
        print("Device config 'config/device.json' does not exist, please run setup()")

    printLog("pinout")
    print(pinout)
    printLog("io_conf")
    print(io_conf)
    printInfo()


def led_init(pin = pinout.BUILT_IN_LED):
    from components.led import Led
    if pin is not None and pinout is not None and (pin == pinout.RXD0 or pin == pinout.TXD0):
        print("WARNING: PIN {0} is used for UART0. REPL Over serial will be unusable")

    led = Led(pin if pin is not None and pin > 0 else None)
    return led


def i2c_init(scan = False, freq=100000, HWorSW = 0, printInfo = True):
    from machine import I2C
    # HW or SW: HW 0 - | SW -1
    i2c = I2C(HWorSW, scl=Pin(pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=freq)
    if scan:
        if printInfo: print("i2c.scan() > devices:")
        # I2C address:
        OLED_ADDR = 0x3c
        LCD_ADDR = 0x27
        try:
            i2cdevs = i2c.scan()
            if printInfo: print(i2cdevs)
            if (OLED_ADDR in i2cdevs):
                if printInfo: print("ok > OLED: "+str(OLED_ADDR))
            if (LCD_ADDR in i2cdevs):
                if printInfo: print("ok > LCD: "+str(LCD_ADDR))
            bhLight = 0x23 in i2cdevs
            bh2Light = 0x5c in i2cdevs
            tslLight = 0x39 in i2cdevs
        except Exception as e:
            print("Exception: {0}".format(e))
    return i2c


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


def getFree(echo = False):
    from gc import mem_free
    if echo:
        print("--- RAM free ---> " + str(mem_free()))
    return mem_free()


def ap_init(): #192.168.4.1
    printTitle("AP init > ")
    from utils.wifi_connect import WiFiConnect
    import ubinascii
    w = WiFiConnect()
    w.ap_if.active(True)
    mac = ubinascii.hexlify(w.ap_if.config('mac'),':').decode()
    w.ap_if.config(essid="octopus_ESP32_" + mac)
    print(w.ap_if.ifconfig())
    print("AP Running: " + w.ap_if.config("essid"))
    return w


def w_connect():
    led.value(1)

    from utils.wifi_connect import WiFiConnect
    sleep(1)
    w = WiFiConnect()
    if w.connect():
        print("WiFi: OK")
    else:
        print("WiFi: Connect error, check configuration")

    led.value(0)
    print('Network config:', w.sta_if.ifconfig())
    return w


def lan_connect():
    from network import LAN, ETH_CLOCK_GPIO17_OUT, PHY_LAN8720
    led.value(1)
    lan = LAN(mdc=Pin(23), mdio=Pin(18), phy_type=PHY_LAN8720, phy_addr=1, clock_mode=ETH_CLOCK_GPIO17_OUT)
    lan.active(1)

    retry = 0
    while not lan.isconnected() or lan.ifconfig()[0] is '0.0.0.0':
        retry+=1
        sleep_ms(500)

        if retry > 20:
            break

    if not lan.isconnected():
        print("LAN: Connect error, check cable or DHCP server")
        return None

    print("LAN: OK")
    led.value(0)
    print('network config:', lan.ifconfig())
    return lan


def logDevice(urlPOST = "https://www.octopusengine.org/iot17/add18.php"):
    from urequests import post
    header = {}
    header["Content-Type"] = "application/x-www-form-urlencoded"
    deviceID = Env.uID
    place = "octoPy32"
    logVer =  int(float(Env.ver)*100)
    try:
        postdata_v = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, logVer,"log_ver")
        res = post(urlPOST, data=postdata_v, headers=header)
        sleep_ms(100)
        print("logDevice.ok")
        res.close()
    except Exception as e:
        print("Err.logDevice: {0}".format(e))


def w(logD=True, echo=True):
    if echo:
        printInfo()
        printTitle("WiFi connect > ")
    w = w_connect()
    if logD and Env.logDev: logDevice()

    from ubinascii import hexlify
    try:
        Env.MAC = hexlify(w.sta_if.config('mac'),':').decode()
    except:
        Env.MAC = "Err: w.sta_if"
    if echo:
        getFree(True)
    return w


def bme280_init():
    from bme280 import BME280
    try:
        i2c = i2c_init(1)
        bme = BME280(i2c=i2c)
        print(bme.values)
        return bme
    except Exception as e:
        print("bme280_init() Exception: {0}".format(e))



def getApiJson(urlApi ="https://www.octopuslab.cz/data/", urlFile = "led2.json", debug = "True"):
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
    printTitle("data from url")
    #print("https://urlApi/"+urljson)
    print("htts://public_unsecure_web/data.json")
    print(getApiJson())


def getApiText(urlApi ="https://www.octopusengine.org/api"):
    from urequests import get
    urltxt=urlApi+"/text123.txt"
    try:
        response = get(urltxt)
        dt_str = response.text
    except Exception as e:
        print("Err. read txt from URL")
    return dt_str


def octopus(auto = True):
    if auto:
        # print("auto")
        auto_init = True # todo

    from gc import collect
    printOctopus()
    print("("+getVer()+")")
    collect()
    printInfo()
    print("This is basic library, type h() for help")


def octopus_init():
    Env.start = ticks_ms()
    print("auto Init: " + str(Env.autoInit))
    #if Env.autoInit:
    printTitle("> auto Init ")
    if io_conf.get('led'):
        printLog("led.blink()")
        print("testing led")
        led.blink()

    if io_conf.get('ws'):
        printLog("ws.test()")
        print("testing ws - RGB led")
        ws.test()

    if io_conf.get('led7'):
        Env.d7 = disp7_init()

    if io_conf.get('oled'):
        Env.o = oled_init()

    if io_conf.get('temp'):
        Env.t = temp_init()

    printLog("ticks_diff(ticks_ms(), Env.start)")
    delta = ticks_diff(ticks_ms(), Env.start)
    print("delta_time: " + str(delta))


# ---------- init env. def(): --------------
if io_conf.get('fet'): # 1 defaul for IoT, >1 user pin
    if int(io_conf.get('fet')) > 1:
        if "PWM" not in modules:
            from machine import PWM
        mfet_pin = int(io_conf.get('fet')) # pinout.MFET_PIN
        FET = PWM(Pin(mfet_pin), freq=500)
        FET.duty(500) # pin(14) Robot(MOTO_3A), ESP(JTAG-MTMS)
        sleep(0.5)
        FET.duty(0)


if Env.autoInit:  # test
    print("octopus() --> autoInit: ",end="")
    if io_conf.get('led') is None:
        led = led_init(None)
    elif io_conf.get('led') == 1:
        print("Led | ",end="")
        led = led_init()
    else:
        print("Led | ",end="")
        led = led_init(io_conf.get('led'))

    piezzo = None
    if io_conf.get('piezzo'):
        print("piezzo | ",end="")
        from components.buzzer import Buzzer
        piezzo = Buzzer(pinout.PIEZZO_PIN)
        piezzo.beep(1000,50)
        from components.buzzer import Notes
        def beep(f=1000, l=50):  # noqa: E741
            piezzo.beep(f, l)

        def tone(f, l=300):  # noqa: E741
            piezzo.play_tone(f, l)
    # else:   #    piezzo =Buzzer(None)

    if io_conf.get('ws'):
        print("ws | ",end="")
        from components.rgb import Rgb
        from colors_rgb import *
        if pinout.WS_LED_PIN is None:
            print("Warning: WS LED not supported on this board")
        else:
            ws = Rgb(pinout.WS_LED_PIN,io_conf.get('ws')) # default rgb init

        def rgb_init(num_led=io_conf.get('ws'), pin=None):  # default autoinit ws
            if pinout.WS_LED_PIN is None:
                print("Warning: WS LED not supported on this board")
                return
            if num_led is None or num_led == 0:
                print("Warning: Number of WS LED is 0")
                return
            from components.rgb import Rgb  # setupNeopixel
            ws = Rgb(pin, num_led)
            return ws


    if io_conf.get('led7') or io_conf.get('led8'):
        from machine import SPI
        print("SPI | ",end="")
        spi = None
        ss  = None
        try:
            #spi.deinit() #print("spi > close")
            spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
            ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
        except Exception as e:
            print("Err.spi")

    if io_conf.get('led7'):
        print("disp7 | ",end="")
        def disp7_init():
            printTitle("disp7init()")
            from components.display7 import Display7
            print("display test: octopus")
            d7 = Display7(spi, ss)
            d7.write_to_buffer('octopus')
            d7.display()
            return d7

    if io_conf.get('led8'):
        print("disp8 | ",end="")
        def disp8_init():
            printTitle("disp8init()")
            from lib.max7219 import Matrix8x8
            d8 = Matrix8x8(spi, ss, 1)  # 1/4

            count = 6
            for i in range(count):
                d8.fill(0)
                d8.text(str(i), 0, 0, 1)
                d8.show()
                print(i)
                sleep_ms(500)
            d8.fill(0)
            d8.show()
            return d8

        def scroll(d8, text, num):  # TODO speed, timer? / NO "sleep"
            WIDTH = 8*4
            x = WIDTH + 2
            for _ in range(8*len(text)*num):
                sleep(0.03)
                d8.fill(0)
                x -= 1
                if x < - (8*len(text)):
                    x = WIDTH + 2
                d8.text(text, x, 0, 1)
                d8.show()
            d8.fill(0)
            d8.show()

    if io_conf.get('oled') or io_conf.get('lcd'):
        print("I2C | ",end="")
        try:
            i2c = i2c_init(False)
        except Exception as e:
            print("Err.i2c_init")

    if io_conf.get('oled'):
        print("OLED | ",end="")
        from assets.icons9x9 import ICON_clr, ICON_wifi
        from components.display_segment import oneDigit, threeDigits
        from components.oled import Oled

        def oled_init(ox=128, oy=64, runTest = True):
            printTitle("oled_init()")

            from components.oled import Oled
            from components.display_segment import threeDigits
            sleep_ms(1000)

            oled = Oled(i2c, 0x3c, ox, oy)
            print("test oled display: OK")
            if runTest:
                oled.test()
                threeDigits(oled,123)

            return oled

    if io_conf.get('lcd'):
        print("lcd | ",end="")
        LCD_ADDR = 0x3F # 0x27
        def lcd2_init(addr = LCD_ADDR):

            printTitle("lcd2init()")
            LCD_ROWS=2
            LCD_COLS=16
            from lib.esp8266_i2c_lcd import I2cLcd
            lcd = I2cLcd(i2c, addr, LCD_ROWS, LCD_COLS)
            print("display test: octopusLAB")
            happy_face = bytearray([0x00,0x0A,0x00,0x04,0x00,0x11,0x0E,0x00])
            lcd.custom_char(0, happy_face)
            # lcd.move_to(0,1) # col 1 (0) / row 2 (012)
            lcd.clear()
            lcd.putstr("octopusLAB")
            return lcd


    if io_conf.get('temp'):
        print("temp | ",end="")
        try: PIN_TEMP = pinout.ONE_WIRE_PIN
        except: PIN_TEMP = 17 # ROBOT
        def temp_init(pin = PIN_TEMP):
            from components.iot import Thermometer
            ts = Thermometer(pin)
            # tx = tt.ds.scan()
            # ts.read_temp(tx[0])
            return ts


    if io_conf.get('exp8'):
        print("exp8 | ",end="")
        from components.i2c_expander import Expander8
        def i2c_expander_init(addr = 0):
            printTitle("i2c_expander_init()")
            from components.i2c_expander import Expander8 # from components.i2c_expander import neg, int2bin
            if addr == 0:
                e8 = Expander8()
            else:
                e8 = Expander8(addr)
            return e8


        def wait_pin_change(pin):
            # wait for pin to change value, it needs to be stable for a continuous 20ms
            cur_value = pin.value()
            active = 0
            while active < 20:
                if pin.value() != cur_value:
                    active += 1
                else:
                    active = 0
                sleep_ms(1)

    print()


def small_web_server(wPath='www/'):
    from lib.microWebSrv import MicroWebSrv
    # ? webPath as parameter
    mws = MicroWebSrv(webPath=wPath)      # TCP port 80 and files in /flash/www
    mws.Start(threaded=True) # Starts server in a new thread
    print("Web server started > " + wPath)
    getFree(True)


def web_server():
    printTitle("web_server start > ")
    from lib.microWebSrv import MicroWebSrv
    import os, webrepl
    from ubinascii import hexlify
    from utils.wifi_connect import WiFiConnect
    if Env.wscExp8:
        from components.i2c_expander import Expander8
        expander = Expander8()

    wc = WiFiConnect()

    led = None

    if io_conf.get('led') is None:
        led = led_init(None)
    elif io_conf.get('led') == 1:
        print("Led | ",end="")
        led = led_init()
    else:
        print("Led | ",end="")
        led = led_init(io_conf.get('led'))

    led.blink()


    @MicroWebSrv.route('/setup/wifi/networks.json') # GET
    def _httpHandlerWiFiNetworks(httpClient, httpResponse):
        nets = [[item[0], hexlify(item[1], ":"), item[2], item[3], item[4]] for item in wc.sta_if.scan()]
        httpResponse.WriteResponseJSONOk(nets)


    @MicroWebSrv.route('/setup/wifi/savednetworks.json') # GET
    def _httpHandlerWiFiNetworks(httpClient, httpResponse):
        wc.load_config()
        nets = [k for k,v in wc.config['networks'].items()]
        httpResponse.WriteResponseJSONOk(nets)


    @MicroWebSrv.route('/setup/wifi/network')   # Get acutal network
    def _httpHandlerWiFiCreateNetwork(httpClient, httpResponse):
        content = None
        data = dict()
        sta_ssid = wc.sta_if.config("essid")
        sta_rssi = wc.sta_if.status("rssi") if wc.sta_if.isconnected() else 0
        sta_connected = wc.sta_if.isconnected()
        sta_active = wc.sta_if.active()

        ap_ssid = wc.ap_if.config("essid")
        ap_connected = wc.ap_if.isconnected()
        ap_active = wc.ap_if.active()
        ap_stations = [ hexlify(sta[0], ":") for sta in wc.ap_if.status("stations") ] if wc.ap_if.active() else []

        data["sta_if"] = { "active": sta_active, "connected": sta_connected, "ssid": sta_ssid, "rssi": sta_rssi}
        data["ap_if"] = { "active": ap_active, "connected": ap_connected, "ssid": ap_ssid, "stations": ap_stations }

        httpResponse.WriteResponseJSONOk(data)


    @MicroWebSrv.route('/setup/wifi/network', "POST")   # Create new network
    def _httpHandlerWiFiCreateNetwork(httpClient, httpResponse):
        data  = httpClient.ReadRequestContentAsJSON()
        responseCode = 500
        content = None

        if len(data) < 1:
            responseCode = 400
            content = "Missing ssid in request"
            httpResponse.WriteResponse( code=400, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)
            return

        ssid = data[0]
        psk = data[1] if len(data) > 1 else ""
        wc.add_network(ssid, psk)
        responseCode = 201

        httpResponse.WriteResponse( code=responseCode, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)


    @MicroWebSrv.route('/setup/wifi/network', "PUT")    # Update existing network
    def _httpHandlerWiFiUpdateNetwork(httpClient, httpResponse):
        data  = httpClient.ReadRequestContentAsJSON()
        responseCode = 500
        content = None

        print(data)

        if len(data) < 1:
            responseCode = 400
            content = "Missing ssid in request"
            httpResponse.WriteResponse( code=400, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)
            return

        ssid = data[0]
        psk = data[1] if len(data) > 1 else ""

        print("Updating network {0}".format(data[0]))
        wc.add_network(ssid, psk)
        responseCode = 201

        httpResponse.WriteResponse( code=responseCode, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)


    @MicroWebSrv.route('/setup/wifi/network', "DELETE") # Delete existing network
    def _httpHandlerWiFiDeleteNetwork(httpClient, httpResponse):
        data = httpClient.ReadRequestContentAsJSON()
        responseCode = 500
        content = None

        if len(data) < 1:
            responseCode = 400
            content = "Missing ssid in request"
            httpResponse.WriteResponse( code=400, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)
            return

        ssid = data[0]
        wc.remove_network(ssid)
        responseCode = 201

        httpResponse.WriteResponse( code=responseCode, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)


    @MicroWebSrv.route('/setup/devices.json') # GET boards
    def _httpHandlerDevices(httpClient, httpResponse):
        from utils.setup import devices

        httpResponse.WriteResponseJSONOk(devices)


    @MicroWebSrv.route('/esp/control_info.json') # GET info
    def _httpHandlerInfo(httpClient, httpResponse):

        infoDict = {}
        infoDict["deviceUID"] = Env.uID
        infoDict["deviceMAC"] = Env.MAC
        infoDict["freq"] = Env.freq
        infoDict["freeRAM"] = getFree()
        infoDict["freeFLASH"] = str(int(os.statvfs("/")[0])*int(os.statvfs("/")[3]))
        ## infoJ = ujson.dumps(infoDict)

        httpResponse.WriteResponseJSONOk(infoDict)


    @MicroWebSrv.route('/esp/control/led', "POST") # Set LED
    def _httpHandlerSetDevice(httpClient, httpResponse):
        data = httpClient.ReadRequestContent()
        val = int(data)
        print("control/led call: " + str(val))
        led.value(val)
        if Env.wscWS:
            if val == 2: ws.color(RED)
            if val == 3: ws.color(GREEN)
            if val == 4: ws.color(BLUE)
            if val == 5: ws.color(ORANGE)
            if val == 6: ws.color((128,0,128))
            if val == 0: ws.color(BLACK)

        httpResponse.WriteResponseOk(None)


    @MicroWebSrv.route('/esp/control/pwm', "POST") # PWM - IOT/ Hydroponics LED
    def _httpLedPwmSet(httpClient, httpResponse):
        data = httpClient.ReadRequestContent()
        print("LED PWM Call: " + str(int(data)))

        if FET is None:
            httpResponse.WriteResponse(code=500, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "MFET is not defined, check setup()")
            return
        try:
            value = int(data)
            if value > 390: FET.freq(2000)
            else: FET.freq(300)
            FET.duty(value)
        except Exception as e:
            print("Exception: {0}".format(e))
            raise
        finally:
            httpResponse.WriteResponseOk(None)

        httpResponse.WriteResponse(code=204, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = None)


    @MicroWebSrv.route('/esp/control/i2cexpander', "POST") # Set device
    def _httpHandlerSetI2CExpander(httpClient, httpResponse):
        from components.i2c_expander import neg
        data = httpClient.ReadRequestContent()
        print("i2cexpander.data: " + str(data) + str(bin(int(data))))
        try:
            expander.write_8bit(neg(int(data)))
        except Exception as e:
            print("Exception: {0}".format(e))
            raise
        finally:
            httpResponse.WriteResponseOk(None)


    @MicroWebSrv.route('/setup/device') # Get actual device
    def _httpHandlerGetDevice(httpClient, httpResponse):
        dev = "null"

        try:
            os.stat('config/device.json')
            with open('config/device.json', 'r') as f:
                dev = f.read()
        except:
            pass

        httpResponse.WriteResponseOk(contentType = "application/json", content = dev)

    @MicroWebSrv.route('/setup/device', "POST") # Set device
    def _httpHandlerSetDevice(httpClient, httpResponse):
        data = httpClient.ReadRequestContent()

        with open('config/device.json', 'w') as f:
                f.write(data)

        httpResponse.WriteResponseOk(None)

    @MicroWebSrv.route('/setup/io') # Get IO configuration
    def _httpHandlerIOConfigGet(httpClient, httpResponse):
        from utils.io_config import io_conf_file, io_menu_layout, get_from_file as get_io_config_from_file
        io_conf = get_io_config_from_file()
        config = [ {'attr': item['attr'], 'descr': item['descr'], 'value': io_conf.get(item['attr'], None) } for item in io_menu_layout ]

        httpResponse.WriteResponseJSONOk(config)

    @MicroWebSrv.route('/setup/io', "POST") # Set IO configuration
    def _httpHandlerIOConfigSet(httpClient, httpResponse):
        from ujson import dump as json_dump
        data = httpClient.ReadRequestContentAsJSON()
        if type(data['value']) is not int:
            httpResponse.WriteResponse(code=400, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "Value is not integer")
            return

        from utils.io_config import io_conf_file, io_menu_layout, get_from_file as get_io_config_from_file
        io_conf = get_io_config_from_file()
        io_conf[data['attr']] = data['value']

        with open(io_conf_file, 'w') as f:
            json_dump(io_conf, f)

        httpResponse.WriteResponseOk(None)

    @MicroWebSrv.route('/file_list')
    def _httpHandlerTestGet(httpClient, httpResponse):
        path = "/"

        if "path" in httpClient._queryParams:
            path = httpClient._queryParams["path"]

        if len(path) > 1 and path[-1] == '/':
            path = path[:-1]

        files = [
                "{0}/".format(name)
                if os.stat(path+"/"+name)[0] & 0o170000 == 0o040000 else
                name
                for name in os.listdir(path)
                ]
        files.sort()
        content = ";".join(files)

        httpResponse.WriteResponseOk( headers = None, contentType = "text/html", contentCharset = "UTF-8", content = content )

    mws = MicroWebSrv(webPath='www/')      # TCP port 80 and files in /flash/www
    mws.LetCacheStaticContentLevel = 0
    mws.Start(threaded=True) # Starts server in a new thread
    getFree(True)
    webrepl.start()
    print("Web server started on http://{0}".format(wc.sta_if.ifconfig()[0]))
    return mws

    @MicroWebSrv.route('/esp/control/relay', "POST")
    def _httpRelaySet(httpClient, httpResponse):
        print("Relay Call")

        data = httpClient.ReadRequestContent()
        print(data)

        if RELAY is None:
            httpResponse.WriteResponse(code=500, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "RELAY is not defined, check setup()")
            return
        try:
            value = int(data)
            RELAY.value(value)
        except Exception as e:
            print("Exception: {0}".format(e))
            raise
        finally:
            httpResponse.WriteResponseOk(None)

        httpResponse.WriteResponse(code=204, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = None)


# ******** prepare / test **********
# todo: Env.set/get

class Octopus:
    def __init__(self, test):
       self.test = test

    def hello(self,name = "octopus"):
        print("hello " + name)
# **********************************
