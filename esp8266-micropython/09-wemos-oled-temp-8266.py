"""
wemos - 8266:
This is simple usage of SSD1306 OLED display over I2C
temperature sensor
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

#SPI_MOSI_PIN = const(23)
#BUILT_IN_LED = 2
BUTT1_PIN = 14    #d6 x gpio16=d0
PIEZZO_PIN = 0    # IoT wemos {piezz---D3=PWM1}
ONE_WIRE_PIN = 2  # IoT wemos {DEV1 ---D4=PWM2} built in led width pull up
#WS_LED_PIN = 15  #wemos gpio14 = d5

I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2

butt1 = Pin(BUTT1_PIN, Pin.IN, Pin.PULL_UP)

i2c = machine.I2C(-1, machine.Pin(I2C_SCL_PIN), machine.Pin(I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
aa = 16
y0 = 5
x0 = aa+5

pwm0 = PWM(Pin(PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)

ts = TemperatureSensor(ONE_WIRE_PIN)

def beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(200)   # set duty cycle
    time.sleep_ms(t)
    p.duty(0)

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
beep(pwm0,500,100)

while True:
    temp = ts.read_temp()
    threeDigits(int(temp*10),True,True)
    b =butt1.value()
    if not b:
       beep(pwm0,500,100)
       threeDigits(0,True,True)
    time.sleep_ms(1000)
