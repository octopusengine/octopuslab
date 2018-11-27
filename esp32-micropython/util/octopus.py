# this module is for Basic simple examples & tests
# it's loaded in boot.py and provides function octopus()
# user is questioned in interactive mode

# esp8266 / wemos / esp32 doit...

# ampy -p /COM4 put util/octopus-8266.py util/octopus.py

from micropython import const
import time
import os, uos
import json, ujson
import gc #mem_free
import machine, ubinascii
from machine import Pin, PWM, SPI, Timer

BUILT_IN_LED = 2
#---8266---
#SPI_MOSI_PIN = const(23)
"""
BUTT1_PIN = 12 #d6 x gpio16=d0
PIEZZO_PIN = 14
WS_LED_PIN = 15 #wemos gpio14 = d5
ONE_WIRE_PIN = 13
I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2
"""
#---esp32---
BUTT1_PIN = 12 #d6 x gpio16=d0
PIEZZO_PIN = const(27)  #14 //MOTOR_4A = const(27)
WS_LED_PIN = const(13) #v2+ > 15
ONE_WIRE_PIN = const(32)

I2C_SCL_PIN=const(22)
I2C_SDA_PIN=const(21)
#SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)

#PWM/servo:
PWM1_PIN = const(17)
PWM2_PIN = const(16)
PWM3_PIN = const(4)

HALL_SENSOR = const(8)
PIN_ANALOG = const(36)
#---------------------
try:
  spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(SPI_CLK_PIN), mosi=Pin(SPI_MOSI_PIN))
  ss = Pin(SPI_CS0_PIN, Pin.OUT)
  from lib.max7219 import Matrix8x8
  display8 = Matrix8x8(spi, ss, 1) #1/4
except:
  print("SPI device already in use")

pwm0 = PWM(Pin(PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)

from lib.buzzer.notes import *
mario = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0]

"""
timNote = Timer(8, freq=3000)
ch = timNote.channel(2, Timer.PWM, pin=Pin(PIEZZO_PIN))

tim = Timer(-1)
"""
led = Pin(BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

def simple_beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(512)   # set duty cycle
    time.sleep_ms(t)
    p.duty(0)
    #b.deinit()

def blink(t): # time sleep
    led.value(1)
    time.sleep_ms(t)
    led.value(0)
    time.sleep_ms(t)

def simple_fast_blink():
    led.value(1)
    time.sleep_ms(50)
    led.value(0)
    time.sleep_ms(100)

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:]
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

def mainMenu():
    print('-' * 30)
    print("Menu: Basic simple examples & tests")
    print('-' * 30)
    print("[b] - built-in led/beep/button")
    print("[c] - clear terminal")
    print("[f] - file info/dir")
    print("[i] - device & system info")
    print("[m] - piezzo melody")
    print("[m7] - max display 8x7-segm")
    print("[m8] - max display 8x8-matrix")
    print("[o] - oled display test")
    print("[r] - RGB WS led test")
    print("[r8] -8x RGB WS led test")
    print("[sd] -serial display")
    print("[s] - setup machine and wifi")
    print("[t] - temperature")
    print("[u] - uart test")
    print("[v] - list active variables")
    print("[w] - wifi test")
    print("[q] - QUIT")
    print('=' * 30)

    sel = input("select: ")
    #print("your select: "+str(sel))
    return sel
    print()


# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    simple_fast_blink()
    # np[0] = (0, 128, 0)
    # np.write()
    simple_fast_blink()
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    # np[0] = (0, 0, 128)
    # np.write()
    simple_fast_blink()

def beep(pwm_pin, freq, length, volume=50):
       pwm_pin.duty(volume)
       pwm_pin.freq(freq)
       time.sleep(length/1000)

def play_melody(pwm_pin, melody, volume=50):
 for note in melody:
  if note == 0:
      pwm_pin.duty(0)
  else:
      pwm_pin.duty(volume)
      pwm_pin.freq(note)
  time.sleep(0.15)

#-------------
def octopus():
    ###beep(pwm0,500,100) # start beep
    #tim.init(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print("test timer - thread delay"))
    #tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))
    print("      ,'''`.")
    print("     /      \ ")
    print("     |(@)(@)|")
    print("     )      (")
    print("    /,'))((`.\ ")
    print("   (( ((  )) ))")
    print("   )  \ `)(' / ( ")
    print()
    print("Hello, this is basic octopusLAB example (2018/11)")
    print(" (Press Ctrl+C to abort | CTRL+D to soft reboot)")
    print()

    time.sleep_us(10)       # sleep for 10 microseconds
    blink(500)
    time.sleep_ms(1000)     # 1s
    start = time.ticks_ms()

    run= True
    while run:
      sel = mainMenu()
      simple_beep(pwm0,1000,50)

      if sel == "b":
           count = 5
           for _ in range(count):
               simple_beep(pwm0,500,100)
               blink(500)

      if sel == "c":
          print(chr(27) + "[2J") # clear terminal
          print("\x1b[2J\x1b[H") # cursor up

      if sel == "f":
          print("file info /dir/ls:") #
          print(os.listdir())
          print("> lib: "+str(os.listdir("lib")))
          print("> util: "+str(os.listdir("util")))

      if sel == "i":
          print("uPy version: "+str(os.uname()[3]))
          print("> unique_id: "+str(get_eui()))
          #print("--- MAC: "+str(mac2eui(get_eui())))
          gc.collect()
          print("> mem_free: "+str(gc.mem_free()))
          print("> machine.freq: "+str(machine.freq()))

      if sel == "m":
          time.sleep_ms(500)
          play_melody(pwm0, mario)
          """
          # from lib import notes as *
          beep(pwm0,200,50)
          time.sleep_ms(300)
          beep(pwm0,500,50)
          time.sleep_ms(300)
          beep(pwm0,900,50)
          time.sleep_ms(1000)

          # play Mario Bros tone example
          # source from here http://www.linuxcircle.com/2013/03/31/playing-mario-bros-tune-with-arduino-and-piezo-buzzer/

          #pwm0.duty()  # get current duty cycle
          pwm0.duty(512)   # set duty cycle
          for i in range(30,120):
              print(i)
              pwm0.freq(i*10)     # set frequency
              time.sleep_ms(50)
          """
          pwm0.duty(0)

      if sel == "m8":
        count = 5
        for i in range(count):
           display8.text(str(i),0,0,1)
           display8.show()
           time.sleep_ms(300)

      if sel == "o":
          from lib import ssd1306
          time.sleep_ms(2000)
          i2c = machine.I2C(-1, machine.Pin(I2C_SCL_PIN), machine.Pin(I2C_SDA_PIN))
          oled = ssd1306.SSD1306_I2C(128, 64, i2c)

          oled.fill(1)
          oled.show()
          time.sleep_ms(300)

          # reset display
          oled.fill(0)
          oled.show()

          # write text on x, y
          oled.text('OLED test', 20, 20)
          oled.show()
          time.sleep_ms(1000)


      if sel == "sd":
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
        from neopixel import NeoPixel
        NUMBER_LED = 1
        pin = Pin(WS_LED_PIN, Pin.OUT)
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
       pin = Pin(WS_LED_PIN, Pin.OUT)
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
         pin = Pin(WS_LED_PIN, Pin.OUT)
         np = NeoPixel(pin, NUMBER_LED)
         for i in range(NUMBER_LED):
           np[i] = (1, 0, 0)
           time.sleep_ms(1)# REVIEW:
         np.write()

      if sel == "s":
           from util.setup import setup
           setup()

      if sel == "u":
            print("uart - todo")

      if sel == "v":
          print("active variables: ")
          print(dir())

      if sel == "w":
          from util.wifi_connect import WiFiConnect
          time.sleep_ms(2000)
          f = open('config/wifi.json', 'r')
          d = f.read()
          f.close()
          j = json.loads(d)
          ssid=j["wifi_ssid"]
          print("config for: " + ssid)
          w = WiFiConnect()
          w.events_add_connecting(connecting_callback)
          w.events_add_connected(connected_callback)
          w.connect(ssid,j["wifi_pass"])
          print("WiFi: OK")

      if sel == "q":
          run = False

    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("> delta time: "+str(delta))
    beep(pwm0,2000,50)
    print("all OK, press CTRL+D to soft reboot")
    blink(50)
