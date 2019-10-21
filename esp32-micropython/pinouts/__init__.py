try:
    from micropython import const
except ModuleNotFoundError:
    def const(value):
        return value


class Pinout:
    def __init__(self):
        pass

    def platform(self):
        raise NotImplementedError("Not specified platform")
