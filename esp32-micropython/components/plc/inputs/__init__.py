from components.plc import PLC_base

class PLC_input():
    def __init__(self):
        self._value = None
        pass

    @property
    def output(self):
        return self._value
