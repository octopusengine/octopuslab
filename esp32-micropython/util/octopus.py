# this module is for Basic simple examples & tests
# it's loaded in boot.py and provides function octopus()
# user is questioned in interactive mode

# esp8266 / wemos / esp32 doit...

# ampy -p /COM4 put util/octopus-8266.py util/octopus.py
ver = "4.12.2018-v0.15"

from micropython import const
import time
import os, uos
import gc #mem_free
import machine, ubinascii
from machine import Pin, PWM, SPI, Timer

from util.buzzer import beep, play_melody
from util.led import blink
from util.pinout import set_pinout
pinout = set_pinout()

# spi
try:
    spi.deinit()
    print("spi > close")
except:
    print()
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)

rtc = machine.RTC() # real time

pwm0 = PWM(Pin(pinout.PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)


"""
timNote = Timer(8, freq=3000)
ch = timNote.channel(2, Timer.PWM, pin=Pin(pinout.PIEZZO_PIN))

tim = Timer(-1)
"""
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

# def simple_beep(p,f,t):  # port,freq,time
#     #pwm0.freq()  # get current frequency
#     p.freq(f)     # set frequency
#     #pwm0.duty()  # get current duty cycle
#     p.duty(512)   # set duty cycle
#     time.sleep_ms(t)
#     p.duty(0)
#     #b.deinit()

# def blink(t): # time sleep
#     led.value(1)
#     time.sleep_ms(t)
#     led.value(0)
#     time.sleep_ms(t)

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:]
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

def add0(sn):
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str

def get_hhmm():
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm

octopuASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   )  \ `)(' / ( ",
]

def mainOctopus():
    for ol in octopuASCII:
        print(str(ol))
    print()

def mainMenu():
    print()
    print(get_hhmm())
    print('-' * 39)
    print("Menu: Basic simple examples & tests")
    print('.' * 30)
    print("SYSTEM & SETTINGS")
    print("[i] - device & system info")
    print("[s] - setup machine and wifi")
    print("[w] - wifi test")
    print("[f] - file info/dir")
    print("[c] - clear terminal")
    print('.' * 30)
    print("EXAMPLES & TESTS")
    print("[b] - built-in led/beep/button")
    print("[r1] - RGB WS led test")
    print("[r8] - 8x RGB WS led test")
    print("[m] - piezzo melody")
    print("[a] - analog input test")
    print("[t] - temperature")
    print("[d] - displays    --- >>>")
    print("[r] - robot Board --- >>>")
    print("[p] - projects    --- >>>")
    #print("[u] * uart test")
    print("[q] - QUIT")
    print('-' * 39)

    sel = input("select: ")
    #print("your select: "+str(sel))
    return sel
    print()

# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    blink(led, 50, 100)
    # np[0] = (0, 128, 0)
    # np.write()
    blink(led, 50, 100)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    # np[0] = (0, 0, 128)
    # np.write()
    blink(led, 50, 100)
#
# def beep(pwm_pin, freq, length, volume=50):
#        pwm_pin.duty(volume)
#        pwm_pin.freq(freq)
#        time.sleep(length/1000)

#servo
SERVO_MIN = 45
SERVO_MAX = 130
def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def set_degree(servo, angle):
    servo.duty(map(angle, 0,150, SERVO_MIN, SERVO_MAX))

#-------------
def octopus():
    ###beep(pwm0,500,100) # start beep
    #tim.init(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print("test timer - thread delay"))
    #tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))
    mainOctopus()
    print("Hello, this is basic octopusLAB example (2018/12)")
    print(" (Press Ctrl+C to abort | CTRL+D to soft reboot)")
    print()

    time.sleep_us(10)       # sleep for 10 microseconds
    blink(led, 500)
    time.sleep_ms(300)     # 1s
    start = time.ticks_ms()

    run= True
    while run:
      sel = mainMenu()
      beep(pwm0, 1000, 50)

      if sel == "a":
          print("analog input test: ")
          pin_an = Pin(pinout.ANALOG_PIN, Pin.IN)
          adc = machine.ADC(pin_an)
          an = adc.read()
          print("RAW: " + str(an))
          # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
          print("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)

      if sel == "b":
           count = 5
           for _ in range(count):
               beep(pwm0, 500, 100)
               blink(led, 500)

      if sel == "c":
          print(chr(27) + "[2J") # clear terminal
          print("\x1b[2J\x1b[H") # cursor up
          mainOctopus()

      if sel == "f":
          print("file info /dir/ls:") #
          print(os.listdir())
          print("> lib: "+str(os.listdir("lib")))
          print("> util: "+str(os.listdir("util")))
          print("> pinouts: "+str(os.listdir("pinouts")))

      if sel == "i":
          print("> unique_id: "+str(get_eui()))
          #print("--- MAC: "+str(mac2eui(get_eui())))
          print("> uPy version: "+str(os.uname()[3]))
          print("> octopus() ver: " + ver)
          try:
                with open('config/device.json', 'r') as f:
                    d = f.read()
                    f.close()
                    print("> config/device: " + d)
                    # device_config = json.loads(d)
          except:
                print("Device config 'config/device.json' does not exist, please run setup()")

          gc.collect()
          print("> mem_free: "+str(gc.mem_free()))
          print("> machine.freq: "+str(machine.freq()))
          print("> active variables:")
          print(dir())
          print("> datetime RAW: "+str(rtc.datetime()))

      if sel == "m":
          time.sleep_ms(500)
          from util.buzzer.melody import mario
          play_melody(pwm0, mario)
          pwm0.duty(0)

      if sel == "r1":
        from neopixel import NeoPixel
        NUMBER_LED = 1
        pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
        np = NeoPixel(pin, NUMBER_LED)

        np[0] = (128, 0, 0) #R
        np.write()
        time.sleep_ms(1000)

        np[0] = (0,128, 0) #G
        np.write()
        time.sleep_ms(1000)

        np[0] = (0, 0, 128) #B
        np.write()
        time.sleep_ms(1000)

        np[0] = (0, 0, 0) #0
        np.write()

      if sel == "r8":
       from neopixel import NeoPixel
       NUMBER_LED = 8
       pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
       np = NeoPixel(pin, NUMBER_LED)

       np[0] = (32, 0, 0) #R
       np[1] = (0,32, 0) #G
       np[2] = (0, 0, 32) #B
       np[5] = (32, 0, 0) #R
       np[6] = (0,32, 0) #G
       np[7] = (0, 0, 32) #B
       np.write()

      if sel == "r80":
         from neopixel import NeoPixel
         NUMBER_LED = 8
         pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
         np = NeoPixel(pin, NUMBER_LED)
         for i in range(NUMBER_LED):
           np[i] = (1, 0, 0)
           time.sleep_ms(1)# REVIEW:
         np.write()

      if sel == "s":
           from util.setup import setup
           setup()

      if sel == "w":
          from util.wifi_connect import read_wifi_config, WiFiConnect
          time.sleep_ms(2000)
          wifi_config = read_wifi_config()
          print("config for: " + wifi_config["wifi_ssid"])
          w = WiFiConnect()
          w.events_add_connecting(connecting_callback)
          w.events_add_connected(connected_callback)
          w.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
          print("WiFi: OK")

      if sel == "q":
          print("machine.reset() and Exit")
          time.sleep_ms(1000)
          machine.reset()
          run = False


      if sel == "d":
         mainOctopus()
         print("Display test >>>")
         print('=' * 30)
         print("[od] --- oled display test")
         print("[m7] --- max display 8x7-segm")
         print("[m8] --- max display 8x8-matrix")
         print("[sd] --- serial display")
         print("[nd] -+- Nextion display")
         print("[id] -+- ink display")
         print('=' * 30)
         sel_d = input("select: ")

         if sel_d == "od":
              print("oled display test >")
              from lib import ssd1306
              time.sleep_ms(1500)
              i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
              oled = ssd1306.SSD1306_I2C(128, 64, i2c)

              oled.fill(1)
              oled.show()
              time.sleep_ms(300)
              oled.fill(0)                # reset display
              oled.show()

              # write text on x, y
              oled.text('OLED test', 25, 10)
              oled.text(get_hhmm(), 45,29) #time HH:MM
              oled.hline(0,50,128,1)
              oled.text("octopusLAB 2018",5,55) #time HH:MM
              oled.show()
              time.sleep_ms(1000)

         if sel_d == "m7":
             from lib.max7219_8digit import Display
             #spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
             #ss = Pin(15, Pin.OUT)
             d7 = Display(spi, ss)
             d7.write_to_buffer('12345678')
             d7.display()

         if sel_d == "m8":
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

         if sel_d == "sd":
                   from machine import UART
                   uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
                   uart.write('C')      #test quick clear display

                   uart.write('W7')   #change color
                   uart.write('h30')  #horizontal line
                   uart.write('h230') #horizontal line

                   uart.write('R0')
                   uart.write('W2')   #color
                   uart.write('QoctopusLAB - UART2 test*')
                   time.sleep_ms(100)
                   uart.write('R2')
                   uart.write('W1')   #color
                   uart.write('QESP32 & ROBOTboard*')
                   time.sleep_ms(100)

                   uart.write('R5')
                   uart.write('W2')   #color

                   num=9
                   for i in range(num):
                       uart.write('Q')
                       uart.write(str(num-i-1))
                       uart.write('*')
                       time.sleep_ms(500)

      if sel == "r":
             mainOctopus()
             print("Robot board test >>>")
             print('=' * 30)
             print("[dc] --- dc motor test")
             print("[se] --- servo")
             print("[sm] --- step motor")
             print('=' * 30)

             sel_r = input("select: ")
             if sel_r == "dc":
                  print("dc motor test >")

             if sel_r == "se":
                print("servo1 test >")

                #pwm_center = int(pinout.SERVO_MIN + (pinout.SERVO_MAX-pinout.SERVO_MIN)/2)
                pwm_center = 60
                pin_servo1 = Pin(pinout.PWM1_PIN, Pin.OUT)
                servo1 = PWM(pin_servo1, freq=50, duty=pwm_center)
                print("setup OK")
                time.sleep_ms(1500)
                servo1 = PWM(pin_servo1, freq=50, duty=SERVO_MAX)
                time.sleep_ms(1500)
                servo1 = PWM(pin_servo1, freq=50, duty=SERVO_MIN)

      if sel == "p":
            mainOctopus()
            print("Projects >>>")
            print('=' * 30)
            print("[1] --- temporary")
            print("[2] --- todo")
            print("[3] --- ")
            print('=' * 30)

            sel_p = input("select: ")
            if sel_p == "1":
                 print("project 1 >")


    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("> delta time: "+str(delta))
    beep(pwm0, 2000, 50)
    print("all OK, press CTRL+D to soft reboot")
    blink(led, 50)
