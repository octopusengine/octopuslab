# PLC main module
# Input / Output
# Operand_AND / Operand_NAND / Operand_OR


class Input():
    def __init__(self):
        self._value = None
        pass

    @property
    def output(self):
        return self._value


class Dummy_input(Input):
    def __init__(self, initialvalue=0):
        self._value = initialvalue


class Output():
    def set_value(self):
        raise "Not implemented"

    def get_value(self):
        raise "Not implemented"


class Operands():
    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def input(self):
        raise "Not Implemented"

    def inputs(self):
        raise "Not Implemented"

    @property
    def output(self):
        raise "Not Implemented"

    value = property(get_value, set_value)


class Operand_AND():
    def __init__(self, inputs=[]):
        self._inputs = inputs

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
    def __init__(self, inputs=[]):
        self._inputs = inputs

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

"""
a = Operand_AND()
na = Operand_NAND()
or1 = Operand_OR()

i1 = DummyInput(True)
od1 = Override_DYNAMIC(i1)
i2 = DummyInput(0)
i3 = DummyInput("asd")
i4 = DummyInput(True)

a.addInput(i1)
a.addInput(i2)
a.addInput(i3)

na.addInput(i1)
na.addInput(i2)
na.addInput(i3)

or1.addInput(od1)
or1.addInput(a)

nt = Operand_NOT(a)

print("AND: {}".format(a.output))
print("NAND: {}".format(na.output))
print("NOT: {}".format(nt.output))
print("OR: {}".format(or1.output))
print("OD: {}".format(od1.output))


i4._value = False
od1.enabled = True
print("OR: {}".format(or1.output))
od1.value = False
print("OR: {}".format(or1.output))
od1.enabled = False
print("OR: {}".format(or1.output))
"""
