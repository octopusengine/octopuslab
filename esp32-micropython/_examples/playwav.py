# Upload wav file using ampy or deploy tar

import os

import struct

# Timer
from machine import Timer

# DAC
from machine import DAC, Pin

# Play rutine
def play(t):
    global wav_pos
    if wav_pos == wav_size:
        t.deinit()
        # rewind wav to data begining
        wav_pos = wav.seek(44)
        print ("Stop play")
        return

    dw(ord(wr(1)))
    wav_pos+=1

def play_loop(t):
    global wav_pos
    if wav_pos == wav_size:
        print ("Rewind to begin")
        wav_pos = wav.seek(44)
        return

    dw(ord(wr(1)))
    wav_pos+=1

# Play rutine
def play_mem(t):
    global mem_pos
    if mem_pos == len(mem):
        t.deinit()
        print ("Stop play")
        return
    dac.write(mem[mem_pos])
    mem_pos+=1


def actualSampleRate(t):
    global wav_pos
    global wav_pos_prev

    print("Samples: {0}".format(wav_pos - wav_pos_prev))

    wav_pos_prev = wav_pos

# Init DAC
dac = DAC(Pin(26))

# Middle value for speaker
dac.write(0x7F)

dw = dac.write

wav_pos = 0
wav_pos_prev = 0

wav_file = "11__koala-11k.wav"
wav_file = "20__holandska.wav"
wav_file = "22__dzn dzn dzn-11k.wav"
wav_file = "untitled3.wav"

wav = open(wav_file, "rb")
wr = wav.read

# Read WAV header
wav.seek(20)
wav_format, \
wav_channels, \
wav_sample_rate, \
wav_byterate, \
wav_blockalign, \
wav_bits_per_sample, \
wav_datasignature, \
wav_data_size = struct.unpack('HHIIHH4sI', wav.read(24))

wav_size = wav_data_size + 44

# Seek to PCM data begin
wav_pos = wav.seek(44)

print("WAV File: {0}\n\
WAV Format: {1}\n\
WAV Channels: {2}\n\
WAV Sample rate: {3}\n\
WAV Bits per sample: {4}".format(wav_file,
                                 wav_format,
                                 wav_channels,
                                 wav_sample_rate,
                                 wav_bits_per_sample))

t1 = Timer(0)
t2 = Timer(1)

t1.init(freq=wav_sample_rate, mode=Timer.PERIODIC, callback=play)
t2.init(freq=1, mode=Timer.PERIODIC, callback=actualSampleRate)
