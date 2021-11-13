# OctopusLAB (c) 2021
# Version 0.3

# by Petr Kracik

__version__ = "0.3.0"


class Keypad():
    def __init__(self, i2c, address=0x21, invert=False):
        self.i2c = i2c
        self.address = address
        self.bussize = 8

        self.KEYPAD = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
        ]

        if not invert:
            self.ROW    = [0,1,2,3]
            self.COLUMN = [4,5,6,7]
        else:
            self.ROW    = [7,6,5,4]
            self.COLUMN = [3,2,1,0]


    def pin_read(self, pinNum):
        mask = 0x1 << pinNum

        value = self.i2c.readfrom(self.address, self.bussize // 8)
        pinVal = value[0]

        if self.bussize > 8:
            pinVal += value[1] << 8

        pinVal &= mask
        if (pinVal == mask):
            return 1
        else:
            return 0


    def getKey(self):
        c = 0
        tmp = bytearray(self.bussize // 8)

        for i in self.ROW:
            c += 1 << i

        tmp[0] = c
        if self.bussize > 8:
            tmp[1] = c >> 8

        self.i2c.writeto(self.address, tmp)

        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = self.pin_read(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        if rowVal < 0 or rowVal > len(self.ROW) - 1:
            return None

        c = 0
        for i in self.COLUMN:
            c += 1 << i

        tmp[0] = c
        if self.bussize > 8:
            tmp[1] = c >> 8

        self.i2c.writeto(self.address, tmp)

        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = self.pin_read(self.COLUMN[j])
            if tmpRead == 0:
                colVal=j

        if colVal < 0 or colVal > len(self.COLUMN) - 1:
            return None

        # Return the value of the key pressed
        return self.KEYPAD[rowVal][colVal]


# 5x4 keypad
#self.KEYPAD = [
#            ['F1', 'F2', '#', '*'],
#            ['1', '2', '3', '^'],
#            ['4', '5', '6', 'v'],
#            ['7', '8', '9', 'ESC'],
#            ['<', '0', '>', 'ENT']
#            ]
#        self.ROW    = [0,1,2,3,4]
#        self.COLUMN = [8,7,6,5]

# 4x4 keypad
#self.KEYPAD = [
#            ['1', '2', '3', 'A'],
#            ['4', '5', '6', 'B'],
#            ['7', '8', '9', 'C'],
#            ['*', '0', '#', 'D']
#            ]
#        self.ROW    = [0,1,2,3]
#        self.COLUMN = [4,5,6,7]
#Invert
#        self.ROW    = [7,6,5,4]
#        self.COLUMN = [3,2,1,0]



class Keypad16(Keypad):
    def __init__(self, i2c, address=0x20, invert=False):
        self.i2c = i2c
        self.address = address
        self.bussize = 16

        self.KEYPAD = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
        ]

        if invert:
            self.ROW    = [7,6,5,4]
            self.COLUMN = [3,2,1,0]
        else:
            self.ROW    = [0,1,2,3]
            self.COLUMN = [4,5,6,7]
