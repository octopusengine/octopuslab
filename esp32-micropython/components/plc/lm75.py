# The MIT License (MIT)

class LM75():
    ADDRESS = 0x49 # 48
    FREQUENCY = 100000 # 100k

    def __init__(self,i2c):
        # self.i2c = I2C(scl=D1, sda=D2, freq=self.FREQUENCY)
        self.i2c = i2c

    def get_output(self):
        """Return raw output from the LM75 sensor."""
        output = self.i2c.readfrom(self.ADDRESS, 2)
        return output[0], output[1]

    def get_temp(self):
        """Return a tuple of (temp_c, point)."""
        from math import floor
        temp = self.get_output()
        return int(temp[0]), floor(int(temp[1]) / 23)


