from components.plc.inputs import PLC_input

class PLC_input_dummy(PLC_input):
    def __init__(self, initialvalue=0):
        self._value = initialvalue

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
