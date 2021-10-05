# OctopusLAB (c) 2021
# Version 0.2

# by Petr Kracik

__version__ = "0.2.0"


class Keypad():
    def __init__(self, i2c, address=0x21, invert=False):
        self.i2c = i2c
        self.address = address

        if not invert:
            self.KEYPAD = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
            ]
        else:
            self.KEYPAD = [
            ['D', 'C', 'B', 'A'],
            ['#', '9', '6', '3'],
            ['0', '8', '5', '2'],
            ['*', '7', '4', '1']
            ]

        self.ROW         = [0,1,2,3]
        self.COLUMN      = [4,5,6,7]

        self.pinState = self.i2c.readfrom(self.address, 1)[0]

    def pin_write(self, pinNum, level):
        mask = 1 << pinNum

        if(level):
            self.pinState |= mask
        else:
            self.pinState &= ~mask

        tmp = bytearray(1)
        tmp[0] = self.pinState
        self.i2c.writeto(self.address, tmp)

    def pin_read(self, pinNum):
        mask = 0x1 << pinNum
        pinVal = self.i2c.readfrom(self.address, 1)[0]

        pinVal &= mask
        if (pinVal == mask):
            return 1
        else:
            return 0

    def getKey(self):
        self.i2c.writeto(self.address, b'\x0F')

        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = self.pin_read(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        if rowVal <0 or rowVal > 3:
            return None

        self.i2c.writeto(self.address, b'\xF0')

        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = self.pin_read(self.COLUMN[j])
            if tmpRead == 0:
                colVal=j

        if colVal <0 or colVal >3:
            return None

        # Return the value of the key pressed
        return self.KEYPAD[rowVal][colVal]
