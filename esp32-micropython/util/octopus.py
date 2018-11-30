# this module is for Basic simple examples & tests
# it's loaded in boot.py and provides function octopus()
# user is questioned in interactive mode

# esp8266 / wemos / esp32 doit...

# ampy -p /COM4 put util/octopus-8266.py util/octopus.py

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

# try:
#   spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(SPI_CLK_PIN), mosi=Pin(SPI_MOSI_PIN))
#   ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
#   from lib.max7219 import Matrix8x8
#   display8 = Matrix8x8(spi, ss, 1) #1/4
# except:
#   print("SPI device already in use")

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
    blink(led, 500)
    time.sleep_ms(1000)     # 1s
    start = time.ticks_ms()

    run= True
    while run:
      sel = mainMenu()
      beep(pwm0, 1000, 50)

      if sel == "b":
           count = 5
           for _ in range(count):
               beep(pwm0, 500, 100)
               blink(led, 500)

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
          from util.buzzer.melody import mario
          play_melody(pwm0, mario)
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
          i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
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

      if sel == "u":
            print("uart - todo")

      if sel == "v":
          print("active variables: ")
          print(dir())

      if sel == "w":
          from wifi_connect import read_wifi_config, WiFiConnect
          time.sleep_ms(2000)
          wifi_config = read_wifi_config()
          print("config for: " + wifi_config["wifi_ssid"])
          w = WiFiConnect()
          w.events_add_connecting(connecting_callback)
          w.events_add_connected(connected_callback)
          w.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
          print("WiFi: OK")

      if sel == "q":
          run = False

    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("> delta time: "+str(delta))
    beep(pwm0, 2000, 50)
    print("all OK, press CTRL+D to soft reboot")
    blink(led, 50)
