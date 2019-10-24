# basic library for IoT board
# octopusLAB 2019
""" 
re1  = Relay()
re1.value(1)

pwm_led = Pwm()
pwm_led.duty(300)

from util.iot import TemperatureSensor
tt = TemperatureSensor(32)
tx = tt.ds.scan()
tt.read_temp(tx[0])
tt.read_temp(tx[0])
"""

from time import sleep_ms
from machine import Pin, PWM
from util.pinout import set_pinout
from onewire import OneWire
from ds18x20 import DS18X20


pinout = set_pinout()
default_relay_pin = pinout.RELAY_PIN
default_pwm_pin = pinout.MFET_PIN
# default_temp_pin = pinout.MFET_PIN

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


class Thermometer:
    def __init__(self, pin=32):
        from onewire import OneWire
        from ds18x20 import DS18X20

        self.pin = pin
        self.ts = []
        try:
            self.ds = DS18X20(OneWire(Pin(self.pin)))
            self.ts = self.ds.scan()
        except Exception:
            print("Found {0} dallas sensors, temp active: {1}".format(len(ts), io_conf.get('temp')))

    def get_pin(self):
        return self.pin

    def get_temp(self, index):
        self.ds.convert_temp()
        sleep_ms(750)
        temp = self.ds.read_temp(self.ts[index])
        temp = int(temp * 10) / 10
        return temp

    def get_temp_n(self):
        tw = []
        self.ds.convert_temp()
        sleep_ms(750)
        for t in self.ts:
            temp = self.ds.read_temp(t)
            tw.append(int(temp * 10) / 10)
        return tw

"""
class TemperatureSensor:
    # Represents a Temperature sensor (Dallas DS18X20)
    def __init__(self, pin):
        # Finds address of single DS18B20 on bus specified by `pin`
        self.ds = DS18X20(OneWire(Pin(pin)))
        addrs = self.ds.scan()
        if not addrs:
            raise Exception('no DS18B20 found at bus on pin %d' % pin)
        # save what should be the only address found
        self.addr = addrs.pop()

    def read_temp(self, addr, fahrenheit=False):
        self.ds.convert_temp()
        sleep_ms(750)
        temp = self.ds.read_temp(addr)
        if fahrenheit:
            return self.c_to_f(temp)
        return temp

    @staticmethod
    def c_to_f(c):
        return (c * 1.8) + 32
"""