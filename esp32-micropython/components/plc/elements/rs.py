from . import PLC_element

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
        s = self._set_element.output
        r = self._reset_element.output
        if r == s:
            return self._value

        if s:
            self._value = True

        if r:
            self._value = False

        return self._value
