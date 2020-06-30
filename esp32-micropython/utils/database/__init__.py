"""
octopusLAB - database class

"""

__version__ = "1.0.1"

from utils.octopus_lib import printTitle


class Database():
    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        raise NotImplementedError("Using abstract class")
