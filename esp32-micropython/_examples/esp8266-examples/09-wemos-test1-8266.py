"""
wemos - 8266:
This is simple usage of SSD1306 OLED display over I2C
ws rgb led
button

# reset device
"""
import machine
from machine import Pin
import time
from time import sleep
from neopixel import NeoPixel
from lib import ssd1306

#import octopus_robot_board as o #octopusLab main library - "o" < octopus
BUILT_IN_LED = 2
BUTT1_PIN = 12 #d6 x gpio16=d0

I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2

i2c = machine.I2C(-1, machine.Pin(I2C_SCL_PIN), machine.Pin(I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

NUMBER_LED = 1
WS_LED_PIN = 14 #wemos gpio14 = d5
pin = Pin(WS_LED_PIN, Pin.OUT)
butt = Pin(BUTT1_PIN, Pin.IN, Pin.PULL_UP)
np = NeoPixel(pin, NUMBER_LED)

led = Pin(BUILT_IN_LED, Pin.OUT)

def simple_blink_pause():
    led.value(0)
    sleep(1/10)
    led.value(1)
    sleep(1/5)

# test_whole display
oled.fill(1)
oled.show()

time.sleep_ms(300)

# reset display
oled.fill(0)
oled.show()

# write text on x, y
oled.text('OLED test', 20, 20)
oled.show()
time.sleep_ms(2000)

for i in range(1,1000):
   b =butt.value()
   print(b)
   oled.fill(0)
   oled.text('OctopusLab', 20, 15)
   oled.text(" --- "+str(i)+" -->"+str(b), 20, 35)
   oled.show()
   #time.sleep_ms(1000)

   np[0] = (128, 0, 0) #R
   np.write()
   simple_blink_pause()

   np[0] = (0,128, 0) #G
   np.write()
   simple_blink_pause()

   np[0] = (0, 0, 128) #B
   np.write()
   simple_blink_pause()
