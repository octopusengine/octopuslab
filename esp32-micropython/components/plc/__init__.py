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

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


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


class PLC_element():
    def __init__(self, initialvalue=False):
        self._value = initialvalue

    @property
    def output(self):
        return self._value


class PLC_element_RS(PLC_element):
    def __init__(self, set_element=None, reset_element=None, initialvalue=False):
        self._set_element = set_element
        self._reset_element = reset_element
        super().__init__(initialvalue)

    @property
    def set(self):
        return self._set_element

    @set.setter
    def set(self, element):
        if element:
            self._set_element = element

    @property
    def reset(self):
        return self._reset_element

    @reset.setter
    def reset(self, element):
        if element:
            self._reset_element = element
    
    @property
    def output(self):
        if self._set_element.output:
            self._value = True

        if self._reset_element.output:
            self._value = False

        return self._value


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
i1 = Dummy_input(False)
i2 = Dummy_input(False)

rs = PLC_element_RS(i1, i2)

print("Init: ", rs.output)
i1.value = True
print("SET 1", rs.output)
i1.value = False
print("SET 0", rs.output)

i2.value = True
print("RESET 1", rs.output)

i2.value = False
print("RESET 0", rs.output)




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
