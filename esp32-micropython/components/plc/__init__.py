# PLC main module
# Input / Output
# Operand_AND / Operand_NAND / Operand_OR


class Input():
    def __init__(self):
        pass

    def output(self):
        return self._value


class DummyInput(Input):
    def __init__(self, initialvalue=0):
        self._value = initialvalue


class Output():
    def setValue():
        raise "Not implemented"

    def getvalue():
        raise "Not implemented"


class Operands():
    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def input():
        raise "Not Implemented"

    def inputs():
        raise "Not Implemented"

    def output():
        raise "Not Implemented"

    value = property(get_value, set_value)


class Operand_AND():
    def __init__(self, inputs=[]):
        self._inputs = inputs

    def addInput(self, input):
        self._inputs.append(input)

    def output(self):
        for i in self._inputs:
            val = i.output()
            if not val:
                return False

        return True


class Operand_NAND(Operand_AND):
    def output(self):
        return not super().output()


class Operand_OR():
    def __init__(self, inputs=[]):
        self._inputs = inputs

    def addInput(self, input):
        self._inputs.append(input)

    def output(self):
        for i in self._inputs:
            val = i.output()
            if val:
                return True

        return False


class Operand_NOR(Operand_OR):
    def output(self):
        return not super().output()


class Operand_NOT(Operands):
    def __init__(self, input):
        self._input = input

    def output(self):
        return not self._input.output()


class Override_FIXED():
    def __init__(self, value):
        self._value = value

    def output(self):
        return self._value


class Override_DYNAMIC():
    def __init__(self, input):
        self._input = input
        self._value = False
        self._enabled = False

    def output(self):
        if self._enabled:
            return self._value

        return self._input.output()


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

print("AND: {}".format(a.output()))
print("NAND: {}".format(na.output()))
print("NOT: {}".format(nt.output()))
print("OR: {}".format(or1.output()))
print("OD: {}".format(od1.output()))
"""


i4._value = False
od1._enabled = True
od1._value = True
print("OR: {}".format(or1.output()))
od1._value = False
print("OR: {}".format(or1.output()))
od1._enabled = False
print("OR: {}".format(or1.output()))
