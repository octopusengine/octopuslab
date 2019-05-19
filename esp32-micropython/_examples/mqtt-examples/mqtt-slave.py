"""
octopusLAB - ESP32 easy - MQTT "slave" manager
need ROBOTboard or IoTboard (it depends on the project)
Built in Led, WS RGB Led
Inputs: 
Button, keyboard, analog Joystick
Sensors: A/D, One wire temperature, I2C light, ...
Outputs: 
Relay, MOS-FER PWM (IoT board)
Servo, DC motor, stepper (Robot board)
Displays: 
I2C OLED, I2C LCD, SPI 8x7 segment, SPI 4x 8x8 matrix, UART Nextion, UART Serial display, SPI TTF...
"""

import machine, time, ubinascii, json
from time import sleep
from machine import Pin, Timer, PWM, SPI
from neopixel import NeoPixel
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config
from util.octopus_lib import *
from umqtt.simple import MQTTClient
#from util.iot_garden import * # fade_
from onewire import OneWire
from ds18x20 import DS18X20

from util.pinout import set_pinout
pinout = set_pinout()

printLog(1,"boot device >")
print("mqtt-slave.py > ESP32")
ver = "0.31 / 19.5.2019"

# hard-code config / daefault
Debug = True        # TODO: debugPrint()?
minute = 10         # 1/10 for data send
timeInterval = 1
wifi_retries = 100  # for wifi connecting

#* = todo / ## = automatic
# Inputs - sensors
isTemp = 0      #  temperature
isLight = 0     #  light (lux)
isMois = 0      #* moisture
isAD = 0        #* A/D input voltage
isAD1 = 0       #  A/D x / photoresistor
isAD2 = 0       #  A/D y / thermistor
# Outpusts
isServo = 1     # Have PWM pins
isFET = 0       # We have FET
isRelay = 0     # Have Relay
# Displays / LED
isWS = 0        #  WS RGB LED 0/1/8/...n
isLed7 = 0      #  SPI max 8x7 segm.display
isLed8 = 0      #  SPI max 8x8 matrix display
isOLED = 1      ##  I2C
isLCD = 0       ##* I2C
isSD = 0        #* UART
isServo = 1     # Have PWM pins
isFET = 1       # We have FET
isRelay = 1     # Have Relay

# testing simple orchestrator connection manager
cm_Light2M8 = 0
cm_Light2M8brightness = 0

#
LCD_ADDRESS=0x27
LCD_ROWS=2
LCD_COLS=16

#OLED size and position
OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7

#ADC/ADL
pin_analog = 36         # analog or power management 
adc = ADC(Pin(pin_analog))
pin_analog_1 = 34       # x
adc1 = ADC(Pin(pin_analog_1)) # AC1 == "ACL"
pin_analog_2 = 35       # y
adc2 = ADC(Pin(pin_analog_2))

ADC_SAMPLES=100
ADC_HYSTERESIS=50
ad_oldval=0
ad1_oldval=0
ad2_oldval=0
adc.atten(ADC.ATTN_11DB) # setup
adc1.atten(ADC.ATTN_11DB) 
adc2.atten(ADC.ATTN_11DB) 

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)

pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
np = NeoPixel(pin_ws, 1)
ws_r = 0
ws_g = 0
ws_b = 0

if isServo:
    pwm1 = PWM(Pin(pinout.PWM1_PIN), freq=50, duty=70)
    pwm2 = PWM(Pin(pinout.PWM2_PIN), freq=50, duty=70)
    pwm3 = PWM(Pin(pinout.PWM3_PIN), freq=50, duty=70)

# only for IoT board
if isFET:
    fet = PWM(Pin(pinout.MFET_PIN, Pin.OUT))
    fet.duty(0)
    fet.freq(2000)

if isRelay:
    rel = Pin(pinout.RELAY_PIN, Pin.OUT)    

rtc = machine.RTC() # real time
tim1 = Timer(0)     # for main 10 sec timer

print("ver: " + ver + " (c)octopusLAB")
esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print("id: " + esp_id)

printLog(2,"init - variables and functions >")

bd = bytes.decode

# Set up I2C
if Debug: print("init i2c >")
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
# i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN), freq=100000) # 100kHz because PCF is slow
if Debug: print(" - scanning")
i2cdevs = i2c.scan()
if Debug: print(" - devices: {0}".format(i2cdevs))

# Determine what we have connected to I2C
isOLED = 0x3c in i2cdevs
bhLight = 0x23 in i2cdevs
bh2Light = 0x5c in i2cdevs
tslLight = 0x39 in i2cdevs


io_config = {}
def loadConfig():
    global isWS, isOLED, isLCD, isLed7, isLed8, isAD, isAD1, isAD2, isTemp, isServo
       
    configFile = 'config/mqtt_io.json'
    if Debug: print("load "+configFile+" >")
    try:
        with open(configFile, 'r') as f:
            d = f.read()
            f.close()
            io_config = json.loads(d)

        isWS = io_config.get('ws')
        isOLED = io_config.get('oled')
        isLCD = io_config.get('lcd')
        isLed7 = io_config.get('8x7')
        isLed8 = io_config.get('8x8')
        isAD = io_config.get('adv')
        isAD1 = io_config.get('adv1')
        isAD2 = io_config.get('adv2')
        isTemp = io_config.get('temp')
        isServo = io_config.get('servo')

        print("isWS: " + str(isWS)) 
        print("isOLED: " + str(isOLED))  
        print("isLCD: " + str(isLCD))  
        print("isLed7: " + str(isLed7)) 
        print("isLed8: " + str(isLed8)) 
        print("isAD: " + str(isAD))  
        print("isAD1: " + str(isAD1))  
        print("isAD2: " + str(isAD2)) 
        print("isTemp: " + str(isTemp))
        print("isServo: " + str(isServo))

    except:
        print("Data Err. or '"+ configFile + "' does not exist")
  

oled = 0
def oled_intit():
    print("OLED present: {0}".format(isOLED))
    global oled
    from lib import ssd1306
    sleep(1)
    oled = ssd1306.SSD1306_I2C(OLEDX, OLEDY, i2c)

def displMessage2(mess,timm): # OLEDdisplMessage()
    #TODO: OLED/TFT/LCD...
    try:
        oled.fill_rect(0,OLED_ydown,OLEDX,10,0)
        oled.text(mess, OLED_x0, OLED_ydown)
        oled.show()
        time.sleep_ms(timm*1000)
    except Exception as e:
       print("Err. displMessage() Exception: {0}".format(e)) 

def displMessage(mess,timm):
    try:
        oled.fill_rect(0,OLED_ydown-17,OLEDX,10,0)
        oled.text(mess, OLED_x0, OLED_ydown-17)
        oled.show()
        time.sleep_ms(timm*1000)
    except Exception as e:
       print("Err. displMessage2() Exception: {0}".format(e))  

def scroll(text,num): # TODO speed, timer? / NO "sleep"
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

def getTemp():
    tw=999
    if isTemp:
        ds.convert_temp()
        sleep_ms(750)
        for t in ts:
            temp = ds.read_temp(t)
            tw = int(temp*10)
    return tw

def get_adc_value(inAdc):
    aval = 0
    for i in range(0, ADC_SAMPLES):
        aval += inAdc.read()
    return aval // ADC_SAMPLES

def timerInit():
    tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerSend()) 

def timeSetup():
    if Debug: print("time setup >")
    urlApi ="http://www.octopusengine.org/api/hydrop/"
    urltime=urlApi+"/get-datetime.php"
    try:
        response = urequests.get(urltime)
        dt_str = (response.text+(",0,0")).split(",")
        print(str(dt_str))
        dt_int = [int(numeric_string) for numeric_string in dt_str]
        rtc.init(dt_int)
        print(str(rtc.datetime()))
    except:
        print("Err. Setup time from WiFi")    
    
def simple_blink():
    pin_led.value(1)
    sleep(0.1)
    pin_led.value(0)
    sleep(0.1) 

def fade_sw_in(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(0)
          time.sleep_us((r-i)*m*2) # multH/L *2
          p.value(1)
          time.sleep_us(i*m)

def fade_sw_out(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(1)
          time.sleep_us((r-i)*m)
          p.value(0)
          time.sleep_us(i*m*2)      

def test7seg():     
     d7.write_to_buffer('octopus')
     d7.display()

def sendData():
    print("sendData()") 
    if isTemp:  
        temp10 = int(ts.read_temp()*10)
        publishTopic = "octopus/{0}/temp/{1}".format(esp_id,temp)
        print(str("publishTopic: ".publishTopic))        
        c.publish("/octopus/device/{0}/temp/".format(esp_id),str(temp10/10))      

it = 0 # every 10 sec.
def timerSend():
    global it
    it = it+1
    if Debug: print("timer > "+str(it))

    """
    if isLed7:
        if isTemp:
            d7.write_to_buffer(str(it)+"-"+str(int(getTemp())))
            d7.display()
        else:
            d7.write_to_buffer(str(it))
            d7.display()        
    """
    if isOLED:
        displMessage2(str(it) + " | " + str(get_hhmm(rtc)),1)    

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    #np[0] = (0, 128, 0)
    #np.write()
    simple_blink()
    print(sta.ifconfig())

def connecting_callback(retries):
    #np[0] = (0, 0, 128)
    #np.write()
    simple_blink()

def mqtt_sub(topic, msg):
    global ws_r
    global ws_g
    global ws_b

    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:")
        data = bd(msg)

        if data[0] == 'N':  # oN
            print("-> on")
            pin_led.value(1)
            #c.publish(mqtt_root_topic+esp_id,1)

        elif data[0] == 'F':  # ofF 
            print("-> off")
            pin_led.value(0) 
            #c.publish(mqtt_root_topic+esp_id,0)

    if "wsled" in topic:
        data = bd(msg)
        if data[0] == 'R':
           ws_r = int(data[1:])
        elif data[0] == 'G':
           ws_g = int(data[1:])
        elif data[0] == 'B':
           ws_b = int(data[1:])

        if data[0] == '#':  
            ws_r = int(int(data[1:3], 16)/2)  
            ws_g = int(int(data[3:5], 16)/2)  
            ws_b = int(int(data[5:7], 16)/2)  
            
        np[0] = (ws_r, ws_g, ws_b)
        np.write()

    if "relay" in topic and isRelay:
        data = bd(msg)   

        if data[0] == 'N':  # oN
            print("R > on")
            rel.value(1)
        elif data[0] == 'F':  # ofF 
            print("R > off")
            rel.value(0) 

    if "pwm/freq" in topic:
        data = bd(msg)
        try:
            value = int(data)
            print("PWM Freq: {0}".format(value))

            fet.freq(value)
        except:
            pass

    if "pwm/duty" in topic:
        data = bd(msg)
        try:
            value = int(data)
            print("PWM Duty: {0}".format(value))

            fet.duty(value)
        except:
            pass

    if "pwmx" in topic and isFET:
        data = bd(msg)   

        if data[0] == '1':
           #pwm = int(data[1:])
            print("led1 - pwm fade in >")
            fade_sw_in(fet,500,5)
            #fet.value(1) 

        if data[0] == '0':
           #pwm = int(data[1:])
            print("led0 - pwm fade out >")
            fade_sw_out(fet,500,5) 
            #fet.value(0)    

    if "8x7seg" in topic:
        data = bd(msg)  
        try:
            d7.write_to_buffer(data)
            d7.display() 
        except:
            print("mqtt.8x7segment.ERR") 
    
    if "8x8mtx/stat" in topic: # show simple 1 or 4 chars
        data = bd(msg)  
        try:
            d8.fill(0)
            d8.text(data, 0, 0, 1)
            d8.show()
        except:
            print("mqtt.8x8matrix/stat.ERR")   

    if "8x8mtx/scroll" in topic: # show simple 1 or 4 chars
        data = bd(msg)  
        try:
            scroll(data,5) # .upper()
        except:
            print("mqtt.8x8matrix/scroll.ERR")             

    if "oled1" in topic:
        data = bd(msg)
        try:
            displMessage(data,2)
        except:
            print("oled.ERR")

    if "oled2" in topic:
        data = bd(msg)
        try:
            displMessage2(data,2)
        except:
            print("oled.ERR")

    if "servo/" in topic and isServo:
        data = bd(msg)
        try:
            servo = str(topic).split('servo/')[1]
            print("Setting servo {0} to value {1}".format(servo, data))

            if servo == "1'":
                pwm1.duty(int(data))
            if servo == "2'":
                pwm2.duty(int(data))
            if servo == "3'":
                pwm3.duty(int(data))

        except Exception as e:
            print("Servo error")
            print(e)

def handleAD():
    global ad_oldval, ad1_oldval, ad2_oldval
    if isAD:
        aval = get_adc_value(adc)
        if abs(ad_oldval-aval) > ADC_HYSTERESIS:
            ad_oldval = aval
            print("ADC: " + str(aval))
            c.publish("octopus/{0}/adc/{1}".format(esp_id, pin_analog), str(aval))

    if isAD1:
        aval = get_adc_value(adc1)
        if abs(ad1_oldval-aval) > ADC_HYSTERESIS/5: # 50/5=10 for light
            ad1_oldval = aval 
            """
            if   isOLED: # test light sensor
                valmap = map(aval, 0, 4050, 0, 126)
                displBarSlimH(oled, valmap, 11)
            """
            print("ADC1: " + str(aval))
            c.publish("octopus/{0}/adc/{1}".format(esp_id, pin_analog_1), str(aval))
   
    
    if isAD2:
        aval = get_adc_value(adc2)
        if abs(ad2_oldval-aval) > ADC_HYSTERESIS:
            ad2_oldval = aval
            print("ADC2: " + str(aval))
            c.publish("octopus/{0}/adc/{1}".format(esp_id, pin_analog_2), str(aval))

def handleConnectionScripts():
    global ad_oldval, ad1_oldval, ad2_oldval
    if cm_Light2M8brightness:        
        if isAD1 and isLed8:
            aval = get_adc_value(adc1)
            if abs(ad1_oldval-aval) > ADC_HYSTERESIS/5: 
                ad1_oldval = aval
                valmap = map(aval, 5, 600, 2, 15)
                if valmap > 15: valmap = 15          
                d8.brightness(valmap)
                if cm_Light2M8: 
                    d8.fill(0)
                    d8.text(str(aval), 0, 0, 1)
                d8.show()       

    """
    if cm_Light2M8: 
        if isAD1 and isLed8:
            aval = get_adc_value(adc1)
            if abs(ad1_oldval-aval) > ADC_HYSTERESIS:
                ad_oldval = aval            
                d8.fill(0)
                d8.text(str(aval), 0, 0, 1)
                d8.show()
    """                        


# --- init and simple testing ---
printLog(3,"init i/o - config >")
loadConfig()

if isWS:
    print("WS RGB LED test >")
    np[0] = (128, 0, 0) #R
    np.write()
    simple_blink() # pause
    sleep(1)

    np[0] = (0,128, 0) #G
    np.write()
    simple_blink()
    sleep(1)

    np[0] = (0, 0, 128) #B
    np.write()
    simple_blink()
    sleep(1)

    np[0] = (0, 0, 0)
    np.write()

ts = []
if isTemp:
    print("dallas temp >")
    try:
        ds = DS18X20(OneWire(dspin))
        ts = ds.scan()

        if len(ts) <= 0:
            isTemp = False

        for t in ts:
            print(" --{0}".format(bytearrayToHexString(t)))
    except:
        isTemp = False
    print("Found {0} dallas sensors, temp active: {1}".format(len(ts), isTemp))

if isLed7:
    from lib.max7219_8digit import Display
    # spi
    try:
        #spi.deinit()
        #print("spi > close")
        spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
        ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
        d7 = Display(spi, ss)
    except:
        print("spi.D7.ERR")

if isLed8:
    from lib.max7219_8digit import Display
    # spi
    if True: #try:
        #spi.deinit()
        spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
        ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)

        from lib.max7219 import Matrix8x8
        d8 = Matrix8x8(spi, ss, 4) #1/4
        #print("SPI device already in use") 
        d8.brightness(15)
        d8.fill(0)
        d8.text('1234', 0, 0, 1)
        d8.show()
    """except:
        print("spi.D8.ERR")  
    """          

if not 0x27 in i2c.scan():
    print("I2C LCD display not found!")
    isLCD = False
    #raise Exception("No device")

if isLCD:
    from lib.esp8266_i2c_lcd import I2cLcd
    lcd = I2cLcd(i2c, LCD_ADDRESS, LCD_ROWS, LCD_COLS)

# serial displ
if isSD:
    from machine import UART
    uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
    uart.write('C')      #test quick clear display  

if isOLED:
    oled_intit()
    oled.text('MQTT-SLAVE test', 5, 3)
    # oled.text(get_hhmm(), 45,29) #time HH:MM
    oled.hline(0,50,128,1)
    oled.text("octopusLAB 2019",5,OLED_ydown) 
    oled.show()    
            
if isLed7:
    print("Testing 7seg")
    test7seg() 

printLog(4,"wifi and mqtt >")    

print("wifi_config >")
wifi_config = read_wifi_config()
wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else 250 )
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
print("wifi.connect  to " + wifi_config["wifi_ssid"])
wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])

# url config: TODO > extern.

print("mqtt_config >")
mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]
#mqtt_ssl  = False # Consider to use TLS!
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]

mqtt_clientid = mqtt_clientid_prefix + esp_id
c = MQTTClient(mqtt_clientid, mqtt_host, ssl=mqtt_ssl)
c.set_callback(mqtt_sub)
print("mqtt.connect to " + mqtt_host)
c.connect()
# c.subscribe("/octopus/device/{0}/#".format(esp_id))

subStr = mqtt_root_topic+"/"+esp_id+"/#"
print("subscribe (root topic + esp id):" + subStr)
c.subscribe(subStr)

print("mqtt log")
# mqtt_root_topic_temp = "octopus/device"
c.publish(mqtt_root_topic,esp_id) # topic, message (value) to publish

print("test temp: " + str(getTemp()))

"""
timeSetup()
if isOLED:
    oled.text(get_hhmm(), 45,29) #time HH:   
    oled.show() 
if isLed7:
    d7.write_to_buffer(get_hhmm())
    d7.display() 
"""

timerInit()
print(get_hhmm(rtc))

printLog(5,"start - main loop >")

while True:

    c.check_msg()

    handleAD()

    handleConnectionScripts() # testing

    

