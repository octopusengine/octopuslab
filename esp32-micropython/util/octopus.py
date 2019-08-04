"""
 * This file is part of the octopusLAB project
 * The MIT License (MIT)
 * Copyright (c) 2016-2019 Jan Copak, Petr Kracik, Vasek Chalupnicek
"""
# this module is main library - for other modules
# or directly in terminal:
# >>> octopus()
# >>> h() help / i() info / w() wifi connect

class Env: # for temporary global variables and config setup
    from ubinascii import hexlify
    from machine import unique_id
    ver = "0.77" # version - log: num = ver*100
    verDat = "3.8.2019 #633"
    debug = True
    logDev = True
    autoInit = True
    autoTest = False
    uID = hexlify(unique_id()).decode()
    TW = 50  # terminal width

olab = Env() # for initialized equipment

from os import urandom
from time import sleep, sleep_ms, sleep_us
from machine import Pin, I2C, PWM, SPI, Timer, ADC, RTC

from util.colors import *
from util.pinout import set_pinout
from util.io_config import get_from_file

pinout = set_pinout()  # set board pinout
rtc = RTC()  # real time
io_conf = get_from_file()  # read configuration for peripherals

# I2C address:
LCD_ADDR=0x27
OLED_ADDR=0x3c

#adc1 - #ADC/ADL
"""pin_analog = 36 #pinout.I36_PIN # analog or power management
adc = ADC(Pin(pin_analog))
pin_analog_1 = 39 #I34_PIN      # x
adc1 = ADC(Pin(pin_analog_1))   # AC1 == "ACL"
pin_analog_2 = 35 #I35_PIN      # y
adc2 = ADC(Pin(pin_analog_2))

ADC_SAMPLES=100
ADC_HYSTERESIS=50
ad_oldval=0
ad1_oldval=0
adc.atten(ADC.ATTN_11DB) # setup
adc1.atten(ADC.ATTN_11DB)
"""
#adcpin = pinout.ANALOG_PIN
adcpin = 39 #default
pin_an = Pin(adcpin, Pin.IN)
adc = ADC(pin_an)
adc.atten(ADC.ATTN_11DB) # setup

# -------------------------------- common terminal function ---------------
def getVer():
    return "octopusLAB - lib.version: " + Env.ver + " > " + Env.verDat

def get_eui():
    return Env.uID #mac2eui(id)

def printInfo(w=Env.TW):
    print('-' * w)
    print("| ESP UID: " + Env.uID + " | RAM free: "+ str(getFree()) + " | " + get_hhmm())
    print('-' * w)

def o_help():
    printOctopus()
    print("Welcome to MicroPython on the ESP32 octopusLAB board")
    print("("+getVer()+")")
    printTitle("basic commands - list, examples", 53)
    help_text = """\
   setup() > octopus()        | 
   h() / o_help() HELP        | i() / o_info() INFO
   c() / clt() clear terminal | r() = system reset
   w() / w_connect()          = connect to WiFi
   f(file)                    - file info / print
   printOctopus()             = print ASCII logo
>> basic simple HW examples -------------------------
   led.value(1)  / (1)        | led.blink()
   ws = Rgb(p, n) > pin, num  | ws.simpleTest()
   ws.color(BLUE)             | RGBi(5, RED)
   beep(f, l) > freq, lenght  | tone(Notes.C5)
>> displays -----------------------------------------
   d7 = disp7_init()          > d7.show(123.567)
   d2 = lcd2_init()           > disp2(d2,text,[0/1])
   d2.clear()
   o = oled_init()            > 
   o.fill(0/1)  |  o.show()   | o.text(text, x, y)
   o.hline(*) |  d.vline(*)   | o.pixel(x, y, 1)
   (*) x, y, w/h, color       > o.show()
>> sensors/communications/... ----------------------
   get_adc(pin)               > return analog RAW
   adc_test()                 > simple adc test
   t = temp_init()    > (*t)  > getTemp(t[0], t[1])
   i2c_scann()                = find I2C devices
   time_init()                > from URL(urlApi)
   get_hhmm(separator)        > get_hhmmss("-")
>> standard lib. functions --------------------------
   sleep(1)  / sleep_ms(1)    = 1 s/ms pause
   urandom(1)[0]              = random num.
   import webrepl_setup       = remote access
"""
    print(help_text)

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

def f(file='config/device.json'):
    """print data: f("filename") """
    printTitle("file > " + file)
    with open(file, 'r') as f:
            d = f.read()
            #print(os.size(f))
            f.close()
            print(d)

def beep(f=1000,l=50):
    piezzo.beep(f,l)

def tone(f, l=300):
    piezzo.play_tone(f,l)

def rgb_init(num_led=io_conf.get('ws'), pin=None): # default autoinit ws
    if pinout.WS_LED_PIN is None:
        print("Warning: WS LED not supported on this board")
        return
    if num_led is None or num_led == 0:
        print("Warning: Number of WS LED is 0")
        return
    from util.rgb import Rgb # setupNeopixel
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
    d8 = Matrix8x8(spi, ss, 1) #1/4

    count = 6
    for i in range(count):
        d8.fill(0)
        d8.text(str(i),0,0,1)
        d8.show()
        print(i)
        sleep_ms(500)
    d8.fill(0)
    d8.show()
    return d8

def scroll(d8, text,num): # TODO speed, timer? / NO "sleep"
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

def oled_init():
    printTitle("oled_init()")
    i2c = i2c_scann()

    from util.oled import Oled
    sleep_ms(1000) 

    oled = Oled(i2c) # Oled(OLEDX, OLEDY, i2c)
    print("test oled display: OK")
    oled.test()
    return oled

try: PIN_SER = pinout.PWM1_PIN
except: PIN_SER = 17 # ROBOT
def servo_init(pin = PIN_SER):
    servo = Servo(PIN_SER)
    return servo

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
def button_init(L = 34, R = 35):
    b34 = Pin(L, Pin.IN) #SL
    b35 = Pin(R, Pin.IN) #SR
    return b34, b35

def button(pin, num=10): #num for debounce
    value0 = value1 = 0
    for i in range(num):
        if pin.value() == 0:
            value0 += 1
        else:
            value1 += 1
        sleep_us(50)
    return value0, value1

def adc_test():
    print("analog input test: ")
    #an = get_adc(adcpin)
    an = adc.read()
    print("RAW: " + str(an))
    # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
    #print("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)

def get_adc(adcpin = adcpin):
    pin_an = Pin(adcpin, Pin.IN)
    adc = ADC(pin_an)
    adc.atten(ADC.ATTN_11DB) # setup
    an = adc.read()
    return an # single read, better average

def get_adc_aver(adcpin = adcpin, num=10):
    #pin_an = Pin(adcpin, Pin.IN)
    #adc = ADC(pin_an)
    suman = 0
    for i in range(num):
        an = adc.read()
        suman = suman + an
        sleep_us(10)
    return int(suman/num) # single read, better average

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

def w_connect():
    from network import WLAN, STA_IF
    led.value(1)

    from util.wifi_connect import  WiFiConnect
    sleep(1)
    w = WiFiConnect()
    if w.connect():
        print("WiFi: OK")
    else:
        print("WiFi: Connect error, check configuration")

    led.value(0)
    wlan = WLAN(STA_IF)
    print('network config:', wlan.ifconfig())
    return wlan

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

def w():
    printInfo()
    printTitle("WiFi connect > ")
    w_connect()
    if Env.logDev: logDevice()

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
        print("led | ",end="")
        from util.led import Led
        if pinout.BUILT_IN_LED is None:
            print("Warning: BUILD-IN LED not supported on this board")
        else:
            led = Led(pinout.BUILT_IN_LED) # BUILT_IN_LED

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
        from util.display_segment import threeDigits
        from util.oled import Oled        

    if io_conf.get('temp'):
        print("temp | ",end="")

    if io_conf.get('servo'):
        print("servo | ",end="")
        from util.servo import Servo

    print()