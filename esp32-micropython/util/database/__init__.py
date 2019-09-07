"""
octopusLAB - database class
from util.database import Db
db = Db("test")
db.addOne("one","1")
db.listAll()
"""
import btree


class Db():
    def __init__(self, name="octopus"):
        self.file = name + ".db"
        # simple test: root > todo sub directory
        
        try:
            f = open(self.file, "r+b")
        except OSError:
            f = open(self.file, "w+b")

        self.data = btree.open(f) 
        #super().open(f)
    
    def addOne(self, key, val):
        self.data[key] = val
        self.data.flush()
    
    def listAll(self):
        print("test list")
        for key in self.data:
            print(key, end=" | ")
            print(self.data[key])
