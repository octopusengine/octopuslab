# MicroPython 28BYJ-48 step motor on ULN2803 driver via PFC8574 I2C expander

import time
from micropython import const

# one step must consist of multiple coil switching, each bit is one coil
# clockwise (right)
step_elements_cw = (
    const(0b0001),
    const(0b0011),
    const(0b0010),
    const(0b0110),
    const(0b0100),
    const(0b1100),
    const(0b1000),
    const(0b1001)
)
# counter clockwise (left)
step_elements_ccw = (
    const(0b1001),
    const(0b1000),
    const(0b1100),
    const(0b0100),
    const(0b0110),
    const(0b0010),
    const(0b0011),
    const(0b0001)
)


class SM28BYJ48:
    def __init__(self, i2c, address, id=1):
        """
        id is motor ID either 1 or 2
        """
        self.i2c = i2c
        self.address = address
        self.id = id

    def one_step(self, ccw=False, delay_ms=1):
        # set direction
        if ccw:
            step_elements = step_elements_ccw
        else:
            step_elements = step_elements_cw

        for el in step_elements:
            if self.id == 2:
                # to control motor no. 2, shift
                el <<= 4
            # overtype to bytearray, because if not i2c complains "TypeError: object with buffer protocol required"
            self.i2c.writeto(self.address, bytearray([el]))
            time.sleep_ms(1)

    def turn_step(self, count, ccw=False, delay_ms=1):
        # minimum delay is 1 ms, step motor can't work faster
        for _ in range(count):
            self.one_step(ccw, delay_ms)

    def turn_degree(self, angle, ccw=False):
        # 64 / 45 is a gearbox included in 28BYJ-48 step motor
        step_count = angle * 64 / 45
        self.turn_step(step_count, ccw)
