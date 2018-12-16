# Upload wav file using ampy

import os

# Timer
from machine import Timer

# DAC
from machine import DAC, Pin

# Play rutine
def play(t):
    if wav.tell() == wav_size:
        t.deinit()
        # rewind wav to data begining
        wav.seek(44)
        print ("Stop play")
        return
    dac.write(ord(wav.read(1)))
    
def play_loop(t):
    if wav.tell() == wav_size:
        print ("Rewind to begin")
        wav.seek(44)
        return

    dac.write(ord(wav.read(1)))


# Init DAC
dac = DAC(Pin(25))

# Middle value for speaker
dac.write(0x7F)

# Determine size of WAV
wav_size = os.stat("untitled3.wav")[6]

wav = open("untitled3.wav", "rb")
wav.seek(44)

t1 = Timer(1)
t1.init(freq=8000, mode=Timer.PERIODIC, callback=play)
