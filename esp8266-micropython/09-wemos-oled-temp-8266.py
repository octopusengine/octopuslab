"""
wemos - 8266:
This is simple usage of SSD1306 OLED display over I2C
ws rgb led
button

ampy -p /COM4 put 09-wemos-oled-temp-8266.py main.py
# reset device
"""
import machine
from machine import Pin, PWM
import time
from time import sleep
from neopixel import NeoPixel

from lib import ssd1306
from lib.temperature import TemperatureSensor

#import octopus_robot_board as o #octopusLab main library - "o" < octopus
BUILT_IN_LED = 2
BUTT1_PIN = 12 #d6 x gpio16=d0
PIEZZO_PIN = 14
WS_LED_PIN = 15 #wemos gpio14 = d5
ONE_WIRE_PIN = 13

I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2

i2c = machine.I2C(-1, machine.Pin(I2C_SCL_PIN), machine.Pin(I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

pwm0 = PWM(Pin(PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)

#ts = TemperatureSensor(ONE_WIRE_PIN)

aa = 16
y0 = 5
x0 = aa+5

def beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(200)   # set duty cycle
    time.sleep_ms(t)
    p.duty(0)
    #b.deinit()

NUMBER_LED = 1
pin = Pin(WS_LED_PIN, Pin.OUT)
butt = Pin(BUTT1_PIN, Pin.IN, Pin.PULL_UP)
np = NeoPixel(pin, NUMBER_LED)

led = Pin(BUILT_IN_LED, Pin.OUT)

def simple_blink_pause():
    led.value(0)
    sleep(1/10)
    led.value(1)
    sleep(1/5)

sevenSeg = [      #seven segment display
 [1,1,1,1,1,1,0], #0
 [0,1,1,0,0,0,0], #1
 [1,1,0,1,1,0,1], #2
 [1,1,1,1,0,0,1], #3
 [0,1,1,0,0,1,1], #4
 [1,0,1,1,0,1,1], #5
 [1,0,1,1,1,1,1], #6
 [1,1,1,0,0,0,0], #7
 [1,1,1,1,1,1,1], #8
 [1,1,1,1,0,1,1], #9
 [1,1,0,0,0,1,1], #deg
 [0,0,0,0,0,0,1]  #-
]

def oneDigit(seg,x,y,a): #segment /x,y position / a=size
    oled.hline(x,y,a,seg[0])
    oled.vline(x+a,y,a,seg[1])
    oled.vline(x+a,y+a,a,seg[2])
    oled.hline(x,y+a+a,a,seg[3])
    oled.vline(x,y+a,a,seg[4])
    oled.vline(x,y,a,seg[5])
    oled.hline(x,y+a,a,seg[6])

def threeDigits(d,point,deg): #display number 0-999 / point 99.9 / degrees
    d100=int(d/100)
    d10=int((d-d100*100)/10)
    d1= d-d100*100-d10*10
    oneDigit(sevenSeg[d100],x0,y0,aa)
    oneDigit(sevenSeg[d10],x0+aa+int(aa/2),y0,aa)
    oneDigit(sevenSeg[d1],x0+(aa+int(aa/2))*2,y0,aa)
    if point:
       oled.fill_rect(x0+(aa+int(aa/2))*2-5,y0+aa+aa,2,3,1) #test poin
    if deg:
       oneDigit(sevenSeg[10],x0+(aa+int(aa/2))*3,y0,aa) #test deg
    oled.show()

# ----------------------------------------------
oled.fill(0)

oled.text('OctopusLab', x0, 57)
oled.show()
time.sleep_ms(2000)

#temp = ts.read_temp()

for num in range(150,239):
    threeDigits(num,True,True)
    time.sleep_ms(50)
    #temp = ts.read_temp()
    #print(temp)

beep(pwm0,500,100)
oled.fill(0)
oled.text('OctopusLab - ok', x0, 57)
