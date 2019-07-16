from time import sleep_ms
from machine import Pin, PWM

def play_tone(pwm_pin, freq, length, volume=50):
    print("WARGNING: DEPRECATED: Do not USE, Use Buzzer class instead!!")

    if pwm_pin is None:
        print("DUMMY_BUZZ DEPRECATED: play tone (freq {0}, time {1} volume {2})".format(freq, length, volume))
        sleep_ms(length)
        return

    # continuously
    pwm_pin.duty(volume)
    pwm_pin.freq(freq)
    sleep_ms(length)

def beep(p,f,t):  # port,freq,time
    print("WARGNING: DEPRECATED: Do not USE, Use Buzzer class instead!!")

    if p is None:
        print("DUMMY_BUZZ DEPRECATED: beep (freq {0}, time {1})".format(f ,t))
        sleep_ms(t)
        return

    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(512)   # set duty cycle
    sleep_ms(t)
    p.duty(0)
    #b.deinit()

def play_melody(pwm_pin, melody, volume=50):
    print("WARGNING: DEPRECATED: Do not USE, Use Buzzer class instead!!")

    if pwm_pin is None:
        print("DUMMY_BUZZ DEPRECATED: play melody")
        return

    for note in melody:
        if note == 0:
            pwm_pin.duty(0)
        else:
            pwm_pin.duty(volume)
            pwm_pin.freq(note)
        sleep_ms(150)

class Buzzer():
    def __init__(self, pin):
        self.pwm = None

        if pin is None:
            print("WARN: Pin is None, this buzzer will be dummy")
            return

        self.pwm = PWM(Pin(pin, Pin.OUT), 0, 0)

    def nosound(self):
        self.play_tone(0, 0, 0)

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
