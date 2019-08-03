# Display7 - 7segment x 8 digit
# Display8 - 8x8 matrix
# max7919

REG_NO_OP           = 0x00
REG_DIGIT_BASE      = 0x01
REG_DECODE_MODE     = 0x09
REG_INTENSITY       = 0x0a
REG_SCAN_LIMIT      = 0x0b
REG_SHUTDOWN        = 0x0c
REG_DISPLAY_TEST    = 0x0f

CHAR_DATA = {
    '0': 0x7e, '1': 0x30, '2': 0x6d, '3': 0x79, '4': 0x33, 
    '5': 0x5b, '6': 0x5f, '7': 0x70, '8': 0x7f, '9': 0x7b,
    'a': 0x77, 'b': 0x1f, 'c': 0x4e, 'd': 0x3d, 'e': 0x4f, 
    'f': 0x47, 'g': 0x7b, 'h': 0x37, 'i': 0x30, 'j': 0x3c,
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
    def __init__(self, spi, ss, intensity=6):
        self.spi = spi
        self.ss = ss
        self.buffer = bytearray(8)
        self.intensity = intensity
        self.reset()

    def reset(self):
        self.set_register(REG_DECODE_MODE, 0)
        self.set_register(REG_INTENSITY, self.intensity)
        self.set_register(REG_SCAN_LIMIT, 7)
        self.set_register(REG_DISPLAY_TEST, 0)
        self.set_register(REG_SHUTDOWN, 1)

    def set_register(self, register, value):
        self.ss.value(0)
        self.spi.write(bytearray([register, value]))
        self.ss.value(1)
    
    def intensity(self, i):
        self.send(self.intensity, i)

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
        if(len(dotRemoved)) < 8:
            dotRemoved   = "%-8s" % dotRemoved
            dots         = "%-8s" % dots
        for index in range(0,8):
            self.buffer[7-index] = self.decode_char(dotRemoved[index]) + self.decode_char(dots[index])

    def display(self):
        for i in range(0,8):
            self.set_register(REG_DIGIT_BASE + i, self.buffer[i])

    def show(self, toDisplay):
        self.write_to_buffer(toDisplay)
        self.display()
