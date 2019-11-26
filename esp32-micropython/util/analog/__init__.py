# basic library for class Analog input 
# octopusLAB 2019

""" 
from util.analog import Analog
an1 = Analog(36)
an1.adc_test()
an1.get_adc_aver(20)

an1.adc.atten(ADC.ATTN_2_5DB) #Full range: 3.3v
"""

from time import sleep_ms, sleep_us
from machine import Pin, ADC

ADC_SAMPLES=100
ADC_HYSTERESIS=50


class Analog:
    def __init__(self, pin, value=False):
        #self.pin = None
        #if pin is None:
        #    print("WARN: Pin is None, this analog will be dummy")
        #    return
        self.pin = pin
        self.adcpin = Pin(pin, Pin.IN)
        self.adc = ADC(self.adcpin)
        self.adc.atten(ADC.ATTN_11DB) # setup


    def read(self):
        return self.adc.read()


    def adc_test(self,maxvolt = 4.2):
        print("analog input test: ")
        an = self.adc.read()
        print("RAW: " + str(an))
        # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
        print("volts: {0:.2f} V".format(an/4096*maxvolt), 20, 50)


    def get_adc_aver(self, num=10):
        sumAn = 0
        for i in range(num):
            an = self.adc.read()
            sumAn += an
            sleep_us(10)
        return int(sumAn/num)
