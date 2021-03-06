from components.plc import PLC_base


class PLC_operand(PLC_base):
    def input(self):
        raise NotImplementedError()

    def inputs(self):
        raise NotImplementedError()

    @property
    def output(self):
        raise NotImplementedError()
