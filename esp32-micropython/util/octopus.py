# this module is main library
# for other modules
# or directly in terminal: 
# >>> octopus()
# >>> o_help()

ver = "13.7.2019" #465
# todo object "o"

import time, os, urequests, network # import math
from os import urandom
# from micropython import const
from time import sleep, sleep_ms, sleep_us
import gc, ubinascii # machine >
from machine import Pin, I2C, PWM, SPI, Timer, ADC, RTC, unique_id

from util.buzzer import beep, play_melody
from util.led import blink
from util.pinout import set_pinout
pinout = set_pinout()
from util.io_config import get_from_file
io_conf = get_from_file()

led = None
if pinout.BUILT_IN_LED is not None:
    led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

rtc = RTC() # real time

# not all boards must have piezzo
pwm0 = None
if pinout.PIEZZO_PIN is not None:
    pwm0 = PWM(Pin(pinout.PIEZZO_PIN)) # create PWM object from a pin
    pwm0.duty(0)

WT = 50 # widt terminal / 39*=

# I2C address:
LCD_ADDR=0x27
OLED_ADDR=0x3c

#if io_conf['oled'] is not None:
from util.display_segment import threeDigits
OLEDX = 128
OLEDY = 64
OLED_x0 = 3

#adc1
#ADC/ADL
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
ad2_oldval=0
adc.atten(ADC.ATTN_11DB) # setup
adc1.atten(ADC.ATTN_11DB)
adc2.atten(ADC.ATTN_11DB)
"""
#adcpin = pinout.ANALOG_PIN
adcpin = 39 #default
pin_an = Pin(adcpin, Pin.IN)
adc = ADC(pin_an)
adc.atten(ADC.ATTN_11DB) # setup

# spi init?
try:
    #spi.deinit()
    #print("spi > close")
    spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
    ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
except:
    print("Err.SPI")

menuList = [
"   h()  /  o_help()           = this quick HELP", 
"   i()                        = basic system info",    
"   c()  /  clt()              = clear terminal",
"   f(file)                    - file info / print",
"   printOctopus()             = print ASCII logo",
">> basic simple examples:",
"   led.value(1)               | led.value(0)",
"   RGBtest()                  | Rainbow()",
"   RGB(BLUE)                  | RGBi(5,RED)",
"   np[0]=(128, 0, 0)          + np.write()",
">> SPI 8 x 7 segment display:",
"   d = disp7_init()           > disp7(d,123)",
">> I2C LCD 2/4 row display:",
"   d = lcd2_init()            > disp2(d,text,[0/1])",
"   d.clear()",
">> I2C OLED 128x64 pix display:",
'   d = oled_init()            > oled(d,"text")',
"   d.fill(0/1)  |  d.show()   | d.text(text,x,y)",
"   d.hline(*) |  d.vline(*)   | d.pixel(x,y,1)",
"   (*) x, y, w/h, color       > d.show()",
">> sensors/communications/etc.",
"   get_adc(pin)               > return analog RAW",
"   adc_test()                 > simple adc test",
"   t = temp_init()            > getTemp(t[0],t[1])",
"   i2c_scann()                = find I2C devices",
"   w()   /   w_connect()      = connect to WiFi ",
"   timeSetup()                > from URL(urlApi)",
'   get_hhmm(separator)        > get_hhmm("-")',
">> standard lib. functions:",
"   sleep(1)                   = 1 s pause",
"   urandom(1)[0]              = random num.",
"   import webrepl_setup       = remote access",
"   r() = reset()              = reset/reboot system"
]

# -------------------------------- common terminal function ---------------
def getVer():
    return "octopus lib.ver: " + ver 

def get_eui():
    id = ubinascii.hexlify(unique_id()).decode()
    return id #mac2eui(id) 

def o_help():
    printOctopus()
    print("Welcome to MicroPython on the ESP32 and octopusLAB board!")
    print("("+getVer()+")")
    printTitle("example - list commands",WT)
    for ml in menuList:
        print(ml)

def printInfo():
    print('-' * WT)
    print("ESP UID: " + get_eui() + " | RAM free: "+ str(getFree()) + " | " + get_hhmm())  
    print('-' * WT)      

def h():
    o_help()    
    printInfo()

def i():
    printTitle("basic info > ",WT)
    printInfo()

def f(file='config/device.json'):
    printTitle("file > " + file, WT)
    with open(file, 'r') as f:
            d = f.read()
            f.close()
            print(d)      

def rgb_init(num_led):
    if num_led == 0:
        return

    from util.ws_rgb import * # setupNeopixel

    if pinout.WS_LED_PIN is None:
        print("Error: WS LED not supported on this board")
        return

    pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
    npObj = setupNeopixel(pin_ws, num_led)
    np = npObj
    return npObj 

np = rgb_init(io_conf['ws'] if 'ws' in io_conf else 0)
  
def RGB(color,np=np):
    np.fill(color)
    np.write()
 
def RGBi(i,color, np=np):
    np[i] = color
    np.write()    

def RGBtest(wait=500): 
    from util.ws_rgb import simpleRgb
    simpleRgb(np,wait)

def Rainbow(wait=50):
    print("> RGB Rainbow")
    from util.ws_rgb import rainbow_cycle
    rainbow_cycle(np, io_conf['ws'],wait)

def disp7_init():
    printTitle("disp7init()",WT)
    from lib.max7219_8digit import Display
    #spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
    #ss = Pin(15, Pin.OUT)
    print("display test: octopus")
    d7 = Display(spi, ss)
    d7.write_to_buffer('octopus')
    d7.display()
    return d7

def disp7(d,mess):
    d.write_to_buffer(str(mess))
    d.display()

def i2c_scann():
    print("i2c_scann() > devices:")
    i2c = I2C(-1, Pin(pinout.I2C_SCL_PIN), Pin(pinout.I2C_SDA_PIN))
    i2cdevs = i2c.scan()
    print(i2cdevs) 
    if (OLED_ADDR in i2cdevs): print("ok > OLED: "+str(OLED_ADDR))
    if (LCD_ADDR in i2cdevs): print("ok > LCD: "+str(LCD_ADDR))
    bhLight = 0x23 in i2cdevs
    bh2Light = 0x5c in i2cdevs
    tslLight = 0x39 in i2cdevs
    return i2c   

def lcd2_init():
    printTitle("lcd2init()",WT)
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
    from util.display_segment import * 

    printTitle("oled_init()",WT)
    i2c = i2c_scann()
    OLED_ydown = OLEDY-7
    from lib import ssd1306
    time.sleep_ms(1000)
    #i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
    oled = ssd1306.SSD1306_I2C(OLEDX, OLEDY, i2c)
    print("display test: oled display OK")
    oled.text('oled display OK', OLED_x0, 3)
    # oled.text(get_hhmm(), 45,29) #time HH:MM
    oled.hline(0,50,128,1)
    oled.text("octopusLAB 2019",OLED_x0,OLED_ydown)
    oled.show()
    return oled

def oledSegment(oled,num,point=False,deg=False):
    threeDigits(oled,num,point,deg)   

def oledSegmentTest(oled):
    print("oled segment test >")
    oled.fill(0)
    oled.text('octopusLAB test', OLED_x0, 3)
    for num in range(100):
        oledSegment(oled,100-num)
        sleep_ms(50)

def oledImage(oled, file="assets/octopus_image.pbm"):
    IMAGE_WIDTH = 63
    IMAGE_HEIGHT = 63

    with open('assets/'+file, 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(data, IMAGE_WIDTH, IMAGE_HEIGHT, framebuf.MONO_HLSB)
        # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
        oled.invert(1)
        oled.blit(fbuf, 0, 0)        
    oled.show()    

def clt():
    print(chr(27) + "[2J") # clear terminal
    print("\x1b[2J\x1b[H") # cursor up

def c():
    clt()

def r():
    import machine
    machine.reset()            

octopuASCII = [
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
    for ol in octopuASCII:
        print("     " + str(ol))
    print()        

def printHead(s):
    print()
    print('-' * WT)
    print("[--- " + s + " ---] ") 

def printTitle(t,num):
    print()
    print('=' * num)
    print(t.center(num))
    print('=' * num)    

def printLog(i,s):
    print()
    print('-' * WT)
    print("[--- " + str(i) + " ---] " + s)

def getFree():
    return gc.mem_free()      

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
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh + separator + mm

# Define function callback for connecting event
"""def connected_callback(sta):
    global WSBindIP
    blink(led, 50, 100)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    blink(led, 50, 100)
"""
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

def temp_init():
    printHead("temp")
    print("dallas temp init >")
    from onewire import OneWire
    from ds18x20 import DS18X20
    dspin = Pin(pinout.ONE_WIRE_PIN)
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

    print("Found {0} dallas sensors, temp active: {1}".format(len(ts), io_conf['temp']))

    if len(ts)>1:
        print(getTempN(ds,ts))
    else: 
        print(getTemp(ds,ts))

    return ds,ts       

def getTemp(ds,ts): # return single/first value
    tw=0
    ds.convert_temp()
    sleep_ms(750)
    temp = ds.read_temp(ts[0])
    tw = int(temp*10)/10
    return tw    

def getTempN(ds,ts):
    tw=[]
    ds.convert_temp()
    sleep_ms(750)
    for t in ts:
        temp = ds.read_temp(t)
        tw.append(int(temp*10)/10)
    return tw 

def w_connect():
    if led is not None:
        led.value(1)

    from util.wifi_connect import  WiFiConnect
    sleep(1)
    w = WiFiConnect()
    if w.connect():
        print("WiFi: OK")
    else:
        print("WiFi: Connect error, check configuration")

    if led is not None:
        led.value(0)
    wlan = network.WLAN(network.STA_IF)
    print('network config:', wlan.ifconfig())
    return wlan

def w():  
    printInfo()
    printTitle("WiFi connect > ",WT)
    w_connect()  

def timeSetup(urlApi ="http://www.octopusengine.org/api/hydrop"):
    printTitle("time setup from url",WT)    
    urltime=urlApi+"/get-datetime.php"
    print("https://urlApi/"+urltime)
    try:
        response = urequests.get(urltime)
        dt_str = (response.text+(",0,0")).split(",")
        print(str(dt_str))
        dt_int = [int(numeric_string) for numeric_string in dt_str]
        rtc.init(dt_int)
        #print(str(rtc.datetime()))
        print("time: " + get_hhmm())
    except:
        print("Err. Setup time from URL")

def getApiJson(urlApi ="http://www.octopusengine.org/api"):
    import json
    urljson=urlApi+"/led3.json"
    aj = ""
    try:
        response = urequests.get(urljson)
        dt_str = (response.text)
        #print(str(dt_str))
        j = json.loads(dt_str)
        #print(str(j))
        aj = j['light'] 
    except:
        print("Err. read json from URL")  
    return aj    

def getApiTest():
    printTitle("data from url",WT)
    #print("https://urlApi/"+urljson)
    print("htts://public_unsecure_web/data.json")    
    print(getApiJson())

def getApiText(urlApi ="http://www.octopusengine.org/api"):
    import json
    urltxt=urlApi+"/text123.txt"
    try:
        response = urequests.get(urltxt)
        dt_str = response.text
    except:
        print("Err. read txt from URL")  
    return dt_str        

def octopus():
    printOctopus()
    print("("+getVer()+")")
    printInfo()
    print("This is basic library, type o_help() or h() for help")
