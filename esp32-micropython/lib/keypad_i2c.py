# Deprecated library
# backward compaitiblity

print("DEPRECATED: use module components.i2c_keypad class Keypad instead")

from components.i2c_keypad import Keypad

class keypad(Keypad):
    def __init__(self, i2c, address=0x21):
        print("DEPRECATED: use Keypad class instead")
        super().__init__(i2c, address)
