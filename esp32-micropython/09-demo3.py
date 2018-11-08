# usage:
# __import__('09-remote-wsled')
# Android: RoboRemo/menu/connect IP:PORT
# Win: ncat -u IP PORT

from time import sleep, sleep_ms
from neopixel import NeoPixel
from machine import Pin, PWM, I2C
import ssd1306
import framebuf #for oled image
import WiFiConfig  # Remember set SSID and password in WiFiConfig.py file
from WiFiConnect import WiFiConnect # Include wifi
import usocket

# Import OctopusLab Robot board definition file
import octopus_robot_board as o # octopusLab main library - "o" < octopus
from temperature import TemperatureSensor

# Warning: RobotBoard version 1 use different WS Pin 13 !
pin_ws = Pin(13, Pin.OUT)
WSUDPPort = 12811
WSBindIP = None

ONE_WIRE_PIN = 32
ts = TemperatureSensor(ONE_WIRE_PIN)

pwm_center = int(o.SERVO_MIN + (o.SERVO_MAX-o.SERVO_MIN)/2)

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def set_degree(servo, angle):
    servo.duty(map(angle, 0,150, o.SERVO_MIN, o.SERVO_MAX))

pin_servo1 = Pin(o.PWM1_PIN, Pin.OUT)
servo1 = PWM(pin_servo1, freq=50, duty=pwm_center)
pin_servo2 = Pin(o.PWM2_PIN, Pin.OUT)
servo2 = PWM(pin_servo2, freq=50, duty=pwm_center)
sleep(1)

i2c = I2C(-1, Pin(o.I2C_SCL_PIN), Pin(o.I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# test_whole display
oled.fill(1)
oled.show()

sleep_ms(300)

# reset display
oled.fill(0)
oled.show()

np = NeoPixel(pin_ws, 1)
pin_led = Pin(o.BUILT_IN_LED, Pin.OUT)

def simple_blink():
    pin_led.value(1)
    sleep(0.1)
    pin_led.value(0)
    sleep(0.1)

# Default WS led light RED as init
np[0] = (128, 0, 0)
np.write()
simple_blink()

# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    simple_blink()
    np[0] = (0, 128, 0)
    np.write()
    simple_blink()
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    np[0] = (0, 0, 128)
    np.write()
    simple_blink()

IMAGE_WIDTH = 63
IMAGE_HEIGHT = 63

with open('test_image.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, IMAGE_WIDTH, IMAGE_HEIGHT, framebuf.MONO_HLSB)

    # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
    oled.invert(1)
    oled.blit(fbuf, 0, 0)

oled.text("Octopus", 66,6)
oled.text("Lab", 82,16)
oled.text("Micro", 74,35)
oled.text("Python", 70,45)
oled.show()
sleep(5)

oled.fill(0)
oled.text('octopus LAB', 20, 20)
oled.text('WiFi Connect', 20, 35)
oled.invert(0)
oled.show()

w = WiFiConnect()
w.events_add_connecting(connecting_callback)
w.events_add_connected(connected_callback)
w.connect(WiFiConfig.WIFI_SSID, WiFiConfig.WIFI_PASS)

sleep(1)
oled.fill(0)
oled.text('octopus LAB', 20, 20)
oled.text('WiFi - OK', 20, 35)
oled.pixel(0, 0, 1)
oled.pixel(127, 0, 1)
oled.show()
sleep(1)

temp = ts.read_temp()
oled.text('T = %.1f C' % temp, 25, 50)
oled.pixel(0, 0, 0)
oled.pixel(127, 0, 0)
oled.show()

if WSBindIP is not None:
    print("UDP Server run on {}:{}".format(WSBindIP, WSUDPPort))

    us = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    us.bind((WSBindIP, WSUDPPort))

    ws_red = 0
    ws_green = 0
    ws_blue = 0

    def parseWS_LED(data):
        global ws_red
        global ws_green
        global ws_blue
        global np

        if len(data) < 1:
            return

        if data.decode()[0] == 'R':
            ws_red = int(data[1:])

        elif data.decode()[0] == 'G':
            ws_green = int(data[1:])

        elif data.decode()[0] == 'B':
            ws_blue = int(data[1:])

        else:
            print("Unknown data: {}".format(data.decode()))
            return

        print(data.decode())
        np[0] = (ws_red, ws_green, ws_blue)
        np.write()

    while True:
        data = us.recv(1024)
        parseWS_LED(data)
        set_degree(servo1,ws_red)
        set_degree(servo2,ws_blue)
        oled.fill(0)
        oled.text('octopus LAB', 20, 20)
        oled.text(" --- "+str(ws_red)+" ---", 20, 35)

        temp = ts.read_temp()
        oled.text('T = %.1f C' % temp, 25, 20)
        oled.show()
