# library for pwm servo
# octopusLAB 2019
from time import sleep
from machine import Pin, PWM
from util import pinout
from util.octopus import map

SERVO_MIN = 45
PWM_CENTER = 60
SERVO_MAX = 130

class Servo():

    def __init__(self, pin):
        print(type(pin))
        print(type(Pin.OUT))
        self.pin_servo = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin_servo, freq=50, duty=PWM_CENTER)
        self.min = SERVO_MIN
        self.max = SERVO_MAX

    def set_degree(self, angle):
        self.pwm.duty(map(angle, 0,150, self.min, self.max))

    def servo_test(self):
        print("servo1 test >")
        #pwm_center = int(pinout.SERVO_MIN + (pinout.SERVO_MAX-pinout.SERVO_MIN)/2)
                    
        sleep(2)
        self.set_degree(self.min)
        sleep(2)
        self.set_degree(self.max)
        sleep(2)
        
        print("degree > 0")
        self.set_degree(0)
        sleep(2) 
        print("degree > 45")
        self.set_degree(45) 
        sleep(2) 
        print("degree > 90")
        self.set_degree(90)