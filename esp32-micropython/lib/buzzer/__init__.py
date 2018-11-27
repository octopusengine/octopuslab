from time import sleep

def beep(pwm_pin, freq, length, volume=50):
    pwm_pin.duty(volume)
    pwm_pin.freq(freq)
    sleep(length/1000)

def play_melody(pwm_pin, melody, volume=50):
    for note in melody:
        if note == 0:
            pwm_pin.duty(0)
        else:
            pwm_pin.duty(volume)
            pwm_pin.freq(note)
        sleep(0.15)

