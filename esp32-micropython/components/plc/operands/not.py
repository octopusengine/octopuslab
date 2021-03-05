from components.plc.operands import PLC_operand


class PLC_operand_NOT(PLC_operand):
    def __init__(self, input):
        self._input = input

    @property
    def output(self):
        return not self._input.output
