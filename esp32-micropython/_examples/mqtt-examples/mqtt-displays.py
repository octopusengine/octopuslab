# basic example: octopusLAB - ESP32 - WiFi - MQTT
"""
import upip
upip.install('micropython-umqtt.robust')

install into lib esp8266_i2c_lcd and lcd_api
https://github.com/dhylands/python_lcd
"""
print("mqtt-lcd1602.py > mqtt 'hello world' - ho + ssl/led/ws")

from time import sleep
from machine import Pin, SPI
import machine, time
from util.wifi_connect import read_wifi_config, WiFiConnect
from util.mqtt_connect import read_mqtt_config
from umqtt.simple import MQTTClient
import ubinascii
from neopixel import NeoPixel
from util.pinout import set_pinout
pinout = set_pinout()

pin_led = Pin(pinout.BUILT_IN_LED, Pin.OUT)
pin_ws = Pin(pinout.WS_LED_PIN, Pin.OUT)
fet = Pin(pinout.MFET_PIN, Pin.OUT)
rel = Pin(pinout.RELAY_PIN, Pin.OUT)

isLed7 = True  # SPI
isOLED = False # I2C
isLCD = False  # I2C
isSD = False   # UART

print("setup displays: >")

# SPI max 8x7 segment
try:
    #spi.deinit()
    #print("spi > close")
    spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
    ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
except:
    print("SPI.Err")

if isLed7:
    from lib.max7219_8digit import Display
    d7 = Display(spi, ss)
    d7.write_to_buffer('octopus')
    d7.display()
    
LCD_ADDRESS=0x27
LCD_ROWS=2
LCD_COLS=16

# Set up I2C
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN), freq=100000) # 100kHz because PCF is slow

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

esp_id = ubinascii.hexlify(machine.unique_id()).decode()
print(esp_id)

np = NeoPixel(pin_ws, 1)
ws_r = 0
ws_g = 0
ws_b = 0
bd = bytes.decode

mqtt_clientid_prefix = "CHANGE PREFIX"
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_ssl  = read_mqtt_config()["mqtt_ssl"]

def simple_blink():
    pin_led.value(1)
    sleep(0.25)
    pin_led.value(0)
    sleep(0.25)

def simple_blink_wifilcd():
    if isLCD:
        lcd.move_to(15, 0)
        lcd.putchar("W")
        sleep(0.5)
        lcd.move_to(15, 0)
        lcd.putchar(" ")
        sleep(0.5)

# Define function callback for connecting event
def connected_callback(sta):
    simple_blink()
    print(sta.ifconfig())
    if isLCD:
        lcd.move_to(15, 0)
        lcd.putchar("W")

def connecting_callback(retries):
    simple_blink()
    simple_blink_wifilcd()

def sdStart():
    uart.write('C')      #test quick clear display
    uart.write('W7')   #change color
    uart.write('h30')  #horizontal line
    uart.write('h230') #horizontal line
    uart.write('R0')
    uart.write('W2')   #color
    uart.write('QoctopusLAB - MQTT client*')
    time.sleep_ms(100)
    uart.write('R2')
    uart.write('W1')   #color
    uart.write('QESP32*')
    time.sleep_ms(100)

def sd_write(sdRow, sdWri): #serial display
    time.sleep_ms(100)
    uart.write('R'+str(sdRow))
    uart.write('W1Q')   #color
    uart.write(str(sdWri))
    uart.write('*')

def sd_write_small(sdRow, sdWri): #serial display
    time.sleep_ms(100)
    uart.write('R'+str(sdRow))
    uart.write('W1q')   #color
    uart.write(str(sdWri))
    uart.write('*')

          
def mqtt_sub(topic, msg):
    global ws_r
    global ws_g
    global ws_b

    print("MQTT Topic {0}: {1}".format(topic, msg))
    """
    if isSD:
        data = bd(topic)
        sd_write_small(9,topic)
        data = bd(msg)
        sd_write(8,data) 
    """

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

    if "led8x7/rawtext" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        if isLed7:
            d7.write_to_buffer(data)
            d7.display()   
    
    if "lcd/clear" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        if isLCD:
            lcd.clear()

    if "lcd/rawtext" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        if isLCD:
            lcd.clear()
            lcd.putstr(data)

    if "lcd/line1text" in topic:
        data = bd(msg)
        print("line 1 text: {0}".format(data))
        if isLCD:
            lcd.move_to(0, 0)
            lcd.putstr(data[:LCD_COLS])

    if "lcd/line2text" in topic:
        data = bd(msg)
        print("line 2 text: {0}".format(data))
        if isLCD:
            lcd.move_to(0, 1)
            lcd.putstr(data[:LCD_COLS])

    if "lcd/write" in topic:
        data = bd(msg)
        print("text: {0}".format(data))
        if isLCD:
             lcd.putstr(data)

    if "lcd/set_cursor" in topic:
        data = bd(msg)
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

    if "sd/clear" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        lcd.clear()

    if "sd/rawtext" in topic:
        data = bd(msg)
        print("raw test: {0}".format(data))
        sd_write(5,data)          

print("display-LCD >")
if isLCD:
    lcd.clear()
    lcd.putstr("MQTT LCD")
    lcd.move_to(0, 1)
    lcd.putstr("ID:{0}".format(esp_id))


print("display-SD >")
if isSD: 
    sdStart()
    sd_write(3,"ID:{0}".format(esp_id))

print("wifi_config >")
wifi_config = read_wifi_config()
wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else 250 )
wifi.events_add_connecting(connecting_callback)
wifi.events_add_connected(connected_callback)
wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])

print("mqtt_config >")
mqtt_clientid_prefix = read_mqtt_config()["mqtt_clientid_prefix"]
mqtt_host = read_mqtt_config()["mqtt_broker_ip"]
mqtt_root_topic = read_mqtt_config()["mqtt_root_topic"]

mqtt_clientid = mqtt_clientid_prefix + esp_id

c = MQTTClient(mqtt_clientid, mqtt_host, ssl=mqtt_ssl)
c.set_callback(mqtt_sub)

if isLCD:
     lcd.move_to(14, 0)

try:
    if c.connect() == 0:
        subStr = mqtt_root_topic+esp_id+"/#"
        c.subscribe(subStr)

        print("mqtt log")
        c.publish(mqtt_root_topic,esp_id) # topic, message (value) to publish

        simple_blink()
        if isLCD:
           lcd.putchar("M")
        if isSD:
           sd_write(9,"M")   

    else:
        if isLCD:
           lcd.putchar("E")
except Exception as e:
    print("Error connecting to MQTT")
    if isLCD:
        lcd.putchar("E")

print("> loop:")
while True:
    c.check_msg()