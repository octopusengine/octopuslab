from components.plc import PLC_base

class PLC_element(PLC_base):
    def __init__(self, initialvalue=False):
        self._value = initialvalue

    @property
    def output(self):
        return self._value
