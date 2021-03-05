# PLC main module
# Input / Output
# Operand_AND / Operand_NAND / Operand_OR

class PLC_base():
    pass


class PLC_exception(Exception):
    pass


class Output():
    def set_value(self):
        raise "Not implemented"

    def get_value(self):
        raise "Not implemented"


class Override():
    def __init__(self, input):
        self._input = input
        self._value = False
        self._enabled = False

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def output(self):
        if self._enabled:
            return self._value
        else:
            return self._input.output


class Override_FIXED(Override):
    def __init__(self, input, value):
        self._value = value
        super().__init__(input)


class Override_DYNAMIC(Override):
    def __init__(self, input):
        self._value = False
        super().__init__(input)

    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        self._value = value
