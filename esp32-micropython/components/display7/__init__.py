# Display7 - 7segment x 8 digit
# max7919

__version__ = "1.1.0"

REG_NOOP            = 0x00
REG_DIGIT_BASE      = 0x01
REG_DECODE_MODE     = 0x09
REG_INTENSITY       = 0x0a
REG_SCAN_LIMIT      = 0x0b
REG_SHUTDOWN        = 0x0c
REG_DISPLAY_TEST    = 0x0f

CHAR_DATA = {
    '0': 0x7e, '1': 0x30, '2': 0x6d, '3': 0x79, '4': 0x33,
    '5': 0x5b, '6': 0x5f, '7': 0x70, '8': 0x7f, '9': 0x7b,
    'a': 0x77, 'b': 0x1f, 'c': 0x0d, 'd': 0x3d, 'e': 0x4f,
    'f': 0x47, 'g': 0x7b, 'h': 0x37, 'i': 0x04, 'j': 0x3c,
    'k': 0x57, 'l': 0x0e, 'm': 0x54, 'n': 0x15, 'o': 0x1d,
    'p': 0x67, 'q': 0x73, 'r': 0x05, 's': 0x5b, 't': 0x0f,
    'u': 0x1c, 'v': 0x3e, 'w': 0x2a, 'x': 0x37, 'y': 0x3b,
    'z': 0x6d, 'A': 0x77, 'B': 0x1f, 'C': 0x4e, 'D': 0x3d,
    'E': 0x4f, 'F': 0x47, 'G': 0x7b, 'H': 0x37, 'I': 0x30,
    'J': 0x3c, 'K': 0x57, 'L': 0x0e, 'M': 0x54, 'N': 0x15,
    'O': 0x1d, 'P': 0x67, 'Q': 0x73, 'R': 0x05, 'S': 0x5b,
    'T': 0x0f, 'U': 0x1c, 'V': 0x3e, 'W': 0x2a, 'X': 0x37,
    'Y': 0x3b, 'Z': 0x6d, ' ': 0x00, '-': 0x01,
    '\xb0': 0x63, '.': 0x80
}

class Display7:
    def __init__(self, spi, ss, intensity=6, units=1):
        self.spi = spi
        self.ss = ss
        self.units = units
        self.buffer = bytearray(8)
        self.intensity = intensity
        self.reset()


    def reset(self):
        self._command(REG_DECODE_MODE, 0)
        self._command(REG_INTENSITY, self.intensity)
        self._command(REG_SCAN_LIMIT, 7)
        self._command(REG_DISPLAY_TEST, 0)
        self._command(REG_SHUTDOWN, 1)


    def _rjust(self, instr, num, char):
        if len(instr) >= num:
            return instr

        return "{}{}".format(char*(num-len(instr)), instr)


    def _ljust(self, instr, num, char):
        if len(instr) >= num:
            return instr

        return "{}{}".format(instr, char*(num-len(instr)))


    def _write_data(self, register, value):
        self.spi.write(bytearray([register, value]))


    def _command(self, register, value):
        self.ss.value(0)
        self.spi.write(bytearray([register, value] * self.units))
        self.ss.value(1)


    def decode_char(self, c):
        disp = CHAR_DATA.get(c)
        return disp if disp is not None else ' '


    def split_dots_chars(self, msg):
        dots  = dotRemoved = ""
        index              = 0
        while(index < len(msg)-1):
            char = msg[index]
            nextChar = msg[index+1]
            if  (char  not in ".," and nextChar not in ".,"):  # aa
                dotRemoved += char
                dots       += " "
                index      += 1
            elif(char  not in ",." and nextChar     in ".,"):  # a.
                dotRemoved += char
                dots       += "."
                index      += 2
            elif(char      in ".," and nextChar not in ".,"):  # .a
                dotRemoved += " "
                dots       += "."
                index      += 1
            elif(char      in ".," and nextChar     in ".,"):  # ..
                dotRemoved += "  "
                dots       += ".."
                index      += 2
        if(len(dotRemoved)-dotRemoved.count(" ")+dots.count(".") < len(msg)): # loop missed last character
            lastChar        = msg[len(msg)-1]
            if(lastChar    in ".,"):
                dots       += "."
            else:
                dotRemoved += lastChar
                dots       += " "
        return  dotRemoved,   dots


    def write_to_buffer(self, toWrite):
        dotRemoved, dots = self.split_dots_chars(str(toWrite))

        dotRemoved   = self._rjust(dotRemoved, 8, ' ')
        dots         = self._rjust(dots, 8, ' ')

        for index in range(8):
            self.buffer[7-index] = self.decode_char(dotRemoved[index]) + self.decode_char(dots[index])


    def display(self, unit=1):
        for i in range(8):
            self.ss.value(0)
            for d in range(self.units):
                if d == unit - 1 or unit == 0:
                    self._write_data(REG_DIGIT_BASE + i, self.buffer[i])
                else:
                    self._write_data(REG_NOOP, 0)
            self.ss.value(1)


    def show(self, toDisplay, unit=1):
        self.write_to_buffer(toDisplay)
        self.display(unit)


    def clear(self, unit=0):
        if unit == 0:
            for u in range(self.units):
                self.show("", u+1)
        else:
            self.show("", unit)
