"""
octopusLAB - database class
from util.database.btreedb import BTreeDB
db = BTreeDB("test")
db.addOne("one","1")
db.listAll()
"""

__version__ = "0.0.1"

from util.database import Database
import btree
from util.octopus import printTitle


class BTreeDB(Database):
    def __init__(self, name="octopus"):
        self.file = name + ".db"
        # simple test: root > todo sub directory

        try:
            f = open(self.file, "r+b")
        except OSError:
            f = open(self.file, "w+b")

        self.data = btree.open(f)
        #super().open(f)

    def addOne(self, key, val):  # edit is the same > last value
        self.data[key] = val
        self.data.flush()

    def delKey(self, key):
        del self.data[key]

    def listAll(self):
        printTitle("listAll > ")
        for key in self.data:
            print(key, end=" | ")
            print(self.data[key])
