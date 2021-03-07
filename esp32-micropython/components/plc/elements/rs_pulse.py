from components.plc.elements import PLC_element
from utime import ticks_ms

class PLC_element_RS_pulse(PLC_element):
    def __init__(self, set_element=None, reset_element=None, initialvalue=False, pulse_s = 3):
        self._set_element = set_element
        self._set_element_old = False
        self._pulse_ms = pulse_s * 1000
        self._start_ms = 0
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
        _pulse_up = s > self._set_element_old
        _delta_ms = ticks_ms() - self._start_ms

        #print(self._set_element_old,_pulse_on,_delta_ms)

        if (_pulse_up):
            self._start_ms = ticks_ms()
            self._set_element_old = True

        """
        if r == s:
            return self._value
        """

        if (_delta_ms <= self._pulse_ms) and (_pulse_up):
            #print("pulse_on", _delta_ms)
            self._set_element_old = True
            self._value = True

        if (_delta_ms > self._pulse_ms):
            #print("pulse_off",_delta_ms)
            self._set_element_old = False
            self._value = False

        if r:
            self._value = False

        return self._value
