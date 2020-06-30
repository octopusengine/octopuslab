# basic library for class Buzzer 
# octopusLAB 2019

""" 
piezzo = Buzzer(33)
piezzo.beep()
"""

__version__ = "1.0.0"

from time import sleep_ms
from machine import Pin, PWM
# from components.buzzer.notes import *
# from components.buzzer.melody import alert1
# piezzo.speed = 100 # BPM
# piezzo.play_melody(alert1)

# piezzo.speed = 30
# piezzo.play_melody(canon_d,32)

# old beep and play_tone functions? > Use Buzzer class instead!



class Buzzer():
    def __init__(self, pin):
        self.pwm = None
        self.speed = 60 # BPM

        if pin is None:
            print("WARN: Pin is None, this buzzer will be dummy")
            return

        self.pwm = PWM(Pin(pin, Pin.OUT), 0, 0)

    def nosound(self):
        if self.pwm is None:
            print("DUMMY_BUZZ: nosound")
            return

        self.pwm.duty(0)


    def play_tone(self, freq, length = 2, volume=50):
        # length = 2 > 1/2, length = 8 > 1/8...
        length_tone = int(60/self.speed*1000/length)
        if self.pwm is None:
            print("DUMMY_BUZZ: play tone (freq {0}, time {1} volume {2})".format(freq, length, volume))
            sleep_ms(length_tone)
            return

        # continuously
        self.pwm.duty(volume)
        self.pwm.freq(freq)
        sleep_ms(length_tone)
        self.pwm.duty(0)


    def beep(self, freq=1000, length=100):  # port,freq,time / default 1000,100
        self.play_tone(freq, length, 512)
        self.nosound()


    def play_tones(self, melody, autoPause = False, volume=50):
        for note in melody:
            if note == 0:
                self.play_tone(0, 8, 0)
            else:
                self.play_tone(note, 8, volume)

        # Stop play in case in melody will not be zero on end
        self.nosound()


    def play_melody(self, melody, speed = 60, autoPause = 0, volume=50):
        self.speed = speed
        for note in melody:
            if note[0] == 0:
                self.play_tone(0, note[1], 0)
            else:
                self.play_tone(note[0], note[1], volume)
            if autoPause:
                self.nosound()
                self.play_tone(0, autoPause, 0)


        # Stop play in case in melody will not be zero on end
        self.nosound()
        if autoPause:
            self.play_tone(0, autoPause, 0)

