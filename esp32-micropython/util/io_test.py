# # --- init and simple testing ---
# printLog(3,"init i/o - config >")
# printFree()
# loadConfig()
# printConfig()
# printFree()

from machine import Pin
from time import sleep, sleep_ms
from util.octopus import *
from util.pinout import set_pinout
pinout = set_pinout()

from util.io_config import get_from_file
io_conf = get_from_file()

def test_led():
    if io_conf.get('led'):
        printHead("led")
        print("LED init  >")
        led = Pin(pinout.BUILT_IN_LED, Pin.OUT)

        print("LED test >")
        led.value(1)
        sleep(1)
        led.value(0)
        
def test_ws():
    if io_conf.get('ws'):
        printHead("ws")
        print("WS RGB LED init neopixel >")
        np = rgb_init(io_conf['ws'] if 'ws' in io_conf else 0)

        print("WS RGB LED test >")
        RGBtest(1000)

def test_piezzo():
    if io_conf.get('piezzo'):
        beep()            

#ts = []
def test_temp():
    temp_init()  

def test_butt():
    if io_conf.get("button"):
        printHead("button")
        # Button settings
        BTN_Debounce   = 20
        BTN_Tresh      = 10
        BTN_Delay      = 250
        BTN_LastPress  = 0
        BTN_PressCount = 0
        print("Initializing single Button, delay {0}".format(BTN_Delay))
        try:
            btn = Pin(pinout.DEV2_PIN, Pin.IN, Pin.PULL_UP)
            #btn.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handleButton)
        except:
            print("btn.Err")    

def test_led7(): 
    if io_conf.get('led7'): 
        printHead("led7")      
        d = disp7_init()

# if isLed8:
#     from lib.max7219_8digit import Display
#     # spi
#     if True: #try:
#         #spi.deinit()
#         spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
#         ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
#
#         from lib.max7219 import Matrix8x8
#         d8 = Matrix8x8(spi, ss, 4) #1/4
#         #print("SPI device already in use")
#         d8.brightness(15)
#         d8.fill(0)
#         d8.text('1234', 0, 0, 1)
#         d8.show()
#     """except:
#         print("spi.D8.ERR")
#     """
# if isTft:
#     print("spi.TFT 128x160 init >")
#     printFree()
#     from lib import st7735
#     from lib.rgb import color565
#     spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
#     ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
#
#     cs = Pin(5, Pin.OUT)
#     dc = Pin(16, Pin.OUT)
#     rst = Pin(17, Pin.OUT)
#     tft = st7735.ST7735R(spi, cs = cs, dc = dc, rst = rst)
#
#     print("spi.TFT framebufer >")
#     printFree()
#     import framebuf
#     # Initialize FrameBuffer of TFT's size
#     fb = framebuf.FrameBuffer(bytearray(tft.width*tft.height*2), tft.width, tft.height, framebuf.RGB565)
#     fbp = fb.pixel
#
#     fb.fill(color565(255,0,0))
#     tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
#     sleep(1)
#
#     fb.fill(color565(0,255,0))
#     tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
#     sleep(1)
#
#     fb.fill(color565(0,0,255))
#     tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
#     sleep(1)
#
#     # reset display
#     fb.fill(0)
#     tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
#
#     sleep(1)
#
#     for i in range(0,3):
#         fb.fill(0)
#         fb.text('OctopusLab', 20, 15, color565(255,255,255))
#         fb.text(" --- "+str(3-i)+" ---", 20, 55, color565(255,255,255))
#         tft.blit_buffer(fb, 0, 0, tft.width, tft.height)
#         sleep(0.5)
#
# if isServo:
#     pwm1 = PWM(Pin(pinout.PWM1_PIN), freq=50, duty=70)
#     pwm2 = PWM(Pin(pinout.PWM2_PIN), freq=50, duty=70)
#     pwm3 = PWM(Pin(pinout.PWM3_PIN), freq=50, duty=70)
#
# if isStepper:
#         print("test stepper")
#         from lib.sm28byj48 import SM28BYJ48
#         #PCF address = 35 #33-0x21/35-0x23
#         ADDRESS = 0x23
#         # motor id 1 or 2
#         MOTOR_ID1 = 1
#         #MOTOR_ID2 = 2
#
#         i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
#         i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)
#
#         i2c = machine.I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
#         motor1 = SM28BYJ48(i2c, ADDRESS, MOTOR_ID1)
#
#         # turn right 90 deg
#         motor1.turn_degree(90)
#         # turn left 90 deg
#         motor1.turn_degree(90, 1)
#
# # only for IoT board
# if isFET:
#     fet = PWM(Pin(pinout.MFET_PIN, Pin.OUT))
#     fet.duty(0)
#     fet.freq(2000)
#
# if isRelay:
#     rel = Pin(pinout.RELAY_PIN, Pin.OUT)
#
# # serial displ
# if isSD:
#     from machine import UART
#     uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
#     uart.write('C')      #test quick clear display
#
# # i2c devices:
# detect_i2c_dev()
#
# if not 0x27 in i2c.scan():
#     print("I2C LCD display not found!")
#     isLCD = False
#     #raise Exception("No device")
#
# if isLCD:
#     from lib.esp8266_i2c_lcd import I2cLcd
#     lcd = I2cLcd(i2c, LCD_ADDRESS, LCD_ROWS, LCD_COLS)
#     lcd.clear()
#     lcd.putstr("octopusLAB")
#
# if isOLED:
#     oled_intit()
#     oled.text('MQTT-SLAVE test', 5, 3)
#     # oled.text(get_hhmm(), 45,29) #time HH:MM
#     oled.hline(0,50,128,1)
#     oled.text("octopusLAB 2019",5,OLED_ydown)
#     oled.show()
#
# if isLed7:
#     print("Testing 7seg")
#     test7seg()
#
# if isKeypad:
#     print("I2C epander Keypad 4x4")
#     if not KP_ADDRESS in i2c.scan():
#         print("I2C Keypad not found!")
#         isKeypad = False
#     else:
#         from lib.KeyPad_I2C import keypad
#         kp = keypad(i2c, KP_ADDRESS)
#

def all():
    test_led()
    test_ws()
    test_piezzo()
    #test_temp()
    #test_butt()
    test_led7()   
