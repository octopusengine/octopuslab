from components.plc.operands import PLC_operand


class PLC_operand_OR(PLC_operand):
    def __init__(self, inputs=None):
        self._inputs = inputs or list()

    def add_input(self, input):
        self._inputs.append(input)

    @property
    def output(self):
        for i in self._inputs:
            val = i.output
            if val:
                return True

        return False


class PLC_operand_NOR(PLC_operand_OR):
    @property
    def output(self):
        return not super().output
