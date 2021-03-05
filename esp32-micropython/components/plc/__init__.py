# PLC main module
# Input / Output
# Operand_AND / Operand_NAND / Operand_OR

class PLC_base():
    pass


class Output():
    def set_value(self):
        raise "Not implemented"

    def get_value(self):
        raise "Not implemented"


class Operands():
    def input(self):
        raise "Not Implemented"

    def inputs(self):
        raise "Not Implemented"

    @property
    def output(self):
        raise "Not Implemented"


class Operand_AND():
    def __init__(self, inputs=None):
        self._inputs = inputs or list()

    def add_input(self, input):
        self._inputs.append(input)

    @property
    def output(self):
        for i in self._inputs:
            val = i.output
            if not val:
                return False

        return True


class Operand_NAND(Operand_AND):
    @property
    def output(self):
        return not super().output


class Operand_OR():
    def __init__(self, inputs=None):
        self._inputs = inputs or list()

    def add_input(self, input):
        self._inputs.append(input)

    @property
    def output(self):
        for i in self._inputs:
            val = i.output
            if val:
                return True

        return False


class Operand_NOR(Operand_OR):
    @property
    def output(self):
        return not super().output


class Operand_NOT(Operands):
    def __init__(self, input):
        self._input = input

    @property
    def output(self):
        return not self._input.output


class PLC_exception(Exception):
    pass


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
