# this module is main library - for other modules
# or directly in terminal: 
# >>> octopus()
# >>> h() help / i() info / w() wifi connect

class var: # for temporary global variables and config setup
    # var.xy = value
    pass

var.ver = "0.75" # log: num = ver*100
var.verDat = "30.7.2019 #677" 
var.debug = True
var.autoTest = False
# Led, Buzzer > class: rgb, oled, servo, stepper, motor, pwm, relay, lan? 

import time, os, urequests, network # import math
from os import urandom
# from micropython import const
from time import sleep, sleep_ms, sleep_us
import gc, ubinascii # machine >
from machine import Pin, I2C, PWM, SPI, Timer, ADC, RTC, unique_id
var.uID = ubinascii.hexlify(unique_id()).decode()

from util.pinout import set_pinout
pinout = set_pinout()

try: LED_PIN = pinout.BUILT_IN_LED
except: LED_PIN = 2

from util.io_config import get_from_file
io_conf = get_from_file()

rtc = RTC() # real time
WT = 50 # widt terminal / 39*=
var.logDev = True
np = None

# I2C address:
LCD_ADDR=0x27
OLED_ADDR=0x3c

#if io_conf['oled'] is not None:
OLEDX = 128
OLEDY = 64
OLED_x0 = 3

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

menuList = [
"   h() / o_help() = HELP      | i() /o_info() = INFO", 
"   c() / clt() clear terminal | r() = system reset",
"   w() / w_connect()          = connect to WiFi ",
"   f(file)                    - file info / print",
"   printOctopus()             = print ASCII logo",
">> basic simple HW examples:",
"   led.value(1)               | led.value(0)",
"   RGBtest()                  | Rainbow()",
"   RGB(BLUE)                  | RGBi(5,RED)",
"   np[0]=(128, 0, 0)          + np.write()",
"   beep(f,l) > freq, lenght   | tone(Notes.C5)",
">> SPI 8 x 7 segment display:",
"   d = disp7_init()           > disp7(d,123)",
"   d.display_text(txt)        d.display_num(123.567)",
">> I2C LCD 2/4 row display:",
"   d = lcd2_init()            > disp2(d,text,[0/1])",
"   d.clear()",
">> I2C OLED 128x64 pix display:",
'   o = oled_init()            > oled(o,"text")',
"   o.fill(0/1)  |  o.show()   | o.text(text,x,y)",
"   o.hline(*) |  d.vline(*)   | o.pixel(x,y,1)",
"   (*) x, y, w/h, color       > o.show()",
">> sensors/communications/etc.",
"   get_adc(pin)               > return analog RAW",
"   adc_test()                 > simple adc test",
"   t = temp_init()            > getTemp(t[0],t[1])",
"   i2c_scann()                = find I2C devices",
"   timeSetup()                > from URL(urlApi)",
'   get_hhmm(separator)        > get_hhmm("-")',
">> standard lib. functions:",
"   sleep(1)  / sleep_ms(1)    = 1 s/ms pause",
"   urandom(1)[0]              = random num.",
"   import webrepl_setup       = remote access",
]

# -------------------------------- common terminal function ---------------
def getVer():
    return "octopusLAB - lib.version: " + var.ver + " > " + var.verDat

def get_eui():
    return var.uID #mac2eui(id) 

def printInfo(w=WT):
    print('-' * w)
    print("| ESP UID: " + var.uID + " | RAM free: "+ str(getFree()) + " | " + get_hhmm())  
    print('-' * w)      

def o_help():
    printOctopus()
    print("Welcome to MicroPython on the ESP32 octopusLAB board")
    print("("+getVer()+")")
    printTitle("example - list commands")
    for ml in menuList:
        print(ml)

def h():
    o_help()    
    printInfo()

def o_info():
    printTitle("basic info > ")
    print("This is basic info about system and setup")
    from machine import freq
    print("> machine.freq: "+str(freq()) + " [Hz]")
    printLog("memory")
    print("> ram free: "+str(gc.mem_free()) + " [B]")
    #print("> flash: "+str(os.statvfs("/")))
    ff =int(os.statvfs("/")[0])*int(os.statvfs("/")[3])
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
    """ print data: f("filename") """
    printTitle("file > " + file)
    with open(file, 'r') as f:
            d = f.read()
            #print(os.size(f))
            f.close()
            print(d) 

try: PIN_WS = pinout.WS_LED_PIN
except: PIN_WS = 15
def rgb_init(num_led, pin = PIN_WS):
    if num_led is None or num_led == 0:
        return
    from util.ws_rgb import * # setupNeopixel
    np = setupNeopixel(Pin(pin, Pin.OUT), num_led)
    return np          

def beep(f=1000,l=50):
    piezzo.beep(f,l)

def tone(f, l=300): 
    piezzo.play_tone(f,l)
  
def disp7_init():
    printTitle("disp7init()")
    from lib.max7219_8digit import Display
    #spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
    #ss = Pin(15, Pin.OUT)
    print("display test: octopus")
    d7 = Display(spi, ss)
    d7.write_to_buffer('octopus')
    d7.display()
    return d7

def disp8_init():
    printTitle("disp8init()")
    from lib.max7219 import Matrix8x8
    d8 = Matrix8x8(spi, ss, 1) #1/4
    #print("SPI device already in use")

    count = 6
    for i in range(count):
        d8.fill(0)
        d8.text(str(i),0,0,1)
        d8.show()
        print(i)
        time.sleep_ms(500)

    d8.fill(0)
    d8.show()
    return d8

def scroll(d8, text,num): # TODO speed, timer? / NO "sleep"
    WIDTH = 8*4
    x = WIDTH + 2
    for _ in range(8*len(text)*num):
        time.sleep(0.03)
        d8.fill(0)
        x -= 1
        if x < - (8*len(text)):
            x = WIDTH + 2
        d8.text(text, x, 0, 1)
        d8.show()
    d8.fill(0)
    d8.show()    

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
    from util.display_segment import * 
    printTitle("oled_init()")
    i2c = i2c_scann()
    OLED_ydown = OLEDY-7
    from lib import ssd1306
    time.sleep_ms(1000)
    #i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
    oled = ssd1306.SSD1306_I2C(OLEDX, OLEDY, i2c)
    print("display test: oled display OK")
    oled.text('oled display OK', OLED_x0, 3)
    # oled.text(get_hhmm(), 45,29) #time HH:MM
    oled.hline(0,52,128,1)
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

def draw_icon(oled, icon, posx, posy):
    for y, row in enumerate(icon):
        for x, c in enumerate(row):
            oled.pixel(x+posx, y+posy, c) 
    oled.show()                

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

try: PIN_SER = pinout.PWM1_PIN
except: PIN_SER = 17 # ROBOT
def servo_init(pin = PIN_SER):
    SERVO_MIN = const(45)
    pwm_center = const(60)
    SERVO_MAX = const(130)
    pin_servo = Pin(pin, Pin.OUT)
    servo = PWM(pin_servo, freq=50, duty=pwm_center)
    return servo

def set_degree(servo, angle):
    servo.duty(map(angle, 0,150, SERVO_MIN, SERVO_MAX))      

def set_degree(servo, angle):
    servo.duty(map(angle, 0,150, SERVO_MIN, SERVO_MAX))            

def servo_test():
    printTitle("servo1 test >")
    #pwm_center = int(pinout.SERVO_MIN + (pinout.SERVO_MAX-pinout.SERVO_MIN)/2)

    #if notInitServo:
    print("init-servo:")
    servo1 = servo_init()
                
    sleep(2)
    servo1.duty(SERVO_MAX)
    sleep(2)
    servo1.duty(SERVO_MIN)
    sleep(2)
    
    print("degree > 0")
    set_degree(servo1,0)
    sleep(2) 
    print("degree > 45")
    set_degree(servo1,45) 
    sleep(2) 
    print("degree > 90")
    set_degree(servo1,90) 

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
    print('-' * WT)
    print("[--- " + s + " ---] ") 

def printTitle(t,w=WT):
    print()
    print('=' * w)
    print("|",end="")
    print(t.center(w-2),end="")
    print("|")
    print('=' * w)

def printLog(i,s=""):
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
    led.value(1)

    from util.wifi_connect import  WiFiConnect
    sleep(1)
    w = WiFiConnect()
    if w.connect():
        print("WiFi: OK")
    else:
        print("WiFi: Connect error, check configuration")

    led.value(0)
    wlan = network.WLAN(network.STA_IF)
    print('network config:', wlan.ifconfig())
    return wlan

def logDevice(urlPOST = "http://www.octopusengine.org/iot17/add18.php"):
    header = {}
    header["Content-Type"] = "application/x-www-form-urlencoded"
    deviceID = var.uID
    place = "octoPy32"
    logVer =  int(float(var.ver)*100)
    try:
        postdata_v = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, logVer,"log_ver")
        res = urequests.post(urlPOST, data=postdata_v, headers=header)
        sleep_ms(100)
        print("logDevice.ok")  
    except:
        print("E.logDevice")    

def w():  
    printInfo()
    printTitle("WiFi connect > ")
    w_connect()
    if var.logDev: logDevice() 

def timeSetup(urlApi ="http://www.octopusengine.org/api/hydrop"):
    printTitle("time setup from url")    
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
    printTitle("data from url")
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

def octopus(autoIni = False): # automaticaly start init_X according to the settings io_conf.get(X)
    var.autoIni = autoIni
    printOctopus()
    print("("+getVer()+")")
    gc.collect()
    printInfo()
    print("This is basic library, type h() for help")

# --------------- init --------------
if True: # var.autoIni: //test
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
            print("Err.SPI")

    if io_conf.get('led'):
        print("led | ",end="")
        from util.led import Led
        led = Led(LED_PIN) # BUILT_IN_LED

    piezzo = None
    if io_conf.get('piezzo'):
        print("piezzo | ",end="")
        from util.buzzer import Buzzer
        piezzo = Buzzer(pinout.PIEZZO_PIN)
        piezzo.beep(1000,50)
        from util.buzzer import Notes
    # else:
    #    piezzo =Buzzer(None)

    if io_conf.get('ws'):
        print("WS | ",end="")
        if pinout.WS_LED_PIN is None:
            print("Warning: WS LED not supported on this board")
        else:    
            np = rgb_init(io_conf.get('ws'))  

    if io_conf.get('oled'):
        print("OLED lib | ",end="")
        from assets.icons9x9 import ICON_clr, ICON_wifi 
        from util.display_segment import threeDigits 

    if io_conf.get('servo'): 
        print("servo | ",end="")  

    print()
# --------------- after init ---------------
# for example: np was still None, need init before
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
    rainbow_cycle(np, io_conf.get('ws'), wait)        