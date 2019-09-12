"""
 * This file is part of the octopusLAB project
 * The MIT License (MIT)
 * Copyright (c) 2016-2019 Jan Copak, Petr Kracik, Vasek Chalupnicek
"""
# this module is main library - for other modules
# or directly in terminal:
# >>> octopus()
# >>> h() help /i() info /w() wifi connect

from os import urandom
from time import sleep, sleep_ms, sleep_us, ticks_ms, ticks_diff
from machine import Pin, I2C, PWM, SPI, Timer, RTC

from util.colors import *
from util.pinout import set_pinout
from util.io_config import get_from_file


class Env:  # for temporary global variables and config setup
    from ubinascii import hexlify
    from machine import unique_id
    ver = "0.87"  # version - log: num = ver*100
    verDat = "10.9.2019 #836"
    debug = True
    logDev = True
    autoInit = True
    autoTest = False
    uID = hexlify(unique_id()).decode()
    TW = 50  # terminal width
    isTimer = True
    timerFlag = 0
    timerCounter = 0
    timerLed = True
    timerBeep = False


olab = Env()  # for initialized equipment

pinout = set_pinout()  # set board pinout
rtc = RTC()  # real time
io_conf = get_from_file()  # read configuration for peripherals

# I2C address:
LCD_ADDR = 0x27
OLED_ADDR = 0x3c

if Env.isTimer:
    tim1 = Timer(0)


# -------------------------------- common terminal function ---------------
def getVer():
    return "octopusLAB - lib.version: " + Env.ver + " > " + Env.verDat


def get_eui():
    return Env.uID  # mac2eui(id)


def printInfo(w=Env.TW):
    print('-' * w)
    print("| ESP UID: " + Env.uID + " | RAM free: " + str(getFree()) + " | " + get_hhmm())
    print('-' * w)


def o_help():
    printOctopus()
    print("Welcome to MicroPython on the ESP32 octopusLAB board")
    print("("+getVer()+")")
    printTitle("basic commands - list, examples", 53)
    f("util/octopus_help.txt", False)


def h():
    o_help()
    printInfo()


def o_info():
    from os import statvfs
    from gc import mem_free
    printTitle("basic info > ")
    print("This is basic info about system and setup")
    from machine import freq
    print("> machine.freq: "+str(freq()) + " [Hz]")
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
    except:
        print("Device config 'config/device.json' does not exist, please run setup()")

    printLog("pinout")
    print(pinout)
    printLog("io_conf")
    print(io_conf)
    printInfo()


def i():
    o_info()


def f(file='main.py', title=True):
    """print data: f("filename") """
    fi = open(file, 'r')
    if title:
        printTitle("file > " + file)
        # file statistic
        lines = 0
        words = 0
        characters = 0
        for line in fi:
            wordslist = line.split()
            lines = lines + 1
            words = words + len(wordslist)
            characters = characters + len(line)

        print("Statistic > lines: " + str(lines) + " | words: " + str(words) + " | chars: " + str(characters))
        print('-' * Env.TW)
        fi = open(file, 'r')

    for line in fi:
        print(line, end="")


def u(tar="https://octopusengine.org/download/micropython/stable.tar"):
    w()
    printTitle("update from > ")
    print(tar)
    from util.setup import deploy 
    deploy(tar)


def ls(directory=""):
    printTitle("list > " + directory)
    from os import listdir
    ls = listdir(directory)
    ls.sort()
    for f in ls:
        print(f)


def file_copy(fileSource, fileTarget="main.py"):
    printTitle("file_copy to " + fileTarget)
    print("(Be careful)")
    fs = open(fileSource)
    data = fs.read()
    fs.close()
    for ii in range(12):
        print(".",end="")
        sleep_ms(300)
    ft = open(fileTarget, 'w')
    ft.write(data)
    ft.close()
    print(" ok")


def beep(f=1000, l=50):  # noqa: E741
    piezzo.beep(f, l)


def tone(f, l=300):  # noqa: E741
    piezzo.play_tone(f, l)


def rgb_init(num_led=io_conf.get('ws'), pin=None):  # default autoinit ws
    if pinout.WS_LED_PIN is None:
        print("Warning: WS LED not supported on this board")
        return
    if num_led is None or num_led == 0:
        print("Warning: Number of WS LED is 0")
        return
    from util.rgb import Rgb  # setupNeopixel
    ws = Rgb(pin, num_led)
    return ws


def disp7_init():
    printTitle("disp7init()")
    from util.display7 import Display7
    print("display test: octopus")
    d7 = Display7(spi, ss)
    d7.write_to_buffer('octopus')
    d7.display()
    return d7


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


def i2c_scann(printInfo=True):
    if printInfo: print("i2c_scann() > devices:")
    i2c = I2C(-1, Pin(pinout.I2C_SCL_PIN), Pin(pinout.I2C_SDA_PIN))
    i2cdevs = i2c.scan()
    if printInfo: print(i2cdevs)
    if (OLED_ADDR in i2cdevs): 
        if printInfo: print("ok > OLED: "+str(OLED_ADDR))
    if (LCD_ADDR in i2cdevs): 
        if printInfo: print("ok > LCD: "+str(LCD_ADDR))
    bhLight = 0x23 in i2cdevs
    bh2Light = 0x5c in i2cdevs
    tslLight = 0x39 in i2cdevs
    return i2c


def lcd2_init():
    printTitle("lcd2init()")
    i2c = i2c_scann()
    LCD_ROWS=2
    LCD_COLS=16
    from lib.esp8266_i2c_lcd import I2cLcd
    lcd = I2cLcd(i2c, LCD_ADDR, LCD_ROWS, LCD_COLS)
    print("display test: octopusLAB")
    lcd.clear()
    lcd.putstr("octopusLAB")
    return lcd


def disp2(d,mess,r=0,s=0):
    #d.clear()
    d.move_to(s, r) # x/y
    d.putstr(str(mess))


def oled_init(ox=128, oy=64, runTest = True):
    printTitle("oled_init()")
    i2c = i2c_scann()

    from util.oled import Oled
    from util.display_segment import threeDigits
    sleep_ms(1000) 

    oled = Oled(i2c, ox, oy)
    print("test oled display: OK")
    if runTest:
        oled.test()
        threeDigits(oled,123)

    return oled

try: PIN_SER = pinout.PWM1_PIN
except: PIN_SER = 17 # ROBOT
def servo_init(pin = PIN_SER):
    servo = Servo(PIN_SER)
    return servo


def stepper_init(ADDRESS = 0x23, MOTOR_ID = 1): # ID 1 / 2
    motor = SM28BYJ48(i2c, ADDRESS, MOTOR_ID)
    # turn right 90 deg
    motor.turn_degree(90, 0)
    # turn left 90 deg
    motor.turn_degree(90, 1)
    return motor


def clt():
    print(chr(27) + "[2J") # clear terminal
    print("\x1b[2J\x1b[H") # cursor up


def c():
    clt()


def r():
    import machine
    machine.reset()


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
        print("     " + str(ol))
    print()


def printHead(s):
    print()
    print('-' * Env.TW)
    print("[--- " + s + " ---] ")


def printTitle(t,w=Env.TW):
    print()
    print('=' * w)
    print("|",end="")
    print(t.center(w-2),end="")
    print("|")
    print('=' * w)


def printLog(i,s=""):
    print()
    print('-' * Env.TW)
    print("[--- " + str(i) + " ---] " + s)


def getFree():
    from gc import mem_free
    return mem_free()


def printFree():
    print("Free: "+str(getFree()))


def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)


def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)


def add0(sn):
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str


def get_hhmm(separator=":",rtc=rtc):
    """get_hhmm(separator) | separator = string: "-" / " " """
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh + separator + mm


def get_hhmmss(separator=":",rtc=rtc):
    """get_hhmm(separator) | separator = string: "-" / " " """
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    ss=add0(rtc.datetime()[6])
    return hh + separator + mm + separator + ss

# Define function callback for connecting event
"""def connected_callback(sta):
    global WSBindIP
    blink(led, 50, 100)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    blink(led, 50, 100)
"""
def timer_init():
    printLog("timer_init")
    print("timer tim1 is ready - periodic - 10s")
    print("for deactivite: tim1.deinit()")
    tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerAction())
    Env.timerCounter = 0


def timerAction():
    print("timerAction " + str(Env.timerCounter))
    Env.timerFlag = 1
    Env.timerCounter += 1
    if Env.timerLed: led.blink(100, 50)
    if Env.timerBeep: beep()
    Env.timerFlag = 0   


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

#test for Shield1 or FirstBoard hack buttons
def buttons_init(L = 34, R = 35, C = 39): # Left, Right, Central
    b34 = Pin(L, Pin.IN) #SL
    b35 = Pin(R, Pin.IN) #SR
    b39 = Pin(C, Pin.IN)
    return b34, b35, b39

def button_init(pin = 34):
    bpin = Pin(pin, Pin.IN)
    return bpin

def button(pin, num=10): #num for debounce
    value0 = value1 = 0
    for i in range(num):
        if pin.value() == 0:
            value0 += 1
        else:
            value1 += 1
        sleep_us(50)
    return value0, value1

try: PIN_TEMP = pinout.ONE_WIRE_PIN
except: PIN_TEMP = 17 # ROBOT
def temp_init(pin = PIN_TEMP):
    printHead("temp")
    print("dallas temp init >")
    from onewire import OneWire
    from ds18x20 import DS18X20
    dspin = Pin(pin)
    # from util.octopus_lib import bytearrayToHexString
    try:
        ds = DS18X20(OneWire(dspin))
        ts = ds.scan()

        if len(ts) <= 0:
            io_conf['temp'] = False

        for t in ts:
            print(" --{0}".format(bytearrayToHexString(t)))
    except:
        io_conf['temp'] = False
        print("Err.temp")

    print("Found {0} dallas sensors, temp active: {1}".format(len(ts), io_conf.get('temp')))

    if len(ts)>1:
        print(get_temp_n(ds,ts))
    else:
        print(get_temp(ds,ts))

    return ds,ts

def get_temp(ds,ts): # return single/first value
    """get_temp(t[0],t[1]) or get_temp(*t)"""
    tw=0
    ds.convert_temp()
    sleep_ms(750)
    temp = ds.read_temp(ts[0])
    tw = int(temp*10)/10
    return tw

def get_temp_n(ds,ts):
    tw=[]
    ds.convert_temp()
    sleep_ms(750)
    for t in ts:
        temp = ds.read_temp(t)
        tw.append(int(temp*10)/10)
    return tw

def ap_init(): #192.168.4.1
    printTitle("AP init > ")
    import network
    import ubinascii
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    mac = ubinascii.hexlify(ap.config('mac'),':').decode()
    ap.config(essid="octopus_ESP32_" + mac)
    print(ap.ifconfig())
    print("AP Running: " + ap.config("essid"))
    return ap

def w_connect():
    led.value(1)

    from util.wifi_connect import WiFiConnect
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
    lan = LAN(mdc = Pin(23), mdio=Pin(18), phy_type=PHY_LAN8720, phy_addr=1, clock_mode=ETH_CLOCK_GPIO17_OUT)
    lan.active(1)

    retry = 0
    while not lan.isconnected() or lan.ifconfig()[0] is '0.0.0.0':
        retry+=1
        sleep_ms(500)

        if retry > 20:
            break;

    if not lan.isconnected():
        print("LAN: Connect error, check cable or DHCP server")
        return None

    print("LAN: OK")
    led.value(0)
    print('network config:', lan.ifconfig())
    return lan

def logDevice(urlPOST = "http://www.octopusengine.org/iot17/add18.php"):
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
    except:
        print("E.logDevice")

def w(logD = True):
    printInfo()
    printTitle("WiFi connect > ")
    w_connect()
    if logD and Env.logDev: logDevice()

def database_init(name):
    from util.database import Db
    db = Db(name)
    return db

def time_init(urlApi ="http://www.octopusengine.org/api/hydrop"):
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
    except:
        print("Err. Setup time from URL")

def getApiJson(urlApi ="http://www.octopusengine.org/api"):
    from urequests import get
    from json import loads
    urljson=urlApi+"/led3.json"
    aj = ""
    try:
        response = get(urljson)
        dt_str = (response.text)
        #print(str(dt_str))
        j = loads(dt_str)
        #print(str(j))
        aj = j['light']
    except:
        print("Err. read json from URL")
    return aj

def getApiTest():
    printTitle("data from url")
    #print("https://urlApi/"+urljson)
    print("htts://public_unsecure_web/data.json")
    print(getApiJson())

def getApiText(urlApi ="http://www.octopusengine.org/api"):
    from urequests import get
    urltxt=urlApi+"/text123.txt"
    try:
        response = get(urltxt)
        dt_str = response.text
    except:
        print("Err. read txt from URL")
    return dt_str

def octopus():
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

# --------------- init --------------
if Env.autoInit:  # test
    print("--> autoInit: ",end="")
    if io_conf.get('led7') or io_conf.get('led8'):
        print("SPI | ",end="")
        spi = None
        ss  = None
        try:
            #spi.deinit() #print("spi > close")
            spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
            ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
        except:
            print("Err.spi")

    if io_conf.get('oled') or io_conf.get('lcd'):
        print("I2C | ",end="")
        try:
            i2c = i2c_scann(False)
        except:
            print("Err.i2c")

    if io_conf.get('led'):
        print("Led | ",end="")
        from util.led import Led
        if pinout.BUILT_IN_LED is None:
            print("Warning: BUILD-IN LED not supported on this board")
            led = Led(None)
        else:
            led = Led(pinout.BUILT_IN_LED) # BUILT_IN_LED
    else:
        from util.led import Led
        led = Led(None)

    piezzo = None
    if io_conf.get('piezzo'):
        print("piezzo | ",end="")
        from util.buzzer import Buzzer
        piezzo = Buzzer(pinout.PIEZZO_PIN)
        piezzo.beep(1000,50)
        from util.buzzer import Notes
    # else:   #    piezzo =Buzzer(None)

    if io_conf.get('ws'): 
        print("ws | ",end="")
        from util.rgb import Rgb
        if pinout.WS_LED_PIN is None:
            print("Warning: WS LED not supported on this board")
        else:
            ws = Rgb(pinout.WS_LED_PIN,io_conf.get('ws')) # default rgb init

    if io_conf.get('oled'):
        print("OLED | ",end="")
        from assets.icons9x9 import ICON_clr, ICON_wifi
        from util.display_segment import oneDigit, threeDigits
        from util.oled import Oled

    if io_conf.get('ad0') or io_conf.get('ad1') or io_conf.get('ad2'):
        print("Analog | ",end="")
        from util.analog import Analog
        #adcpin = pinout.ANALOG_PIN
        adcpin = 39 #default
        an = Analog(adcpin)
        #an0 = Analog(io_conf.get('ad0'))

    if io_conf.get('temp'):
        print("temp | ",end="")

    if io_conf.get('servo'):
        print("servo | ",end="")
        from util.servo import Servo

    if io_conf.get('stepper'):
        print("stepper | ",end="")
        from lib.sm28byj48 import SM28BYJ48   #PCF address = 35 #33-0x21/35-0x23
                  
    print()

def small_web_server(wPath='www/'):
    from lib.microWebSrv import MicroWebSrv
    # ? webPath as parameter
    mws = MicroWebSrv(webPath=wPath)      # TCP port 80 and files in /flash/www
    mws.Start(threaded=True) # Starts server in a new thread
    print("Web server started > " + wPath)

def web_server():
    print("Web setup test > ")
    from lib.microWebSrv import MicroWebSrv
    import os
    import webrepl

    from util.wifi_connect import WiFiConnect
    wc = WiFiConnect()

    wcss = """<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: Silver; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: Orange; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: Navy;}</style>"""
    html = """<html><head> <title>octopus ESP setup</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> """ + wcss + """
    <script>function autoFill(ssid){document.getElementById('fssid').value = ssid;}</script>
    </head><body> <h1>octopusLAB - ESP WiFi setup</h1>
    """
    web_form = """
    <form method="POST">
    ssid: <br><input id="fssid" type="text" name="ssid"><br>
    password: <br><input type="text" name="pass"><br><br>
    <input type="submit" value="Submit">
    </form>"""

    @MicroWebSrv.route('/setup/wifi/networks.json') # GET
    def _httpHandlerWiFiNetworks(httpClient, httpResponse):
        from ubinascii import hexlify
        nets = [[item[0], hexlify(item[1]), item[2], item[3], item[4]] for item in wc.sta_if.scan()]
        httpResponse.WriteResponseJSONOk(nets)

    @MicroWebSrv.route('/setup/wifi/savednetworks.json') # GET
    def _httpHandlerWiFiNetworks(httpClient, httpResponse):
        nets = [k for k,v in wc.config['networks'].items()]
        httpResponse.WriteResponseJSONOk(nets)

    @MicroWebSrv.route('/setup/wifi/network', "POST")   # Create new network
    @MicroWebSrv.route('/setup/wifi/network', "PUT")    # Update existing network
    @MicroWebSrv.route('/setup/wifi/network', "DELETE") # Delete existing network
    def _httpHandlerWiFiAddNetwork(httpClient, httpResponse):
        data  = httpClient.ReadRequestContentAsJSON()
        method = httpClient.GetRequestMethod()
        responseCode = 500
        content = None

        print(method)
        print(data)

        if len(data) < 1:
            responseCode = 400
            content = "Missing ssid in request"
            httpResponse.WriteResponse( code=400, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)
            return

        if method == "POST":
            ssid = data[0]
            psk = data[1] if len(data) > 1 else ""
            print("Creating network {0}".format(data[0]))
            state = wc.add_network(ssid, psk)
            if state:
                responseCode = 201
            else:
                responseCode = 400
                content = "Error while add network"

        httpResponse.WriteResponse( code=responseCode, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)

    @MicroWebSrv.route('/setup/wifi/addnetwork', "POST") # GET
    def _httpHandlerWiFiAddNetwork(httpClient, httpResponse):
        formData  = httpClient.ReadRequestPostedFormData()
        validData = True
        ssid = None
        psk = None
        content = ""

        if not "ssid" in formData:
            content += "Error: Missing SSID in request"
            validData = False
        else:
            ssid = formData['ssid']

        if not "psk" in formData:
            validData = False
            content += "<br/>Error: Missing network key in request"
        else:
            psk = formData['psk']

        if validData:
            #wc.add_network()
            content = "Saved network"
            httpResponse.WriteResponseOk( headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)
        else:
            httpResponse.WriteResponse( code=400, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = content)


    @MicroWebSrv.route('/setup_wifi')          # GET
    @MicroWebSrv.route('/setup_wifi', "POST")  # POST
    def _httpHandlerTestGet(httpClient, httpResponse):
        method = httpClient.GetRequestMethod()
        formData  = httpClient.ReadRequestPostedFormData()
        queryparams = httpClient.GetRequestQueryParams()
        reqCont = httpClient.ReadRequestContent()
        print ("Method {0}".format(method))
        print ("Req content")
        print(reqCont)
        print ("Form data")
        print(formData)
        print ("Query params")
        print(queryparams)

        content = html
        content += web_form
        if "ssid" in formData:
            content += "ssid: <b>{0}</b><br/><br/>".format(MicroWebSrv.HTMLEscape(formData['ssid']))
        if "pass" in formData:
            content += "pass: <b>{0}</b><br/><br/>".format(MicroWebSrv.HTMLEscape(formData['pass']))

        webWc = "<hr /><b>Saved networks: </b><br />"
        for k, v in wc.config['networks'].items():
            webWc += k + "<br />"

        content += webWc
        content += "Method: {0}<br/>".format(method)
        content += "Request content: <br/><p>"
        content += reqCont.decode()
        content += "</p>Request Form data: <br/><p>"
        content += ",".join([ "{0}={1}".format(pair, formData[pair]) for pair in formData ])
        content += "</p>Request query params: <br/><p>"
        content += ",".join([ "{0}={1}".format(pair, queryparams[pair]) for pair in queryparams ])
        content += "</p></body></html>"

        httpResponse.WriteResponseOk( headers = None, contentType = "text/html", contentCharset = "UTF-8", content = content)

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
    mws.Start(threaded=True) # Starts server in a new thread
    print("Web editor started")
    webrepl.start()
