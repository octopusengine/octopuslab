# The MIT License (MIT)

class LM75B():
    DEFAULT_ADDRESS = 0x49
    RESOLUTION_BITS = 11


    def __init__(self,i2c, addr = DEFAULT_ADDRESS):
        self.address = addr
        self.i2c = i2c


    def __twos_complement(self, input_value: int, num_bits: int) -> int:
        mask = 2 ** (num_bits - 1)
        return -(input_value & mask) + (input_value & ~mask)


    def get_temp(self):
        t = self.i2c.readfrom(self.address, 2)
        i = t[0] << 8 | t[1]

        return self.__twos_complement(i >> (16-self.RESOLUTION_BITS), self.RESOLUTION_BITS) * 0.125
