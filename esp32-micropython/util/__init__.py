from time import sleep
from machine import Pin, PWM
from util import pinout

SERVO_MIN = 45
PWM_CENTER = 60
SERVO_MAX = 130

class Servo():

    def __init__(self, pin):
        print(type(pin))
        print(type(Pin.OUT))
        self.pin_servo = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin_servo, freq=50, duty=PWM_CENTER)

    def set_degree(self, angle):
        self.pwm.duty(map(angle, 0,150, SERVO_MIN, SERVO_MAX))

    def servo_test(self):
        print("servo1 test >")
        #pwm_center = int(pinout.SERVO_MIN + (pinout.SERVO_MAX-pinout.SERVO_MIN)/2)
                    
        sleep(2)
        self.set_degree(SERVO_MAX)
        sleep(2)
        self.set_degree(SERVO_MIN)
        sleep(2)
        
        print("degree > 0")
        self.set_degree(0)
        sleep(2) 
        print("degree > 45")
        self.set_degree(45) 
        sleep(2) 
        print("degree > 90")
        self.set_degree(90)