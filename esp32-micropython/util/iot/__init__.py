# basic library for IoT board
# octopusLAB 2019
""" 
re1  = Relay()
re1.value(1)

pwm_led = Pwm()
pwm_led.duty(300)
"""

from time import sleep_ms
from machine import Pin, PWM
from util.pinout import set_pinout

pinout = set_pinout()
default_relay_pin = pinout.RELAY_PIN
default_pwm_pin = pinout.MFET_PIN 

class Relay:
    def __init__(self, pin=default_relay_pin, value=False):
        # self.pin = None
        self.state = value

        if pin is None:
            print("WARN: Pin is None, this relay will be dummy")
            return

        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(self.state)


    def get_pin(self):
        return self.pin


    def value(self, value=None):
        if value is None:
            if self.pin is not None:
                self.state = self.pin.value() # Update internal value in case someone changed it from outside

            return self.state

        self.state = value

        if self.pin is None:
            print("DUMMY_LED Value {0}".format(self.state))
            return

        self.pin.value(self.state)


    def toggle(self):
        self.value(not self.value())


    def demo_test(self, number=2, delay=3000):
        for _ in range (0, number):
            self.value(1)
            sleep_ms(delay)
            self.value(0)
            sleep_ms(delay)


# todo / prepare
class Pwm():
    def __init__(self, pin=default_pwm_pin, duty = 0, freq = 500):
        self.pwm = None

        if pin is None:
            print("WARN: Pin is None, this buzzer will be dummy")
            return
        
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin, freq, duty)

    def get_pin(self):
        return self.pin