from components.plc.inputs import PLC_input

class PLC_input_fixed(PLC_input):
    def __init__(self, fixed_value):
        self._value = fixed_value

plc_input_fixed_high = PLC_input_fixed(True)
plc_input_fixed_low = PLC_input_fixed(False)
