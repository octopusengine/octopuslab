# TODO: Implement input interupts if needed
class PCF8574:
    def __init__(self, i2c, address):
        self._i2c = i2c
        self._address = address
        self._input = 0  # Buffers the result of read in memory
        self._input_mask = 0  # Mask specifying which pins are set as input
        self._output = 0  # The state of pins set for output
        self._write()

    def _read(self):
        self._input = self._i2c.readfrom(self._address, 1)[0] & self._input_mask

    def _write(self):
        self._i2c.writeto(self._address, bytes([self._output | self._input_mask]))

    def read(self, pin):
        bit_mask = 1 << pin
        self._input_mask |= bit_mask
        self._output &= ~bit_mask
        self._write()  # Update input mask before reading
        self._read()
        return (self._input & bit_mask) >> pin

    def read8(self):
        self._input_mask = 0xFF
        self._output = 0
        self._write()  # Update input mask before reading
        self._read()
        return self._input

    def write(self, pin, value):
        bit_mask = 1 << pin
        self._input_mask &= ~bit_mask
        self._output = self._output | bit_mask if value else self._output & (~bit_mask)
        self._write()

    def write8(self, value):
        self._input_mask = 0
        self._output = value
        self._write()

    def set(self):
        self.write8(0xFF)

    def clear(self):
        self.write8(0x0)

    def toggle(self, pin):
        bit_mask = 1 << pin
        self._input_mask &= ~bit_mask
        self._output ^= bit_mask
        self._write()
