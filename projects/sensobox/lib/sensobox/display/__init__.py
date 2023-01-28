"""
Based on:

MicroPython TM1637 quad 7-segment LED display driver
https://github.com/mcauser/micropython-tm1637

MIT License
Copyright (c) 2016 Mike Causer

"""

from machine import Pin
from micropython import const
from time import sleep_us, sleep_ms
from ..pinout import PIN_DISPLAY_CLK, PIN_DISPLAY_DIO

TM1637_CMD1 = const(64)  # 0x40 data command
TM1637_CMD2 = const(192)  # 0xC0 address command
TM1637_CMD3 = const(128)  # 0x80 display control command
TM1637_DSP_ON = const(8)  # 0x08 display on
TM1637_DELAY = const(10)  # 10us delay between clk/dio pulses
TM1637_MSB = const(128)  # msb is the decimal point or the colon depending on your display

_CHARACTER_SEGMENTS = {
    '0': 0b00111111,
    '1': 0b00000110,
    '2': 0b01011011,
    '3': 0b01001111,
    '4': 0b01100110,
    '5': 0b01101101,
    '6': 0b01111101,
    '7': 0b00000111,
    '8': 0b01111111,
    '9': 0b01101111,
    'a': 0b01110111,
    'b': 0b01111100,
    'c': 0b00111001,
    'd': 0b01011110,
    'e': 0b01111001,
    'f': 0b01110001,
    'g': 0b00111101,
    'h': 0b01110110,
    'i': 0b00000110,
    'j': 0b00011110,
    'k': 0b01110110,
    'l': 0b00111000,
    'm': 0b01010101,
    'n': 0b01010100,
    'o': 0b00111111,
    'p': 0b01110011,
    'q': 0b01100111,
    'r': 0b01010000,
    's': 0b01101101,
    't': 0b01111000,
    'u': 0b00111110,
    'v': 0b00011100,
    'w': 0b00101010,
    'x': 0b01110110,
    'y': 0b01101110,
    'z': 0b01011011,
    ' ': 0b00000000,
    '-': 0b01000000,
    '*': 0b01100011,
    '.': 0b10000000,
}

_UNKNOWN_CHARACTER = _CHARACTER_SEGMENTS['*']

# swap segments to make it upsidedown
_UP_DOWN_TRANSFORMER = [0, 1, 5, 6, 7, 2, 3, 4]
_DISPLAY_LIMIT = 4


class Display(object):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""

    def __init__(self, clk=PIN_DISPLAY_CLK, dio=PIN_DISPLAY_DIO, brightness=7):
        self.clk = Pin(clk)
        self.dio = Pin(dio)

        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        sleep_us(TM1637_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)

    def _stop(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.dio(1)

    def _write_data_cmd(self):
        # automatic address increment, normal mode
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        # display on, set brightness
        self._start()
        self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | self._brightness)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            sleep_us(TM1637_DELAY)
            self.clk(1)
            sleep_us(TM1637_DELAY)
            self.clk(0)
            sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)

    def brightness(self, val=None):
        """Set the display brightness 0-7."""
        # brightness 0 = 1/16th pulse width
        # brightness 7 = 14/16th pulse width
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")

        self._brightness = val
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def write(self, segments, pos=0):
        """Display up to 6 segments moving right from a given position.
        The MSB in the 2nd segment controls the colon between the 2nd
        and 3rd segments."""
        if not 0 <= pos <= 5:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        self._start()

        self._write_byte(TM1637_CMD2 | pos)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._write_dsp_ctrl()

    def hex(self, val):
        """Display a hex value 0x0000 through 0xffff, right aligned."""
        string = '{:04x}'.format(val & 0xffff)
        self.write(self.encode_string(string))

    def temperature(self, num):
        if num < -9:
            self.show('lo')  # low
        elif num > 99:
            self.show('hi')  # high
        else:
            string = '{0: >2d}'.format(num)
            self.write(self.encode_string(string))
        self.write([_SEGMENTS[38], _SEGMENTS[12]], 2)  # degrees C

    def scroll(self, string, delay=250):
        segments = string if isinstance(string, list) else self.encode_string(string)
        data = [0] * 8
        data[4:0] = list(segments)
        for i in range(len(segments) + 5):
            self.write(data[0 + i:4 + i])
            sleep_ms(delay)

    def clear(self):
        self.write([0, 0, 0, 0])

    def write_char(self, char, pos=0):
        self.write([_CHARACTER_SEGMENTS[char]], pos)

    # max 1 byte
    # bits moving
    # 0bzzyyyxxx -> 0bzzxxxyyy
    @staticmethod
    def transform_upsidedown(val):
        bit_str = "{0:08b}".format(val)
        result = list("00000000")
        for i in range(len(bit_str)):
            result[_UP_DOWN_TRANSFORMER[i]] = bit_str[i]
        return int('0b' + "".join(result))

    @staticmethod
    def _convert_string(string, scroll):
        if scroll:
            return string.lower()
        last_char = ''
        n = 0

        for c in string:
            if c == '.' and last_char != '.':
                continue
            n += 1
            if n == _DISPLAY_LIMIT:
                break

        return string[:n - 1]

    @staticmethod
    def _convert_boolean(boolean, scroll):
        if scroll:
            return str(boolean).lower()

        return 'true' if boolean else 'fals'

    @staticmethod
    def _convert_integer(integer, scroll):
        if not scroll and not (- 10 ** _DISPLAY_LIMIT - 1) <= integer <= (10 ** _DISPLAY_LIMIT - 1):
            raise ValueError('Number has too much digits and scrolling is disabled')

        return str(integer)

    # todo
    @staticmethod
    def _convert_float(num, scroll):
        pass

    _TYPES_CONVERTERS = {
        str: lambda v, _: v.lower(),
        bool: _convert_boolean,
        int: _convert_integer,
        float: _convert_float,
    }

    @staticmethod
    def encode_string(string):
        segments = []

        for char in string:
            if char == '.':
                if len(segments) > 0:
                    segments[-1] = segments[-1] + _CHARACTER_SEGMENTS['.']
                    continue

            try:
                s = _CHARACTER_SEGMENTS[char]
            except KeyError:
                s = _UNKNOWN_CHARACTER

            segments.append(s)

        return segments

    """
    Show value on display

    :param value: Value to display (str, bool, int, floar, None)
    :param alignment: True - right, False - left
    :param orientation: True - up, False - down
    :param scroll: Show overflowing text by scrolling
    :param delay: int - delay between scroll segment change 
    :return: None
    """

    def show(self, value, alignment=True, orientation=True, scroll=True, delay=250):
        val_type = type(value)

        if val_type not in Display._TYPES_CONVERTERS.keys():
            raise ValueError(f'Invalid value type: "{str(val_type)}"')

        if not isinstance(alignment, bool):
            raise ValueError(f'Parameter "aligment" must be type boolean')

        if not isinstance(scroll, bool):
            raise ValueError(f'Parameter "scroll" must be type boolean')

        if not isinstance(delay, int) or delay <= 0:
            raise ValueError(f'Parameter "delay" must be integer greater than 0')

        if value is None:
            value = 'none'

        converter = Display._TYPES_CONVERTERS[type(value)]

        encoded = Display.encode_string(converter(value, scroll))

        if not orientation:
            encoded.reverse()
            encoded = [Display.transform_upsidedown(e) for e in encoded]

        if len(encoded) < _DISPLAY_LIMIT:
            # also turns off not used segments
            add = (_DISPLAY_LIMIT - len(encoded)) * [0]

            if alignment:
                encoded = add + encoded
            else:
                encoded += add

        if scroll:
            encoded = (_DISPLAY_LIMIT * [0]) + encoded + (_DISPLAY_LIMIT * [0])
            length = len(encoded)

            for i in range(length):
                if orientation:
                    self.write(encoded[i:_DISPLAY_LIMIT + i])
                else:
                    self.write(encoded[length - i - _DISPLAY_LIMIT: length - i])
                sleep_ms(delay)

        else:
            self.write(encoded)

