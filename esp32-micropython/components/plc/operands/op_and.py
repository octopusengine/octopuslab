from components.plc.operands import PLC_operand


class PLC_operand_AND(PLC_operand):
    def __init__(self, inputs=None):
        self._inputs = inputs or list()

    def add_input(self, input):
        self._inputs.append(input)

    @property
    def output(self):
        for i in self._inputs:
            val = i.output
            if not val:
                return False

        return True


class PLC_operand_NAND(PLC_operand_AND):
    @property
    def output(self):
        return not super().output
