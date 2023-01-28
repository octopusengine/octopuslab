# basic library for class Buzzer 
# DtLab 2022

__version__ = "1.0.0"

from time import sleep_ms
from machine import Pin, PWM
from sensobox.pinout import PIN_BUZZER

class Buzzer():
    def __init__(self, pin=PIN_BUZZER):
        self.pwm = None
        self.speed = 60 # BPM

        if pin is None:
            print("WARN: Pin is None")
            return

        self.pwm = PWM(Pin(pin, Pin.OUT), freq=1, duty=0)
        self.pwm.deinit()

    def play_tone(self, freq, length = 2, volume=50):
        # length = 2 > 1/2, length = 8 > 1/8...
        length_tone = int(60/self.speed*1000/length)
        
        if freq > 0:
            
            self.pwm.init(freq=freq, duty=volume)
            
        sleep_ms(length_tone)
        self.pwm.deinit()

    def beep(self, freq=1000, length=100):  # port,freq,time / default 1000,100
        self.play_tone(freq, length, 512)

    def play_tones(self, melody, autoPause = False, volume=50):
        for note in melody:
            if note == 0:
                self.play_tone(0, 8, 0)
            else:
                self.play_tone(note, 8, volume)

    def play_melody(self, melody, speed = 60, autoPause = 0, volume=50):
        self.speed = speed
        for note in melody:
            if note[0] == 0:
                self.play_tone(0, note[1], 0)
            else:
                self.play_tone(note[0], note[1], volume)
            if autoPause:
                self.pwm.deinit()
                self.play_tone(0, autoPause, 0)
                
        if autoPause:
            self.play_tone(0, autoPause, 0)
