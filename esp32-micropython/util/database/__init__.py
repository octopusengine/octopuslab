"""
octopusLAB - database class

"""
from util.octopus import printTitle


class Database():
    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        raise NotImplementedError("Using abstract class")
