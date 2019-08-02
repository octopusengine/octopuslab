from time import sleep_ms
from machine import Pin, PWM

# old beep and play_tone functions? > Use Buzzer class instead!

class Buzzer():
    def __init__(self, pin):
        self.pwm = None

        if pin is None:
            print("WARN: Pin is None, this buzzer will be dummy")
            return

        self.pwm = PWM(Pin(pin, Pin.OUT), 0, 0)

    def nosound(self):
        if self.pwm is None:
            print("DUMMY_BUZZ: nosound")
            return

        self.pwm.duty(0)

    def play_tone(self, freq, length, volume=50):
        if self.pwm is None:
            print("DUMMY_BUZZ: play tone (freq {0}, time {1} volume {2})".format(freq, length, volume))
            sleep_ms(length)
            return

        # continuously
        self.pwm.duty(volume)
        self.pwm.freq(freq)
        sleep_ms(length)

    def beep(self, freq=1000, length=100):  # port,freq,time / default 1000,100
        self.play_tone(freq, length, 512)
        self.nosound()

    def play_melody(self, melody, volume=50):
        for note in melody:
            if note == 0:
                self.play_tone(0, 150, 0)
            else:
                self.play_tone(note, 150, volume)

        # Stop play in case in melody will not be zero on end
        self.nosound()
