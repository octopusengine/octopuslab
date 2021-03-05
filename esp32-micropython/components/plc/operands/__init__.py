class PLC_operand():
    def input(self):
        raise NotImplementedError()

    def inputs(self):
        raise NotImplementedError()

    @property
    def output(self):
        raise NotImplementedError()
