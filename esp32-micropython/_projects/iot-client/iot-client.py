"""
octopusLAB ESP32 easy - MQTT client manager and/or influx db
need ROBOTboard or IoTboard (it depends on the project)
limit: 1000 lines ;)
> Inputs:
Button, keyboard, analog Joystick
Sensors: A/D, One wire temperature, I2C light, ...
> Outputs:
Relay, MOS-FER PWM (IoT board), Servo, DC motor, stepper (Robot board)
> Displays:
I2C OLED, I2C LCD, SPI 8x7 segment, SPI 4x 8x8 matrix, UART Nextion, UART Serial display, SPI TTF
2019 | Octopus engine s.r.o.
"""
import machine, time, ubinascii, json
from time import sleep, ticks_ms, sleep_ms, sleep_us
from machine import Pin, Timer, PWM, SPI
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config
from util.octopus_lib import *
from util.pinout import set_pinout
import urequests
pinout = set_pinout()

from util.Setup import mainOctopus as printOctopus
printOctopus()
printLog(1,"boot device >")
print("iot-client.py > ESP32")
ver = "0.55 / 8.7.2019" #984

# hard-code config / daefault
Debug = True        # TODO: debugPrint()?        
timeInterval = 10    # 1/10 for data send
wifi_retries = 100  # for wifi connecting

name = ""       # device name/describe
isTimer = 0      # config
isTime = 0       # setup time from cloud
isMqtt = False   # hardcode
isInflux = False # influx and grafana db
influxWriteURL = "" # from i/o config
isMySQl = False

# simple orchestrator connection manager / hard wire matrix
menuVal = 0
menuValOld = -1
cm_RunMenu = 1
cm_Light2M8 = 0
cm_Light2M8brightness = 0
cm_Keypad2Lcd = 0
cm_Time2Tft = 0
cm_Temp2Tft = 0
cm_DisplayTemp = 1
cm_DisplayTime = 0
cm_SimpleBlinkTimer = 0

# Button settings
BTN_Debounce   = 10 # ms
BTN_Tresh      = 10
BTN_Delay      = 250
BTN_LastPress  = 0
BTN_PressCount = 0

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

rtc = machine.RTC() # real time
tim1 = Timer(0)     # for main 10 sec timer

print("ver: " + ver + " (c)octopusLAB")
esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print("id: " + esp_id)
printFree()

printLog(2,"init - variables and functions >")
bd = bytes.decode

from util.io_config import io_conf_file, io_menu_layout, get_from_file as get_io_config_from_file
io_conf = get_io_config_from_file()
print('        I / O    (interfaces)')
print('=' * 30)
# show options with current values

for i in io_menu_layout:
    print("%8s [%s] - %s" % (i['attr'], io_conf.get(i['attr'], 0), i['descr']))

# Inputs - sensors
isTemp = io_conf.get('temp')
isLight = io_conf.get('light')
isMoist = io_conf.get('moist')
isAD = io_conf.get('ad0')  # A/D input voltage
isAD1 = io_conf.get('ad1') # A/D x / photoresistor
isAD2 = io_conf.get('ad2') # A/D y / thermistor
isKeypad = io_conf.get('keypad') # Robot I2C+expander 4x4 keypad
isButton = io_conf.get('button') # DEV2 Button
isIR = io_conf.get('ir') # DEV2 IR rec.
# Outpusts
isRelay = io_conf.get('relay') # Have Relay
isStepper = io_conf.get('stepper')  
isServo = io_conf.get('servo') # Have PWM pins (both Robot and IoT have by default)
isFet = io_conf.get('fet') # have mos-FET
# Displays / LED
isLed = io_conf.get('led')
isWS = io_conf.get('ws') #  WS RGB LED 0/1/8/...n
isOLED = io_conf.get('oled') ##  I2C
isLCD = io_conf.get('lcd')   ##* I2C
isLed7 = io_conf.get('led7') #  SPI max 8x7 segm.display
isLed8 = io_conf.get('led8') #  SPI max 8x8 matrix display
isTft = io_conf.get('tft') # 128x160      
isSD = 0        #* UART

print('        M Q T T  (config)')
print('=' * 30)
mq_config = {}
configFileMq = 'config/mqtt_io.json'
try:
    with open(configFileMq, 'r') as f:
        d = f.read()
        f.close()
        mq_config = json.loads(d)

    name = mq_config.get('name')
    isTime = mq_config.get('time')    
    isMqtt = mq_config.get('mqtt')
    isInflux = mq_config.get('influx')
    influxWriteURL = mq_config.get('influxWriteURL')
    influxTable = mq_config.get('influxTable')
    isMySQl = mq_config.get('mysql')
    isTimer = mq_config.get('timer')

except:
    print("Data Err. or '"+ configFileMq + "' does not exist")

print("hostName " + str(name))
print("isTime: " + str(isTime))
print("isMqtt: " + str(isMqtt))
print("isInflux: " + str(isInflux))
print("isMySQl: " + str(isMySQl))
print("isTimer: " + str(isTimer))
print()

# Set up I2C
print("init i2c >")
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
# 100kHz because PCF is slow
printFree()

#
LCD_ADDRESS=0x27
LCD_ROWS=2
LCD_COLS=16

#OLED size and position
OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7

# Keyboard settings timer
KP_ADDRESS=0x23
KP_Delay = 250
KP_LastPress = 0

# Detect I2C bus
def detect_i2c_dev():
    global isOLED, bhLight, bh2Light, tslLight, isLCD
    print("detect i2c devices >")
    printFree()
    if Debug: print(" - scanning")
    i2cdevs = i2c.scan()
    if Debug: print(" - devices: {0}".format(i2cdevs))

    # Determine what we have connected to I2C
    isOLED = (0x3c in i2cdevs) and isOLED      # If there is OLED, but config disabled it
    bhLight = 0x23 in i2cdevs
    bh2Light = 0x5c in i2cdevs
    tslLight = 0x39 in i2cdevs
    isLCD = (LCD_ADDRESS in i2cdevs) and isLCD # =

oled = None
def oled_intit():
    print("OLED present: {0}".format(isOLED))
    global oled
    from lib import ssd1306
    sleep(1)
    oled = ssd1306.SSD1306_I2C(OLEDX, OLEDY, i2c)

def displMessage2(mess,timm): 
    try:
        oled.fill_rect(0,OLED_ydown,OLEDX,10,0)
        oled.text(mess, OLED_x0, OLED_ydown)
        oled.show()
        sleep_ms(timm*1000)
    except Exception as e:
       print("Err. displMessage2() Exception: {0}".format(e))

def displMessage1(mess,timm):
    try:
        oled.fill_rect(0,OLED_ydown-17,OLEDX,10,0)
        oled.text(mess, OLED_x0, OLED_ydown-17)
        oled.show()
        sleep_ms(timm*1000)
    except Exception as e:
       print("Err. displMessage1() Exception: {0}".format(e))

def displMessage(mess,timm):
    try:
        if isOLED:
            oled.fill_rect(0,OLED_ydown-17,OLEDX,10,0)
            oled.text(str(mess), OLED_x0, OLED_ydown-17)
            oled.show()
        if isLed7:
            d7.write_to_buffer(str(mess))
            d7.display()
        if isLCD:
            lcd.move_to(0, 0)
            lcd.putstr(str(mess))    

        sleep(timm)

    except Exception as e:
        print("Err. displMessage() Exception: {0}".format(e))

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
    tw=0
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
    urlApi ="http://www.octopusengine.org/api/hydrop"
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
          sleep_us((r-i)*m*2) # multH/L *2
          p.value(1)
          sleep_us(i*m)

def fade_sw_out(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(1)
          sleep_us((r-i)*m)
          p.value(0)
          sleep_us(i*m*2)

def test7seg():
     d7.write_to_buffer('octopus')
     d7.display()

def sendData():
    print("sendData() timer >")
    temp = 0
    if isTemp:
        temp = getTemp()
        print("temp: " + str(temp/10))
        
    if isMqtt:
        publishTopic = "octopus/{0}/temp/{1}".format(esp_id,temp)
        print(str("publishTopic: " + publishTopic))
        c.publish("/octopus/device/{0}/temp/".format(esp_id),str(temp/10))

    if isInflux:
        print("send influx data >")
        influx_fields["temp"] = temp/10
        postdata_fields = ','.join(["%s=%s" % (k, v) for (k, v) in influx_fields.items()])
        postdata_influx = "{0}{1} {2}".format(influxTable+",", postdata_tags, postdata_fields)
        #postdata_influx = "hohome,place="+name+",device="+esp_id+" temp="+str(temp/10)
        print(postdata_influx)
        res = urequests.post(influxWriteURL, data=postdata_influx) 
        res.close()
     
itt = 0 # every 10 sec. / itteration timer
def timerSend():
    global itt
    itt = itt + 1
    if Debug: print("timer > "+str(itt))
    if cm_SimpleBlinkTimer: simple_blink()    

    if isOLED:
        displMessage2(str(itt) + " | " + str(get_hhmm(rtc)),1)

    if (itt == 6*timeInterval): # 6 = 1min / 60 = 10min
        if Debug: print(str(itt) + " | " + str(timeInterval) + " min. > send data:")
        itt = 0
        sendData() # read sensors and send data
        printFree()
       
# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    print(sta.ifconfig())

def connecting_callback(retries):
    simple_blink()

# ----------------------------------
def mqtt_sub(topic, msg):
    data = bd(msg)
    global ws_r, ws_g, ws_b

    print("MQTT Topic {0}: {1}".format(topic, msg))
    if "led" in topic:
        print("led:")
        
        if data[0] == 'N':  # oN
            print("-> on")
            pin_led.value(1)
            #c.publish(mqtt_root_topic+esp_id,1)

        elif data[0] == 'F':  # ofF
            print("-> off")
            pin_led.value(0)
            #c.publish(mqtt_root_topic+esp_id,0)

    if "wsled" in topic:
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

    if "wsled/rainbow" in topic:
        rainbow_cycle(np, isWS,2)  # Increase to slow down
        time.sleep(1)

    if "wsled/off" in topic:
        np.fill(BLACK)
        np.write()            

    if "relay" in topic and isRelay:
        print("relay")
        if data[0] == 'N':  # oN
            print("R > on")
            rel.value(1)
        elif data[0] == 'F':  # ofF
            print("R > off")
            rel.value(0)

    if "pwm/freq" in topic:
        try:
            value = int(data)
            print("PWM Freq: {0}".format(value))

            fet.freq(value)
        except:
            pass

    if "pwm/duty" in topic:
        try:
            value = int(data)
            print("PWM Duty: {0}".format(value))

            fet.duty(value)
        except:
            pass

    if "pwmx" in topic and isFET:
        if data[0] == '1':
           #pwm = int(data[1:])
            print("led1 - pwm fade in >")
            fade_sw_in(fet,500,5)

        if data[0] == '0':
           #pwm = int(data[1:])
            print("led0 - pwm fade out >")
            fade_sw_out(fet,500,5)

    if "lcd/clear" in topic:
        print("raw test: {0}".format(data))
        if isLCD:
            lcd.clear()

    if "lcd/rawtext" in topic:
        print("raw test: {0}".format(data))
        if isLCD:
            lcd.clear()
            lcd.putstr(data)

    if "lcd/line1text" in topic:
        print("line 1 text: {0}".format(data))
        if isLCD:
            lcd.move_to(0, 0)
            lcd.putstr(data[:LCD_COLS])

    if "lcd/line2text" in topic:
        print("line 2 text: {0}".format(data))
        if isLCD:
            lcd.move_to(0, 1)
            lcd.putstr(data[:LCD_COLS])

    if "lcd/line3text" in topic:
        print("line 3 text: {0}".format(data))
        if isLCD:
            lcd.move_to(0, 2)
            lcd.putstr(data[:LCD_COLS])

    if "lcd/line4text" in topic:
        print("line 4 text: {0}".format(data))
        if isLCD:
            lcd.move_to(0, 3)
            lcd.putstr(data[:LCD_COLS])

    if "lcd/write" in topic:
        print("text: {0}".format(data))
        if isLCD:
             lcd.putstr(data)

    if "lcd/set_cursor" in topic:
        x=0
        y=0
        print("Cursor set: {0}".format(data))
        try:
            if "x" in data:
                x = int(data.split('x')[0])
                y = int(data.split('x')[1])
            else:
                y = int(data)

            lcd.move_to(x, y)

        except Exception as e:
            print("Error parse message")
            print(e)        

    if "8x7seg" in topic:
        try:
            d7.write_to_buffer(data)
            d7.display()
        except:
            print("mqtt.8x7segment.ERR")

    if "8x8mtx/stat" in topic: # show simple 1 or 4 chars
        try:
            d8.fill(0)
            d8.text(data, 0, 0, 1)
            d8.show()
        except:
            print("mqtt.8x8matrix/stat.ERR")

    if "8x8mtx/scroll" in topic: #
        try:
            scroll(data,5) # .upper()
        except:
            print("mqtt.8x8matrix/scroll.ERR")

    if "oled1" in topic:
        try:
            displMessage1(data,2)
        except:
            print("oled.ERR")

    if "oled2" in topic:
        try:
            displMessage2(data,2)
        except:
            print("oled.ERR")

    if "servo/" in topic and isServo:
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

it = 0
def handleHardWireScripts(): # matrix of connections examples
    global ad_oldval, ad1_oldval, ad2_oldval, it, menuValOld
    it = it + 1 
    if cm_RunMenu:
        if (menuVal != menuValOld): # run olny once
            print("menu: " + str(menuVal))
            np[0] = (BLACK)
            np.write()
            if isMqtt:
                publishTopic = mqtt_root_topic + "/{0}/menu/".format(esp_id) 
                c.publish(publishTopic,str(menuVal))

            if (menuVal == 1):
                np[0] = (RED)
                np.write()
                displMessage(get_hh_mm(rtc),3) # hh:mm > hh-mm for 7seg 
            
            if (menuVal == 2):
                np[0] = (GREEN)
                np.write()
                displMessage(esp_id,3)

            if (menuVal == 3):
                np[0] = (BLUE)
                np.write()
                displMessage("octopus",3)
            
            menuValOld = menuVal 
            sleep(2)    

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
    
    if cm_DisplayTemp:
        if isLed7 and isTemp:
            try:
                tt = getTemp()/10
                d7.write_to_buffer(str(tt) + "c ")
                d7.display()
            except:
                print("mqtt.8x7segment.ERR")

    if isTft:
        try:
            fb.fill(0)
            fb.text('OctopusLab', 20, 15, color565(0,0,255))
            fb.hline(3, 27, 122, color565(0,0,255)) # xyw
            fb.text('MQTT test', 3, 39, color565(255,255,255))
        except:
            print("err.tft")              

    if cm_Time2Tft:
        if isTft:
            hhmm = get_hhmm(rtc)
            #print(hhmm)
            try:
                fb.text(hhmm, 86, 148, color565(255,255,255))
                fb.text(str(itt), 10, 148, color565(0,0,255))
                sleep(0.5)
            except:
                print("err.cm_Time2Tft()")    

    if cm_Temp2Tft: 
            tt = getTemp()/10  
            fb.text(str(tt), 86, 133, color565(0,255,0)) 
            #fb.pixel(it,int(tt),color565(255,255,255)) 
            print(str(tt))   
            sleep(2)

    if isTft:
        try:
            tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
            sleep(2)
        except:
            print("err.tft")                    

def handleKeyPad():
    global KP_LastPress
    try:
        key = kp.getKey()
    except OSError as e:
        print(e)

    if key and ticks_ms() > KP_LastPress + KP_Delay:
        KP_LastPress = ticks_ms()
        print(key)
        if cm_Keypad2Lcd:
            if isLCD:
                lcd.move_to(0, 2)
                lcd.putstr(key)

        c.publish("octopus/{0}/keypad/key".format(esp_id), key)

def handleIR():
    global menuVal
    # print(".", end = ' ') 
    f = read_id(pinout.DEV2_PIN)
    if len(f)>0 : 
        key = f[3]
        print("key: " + key)
        try:
            menuVal = int(key)
        except:
            print("e")    

BTN_LastState = False
def handleButton(pin):
    global BTN_LastPress, BTN_PressCount, BTN_LastState, menuVal

    if ticks_ms() > BTN_LastPress + BTN_Delay:
        BTN_LastPress = ticks_ms()

        debounce = 0
        for i in range(BTN_Debounce):
            debounce += pin.value()
            sleep_ms(1)

        #print("Handling button, debounce value: {0}".format(debounce))

        if debounce < BTN_Tresh:
            if not BTN_LastState:
                #print(pin)
                BTN_PressCount += 1
                BTN_LastState = True
                menuVal = menuVal + 1
                if menuVal > 3: menuVal = 0
                c.publish("octopus/{0}/button".format(esp_id), str(BTN_PressCount))
        else:
            BTN_LastState = False 

if isWS:
    print("WS RGB LED init neopixel >")
    from util.ws_rgb import *
    pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
    np = setupNeopixel(pin_ws, isWS)
    
    # num_pixels = 12
    ws_r = 0
    ws_g = 0
    ws_b = 0
    print("WS RGB LED test >")
    
    simpleRgb(np) 

if isWS > 1:
    neopixelTest(np, isWS)        

ts = []
if isTemp:
    print("dallas temp init >")
    from onewire import OneWire
    from ds18x20 import DS18X20
    dspin = machine.Pin(pinout.ONE_WIRE_PIN)
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

isLed7 = io_conf.get('led7')
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

isLed8 = io_conf.get('led8')
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

if isTft:
    print("spi.TFT 128x160 init >")
    printFree()
    from lib import st7735
    from lib.rgb import color565
    spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
    ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)

    cs = Pin(5, Pin.OUT)
    dc = Pin(16, Pin.OUT)
    rst = Pin(17, Pin.OUT)
    tft = st7735.ST7735R(spi, cs = cs, dc = dc, rst = rst)

    print("spi.TFT framebufer >")
    printFree()
    import framebuf
    # Initialize FrameBuffer of TFT's size
    fb = framebuf.FrameBuffer(bytearray(tft.width*tft.height*2), tft.width, tft.height, framebuf.RGB565)
    fbp = fb.pixel

    fb.fill(color565(255,0,0))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
    sleep(1)

    fb.fill(color565(0,255,0))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
    sleep(1)

    fb.fill(color565(0,0,255))
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
    sleep(1)

    # reset display
    fb.fill(0)
    tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
    sleep(1)    

    for i in range(0,3):
        fb.fill(0)
        fb.text('OctopusLab', 20, 15, color565(255,255,255))
        fb.text(" --- "+str(3-i)+" ---", 20, 55, color565(255,255,255))
        tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
        sleep(0.5)

if isServo:
    pwm1 = PWM(Pin(pinout.PWM1_PIN), freq=50, duty=70)
    pwm2 = PWM(Pin(pinout.PWM2_PIN), freq=50, duty=70)
    pwm3 = PWM(Pin(pinout.PWM3_PIN), freq=50, duty=70)

if isStepper:
        print("test stepper")
        from lib.sm28byj48 import SM28BYJ48
        #PCF address = 35 #33-0x21/35-0x23
        ADDRESS = 0x23
        # motor id 1 or 2
        MOTOR_ID1 = 1
        #MOTOR_ID2 = 2
        i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
        i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

        i2c = machine.I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
        motor1 = SM28BYJ48(i2c, ADDRESS, MOTOR_ID1)

        # turn right 90 deg
        motor1.turn_degree(90)
        # turn left 90 deg
        motor1.turn_degree(90, 1)

# only for IoT board
if isFet:
    fet = PWM(Pin(pinout.MFET_PIN, Pin.OUT))
    fet.duty(0)
    fet.freq(2000)

if isRelay:
    rel = Pin(pinout.RELAY_PIN, Pin.OUT)

# serial displ
if io_conf.get('sm'):
    from machine import UART
    uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
    uart.write('C')      #test quick clear display

# i2c devices:
detect_i2c_dev()

if not 0x27 in i2c.scan():
    print("I2C LCD display not found!")
    isLCD = False
    #raise Exception("No device")

if isLCD:
    from lib.esp8266_i2c_lcd import I2cLcd
    lcd = I2cLcd(i2c, LCD_ADDRESS, LCD_ROWS, LCD_COLS)
    lcd.clear()
    lcd.putstr("octopusLAB")

if isOLED:
    oled_intit()
    oled.text('MQTT-SLAVE test', 5, 3)
    # oled.text(get_hhmm(), 45,29) #time HH:MM
    oled.hline(0,50,128,1)
    oled.text("octopusLAB 2019",5,OLED_ydown)
    oled.show()

if io_conf.get('led7'):
    print("Testing 7seg")
    test7seg()

if isKeypad:
    print("I2C epander Keypad 4x4")
    if not KP_ADDRESS in i2c.scan():
        print("I2C Keypad not found!")
        isKeypad = False
    else:
        from lib.KeyPad_I2C import keypad
        kp = keypad(i2c, KP_ADDRESS)    

if isButton:
    print("Initializing Button, delay {0}".format(BTN_Delay))
    btn = Pin(pinout.DEV2_PIN, Pin.IN, Pin.PULL_UP)
    btn.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handleButton) # irq or handle

printLog(4,"wifi and mqtt >")
printFree()

print("wifi_config >")
wifi = WiFiConnect(wifi_retries)
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
print("wifi.connect")
wifi_status = wifi.connect()

if isIR:
    from lib.ir_remote import read_id

if isMqtt:
    from umqtt.simple import MQTTClient
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

if isInflux:
    print("setup Influx db")
    influx_tags   = dict()
    influx_log = dict()
    influx_fields = dict()

    influx_tags["device"] = esp_id
    influx_tags["place"]  = name 
    postdata_tags   = ','.join(["%s=%s" % (k, v) for (k, v) in influx_tags.items()])

    #log
    print("Influx db - log >")
    influx_log["log"] = 1

    postdata_fields = ','.join(["%s=%s" % (k, v) for (k, v) in influx_log.items()])
    postdata_influx = "{0}{1} {2}".format(influxTable+",", postdata_tags, postdata_fields)
    print(postdata_influx)
    try:
        res = urequests.post(influxWriteURL, data=postdata_influx) 
        res.close()   
    except:
        print("Influx or WiFi ERR")     
    printFree()     

printFree()
print("test temp: " + str(getTemp()/10))
# test sendData
sendData()

if isTime: timeSetup()
print(get_hhmm(rtc))

if isTimer: timerInit()

printLog(5,"start - main loop >")
printFree()

while True:
    if isMqtt: c.check_msg()
    if isKeypad: handleKeyPad()
    #if isButton: handleButton(btn) # > irq
    if isIR: handleIR()
    handleAD()
    handleHardWireScripts() # test hw connections