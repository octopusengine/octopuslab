# this module is for Basic simple examples & tests
# it's loaded in boot.py and provides function octopus()
# user is questioned in interactive mode

# esp8266 / wemos / esp32 doit...

# ampy -p /COM4 put util/octopus-8266.py util/octopus.py

import time
import os, uos
import json, ujson
import gc #mem_free
import machine, ubinascii
from machine import Pin, PWM, Timer

#SPI_MOSI_PIN = const(23)
BUILT_IN_LED = 2
BUTT1_PIN = 12 #d6 x gpio16=d0
PIEZZO_PIN = 14
WS_LED_PIN = 15 #wemos gpio14 = d5
ONE_WIRE_PIN = 13
I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2

tim = Timer(-1)
led = Pin(BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

pwm0 = PWM(Pin(PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)

def beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(200)   # set duty cycle
    time.sleep_ms(t)
    p.duty(0)
    #b.deinit()

def blink(t): # time sleep
    led.value(1)
    time.sleep_ms(t)
    led.value(0)
    time.sleep_ms(t)

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:]
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

def printLine():
    print("------------------------------------------------")

def mainMenu():
    printLine()
    print("Menu: Basic simple examples & tests")
    printLine()
    print("[b] - built-in led/beep/button")
    print("[i] - device & system info")
    print("[o] - oled display test")
    print("[r] - RGB WS led test")
    print("[s] - setup machine and wifi")
    print("[t] - temperature")
    print("[w] - wifi test")
    print("[q] - QUIT")
    printLine()

    sel = input("select: ")
    #print("your select: "+str(sel))
    return sel

#-------------
def octopus():
    beep(pwm0,500,100) # start beep
    tim.init(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print("test timer - thread delay"))
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
    print("(Press Ctrl+C to abort | CTRL+D to soft reboot)")
    print()

    time.sleep_us(10)       # sleep for 10 microseconds
    blink(500)
    time.sleep_ms(1000)     # 1s
    start = time.ticks_ms()

    run= True
    while run:
      sel = mainMenu()
      beep(pwm0,2000,50)

      if sel == "b":
           count = 5
           for _ in range(count):
               beep(pwm0,500,100)
               blink(500)

      if sel == "s":
          print(">>> setup()")

      elif sel == "i":
          print("uPy version: "+str(os.uname()[3]))
          print("> unique_id: "+str(get_eui()))
          #print("--- MAC: "+str(mac2eui(get_eui())))
          gc.collect()
          print("> mem_free: "+str(gc.mem_free()))
          print("> machine.freq: "+str(machine.freq()))

      if sel == "o":
          from lib import ssd1306
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

      if sel == "s":
          from util.setup import setup
          setup()

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

      if sel == "q":
          run = False

    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("> delta time: "+str(delta))
    beep(pwm0,2000,50)
    print("all OK, press CTRL+D to soft reboot")
    blink(50)
