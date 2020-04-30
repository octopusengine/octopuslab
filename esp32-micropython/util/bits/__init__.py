# basic library - bits operations - for bool and 8bit expander
# from util.bits import neg, reverse
# b1 = 0b11111001
# int2bin(reverse(b1))   >   '10011111'
# int2bin(reverse(b1),1) > '0b10011111'

__version__ = "1.0.0"

from micropython import const

bar = (
const(0b00000000), #0
const(0b10000000), #1
const(0b11000000), #2
const(0b11100000), #3
const(0b11110000), #4
const(0b11111000), #5
const(0b11111100), #6
const(0b11111110), #7
const(0b11111111)  #8
)


def neg(bb, bit8 = True):
    if bit8:
        return(bb ^ 0xff)
    else:
        return(~ bb)


def reverse(num):
    num = ((num & 0xf0) >> 4) | ((num & 0x0f) << 4) # abcdefgh -> efghabcd
    num = ((num & 0xcc) >> 2) | ((num & 0x33) << 2) # efghabcd -> ghefcdab
    num = ((num & 0xaa) >> 1) | ((num & 0x55) << 1) # ghefcdab -> hgfedcba
    return num


def int2bin(num, string=False):
    return (bin(num)) if string else (bin(num)[2:])


def get_bit(byte, index):
    return 1 if (byte & (1 << index)) else 0


def set_bit(byte, index, bit):
    return byte | (1 << index) if bit else byte & (~ (1 << index))