"""
octopusLAB - database class

"""

__version__ = "1.0.0"

from util.octopus import printTitle


class Database():
    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        raise NotImplementedError("Using abstract class")
