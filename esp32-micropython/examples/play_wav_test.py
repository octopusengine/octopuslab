# Upload wav file using ampy or deploy tar
#
# TAR:
# import utils.setup
# utils.setup.deploy("http[s]://path/to/file.tar")

import os
import struct
from machine import Timer
from machine import DAC, Pin
from time import sleep

#from utils.pinout import set_pinout
#pinout = set_pinout()  
#out = pinout.PIEZZO_PIN

print("init")
sleep(3)

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

def play_loop_all(t):
    global wav_pos
    if wav_pos == wav_size:
        t.deinit()
        # rewind wav to data begining
        play_playlist()
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

    print("Samples: {0} Time: {1}".format(wav_pos - wav_pos_prev, wav_pos / wav_sample_rate))

    wav_pos_prev = wav_pos

def loadWav(wav_file):
    global wav_sample_rate
    global wav_size
    global wav_pos
    global wav

    wav = open(wav_file, "rb")

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
    return wav.read


playlist_pos = 0
def play_playlist():
    global wr
    global playlist_pos
    if playlist_pos >= len(wav_files):
        playlist_pos = 0

    wr = loadWav(wav_files[playlist_pos])
    t1.init(freq=wav_sample_rate, mode=Timer.PERIODIC, callback=play_loop_all)
    playlist_pos+=1
    sleep(1)

# Init DAC
dac = DAC(Pin(26))

# Middle value for speaker
dac.write(0x7F)

dw = dac.write

wav_pos = 0
wav_pos_prev = 0

wav_files = list()
wav_files.append("assets/wav/s1.wav")
wav_files.append("assets/wav/s2.wav")
wav_files.append("assets/wav/s3.wav")
wav_files.append("assets/wav/oeproj.wav")
wav_files.append("assets/wav/s5.wav")
wav_files.append("assets/wav/s6.wav")
wav_files.append("assets/wav/s7.wav")
wav_files.append("assets/wav/upycool.wav")

t1 = Timer(0)
t2 = Timer(1)

t2.init(freq=1, mode=Timer.PERIODIC, callback=actualSampleRate)

play_playlist()