# simple basic test - ESP32 - Micropython - EDU_KIT1
print("-"*20)
print("--- test-sw / utils")
print("-"*20)

print("--- bits ---")
from utils.bits import neg
B1 = 0b11111001
print(neg(B1))


print("--- transform ---")
from utils.transform import *
p1 = Point2D()
p2 = Point2D()
p1.x, p1.y = polar2cart(10, 0)
print(p1)

print("--- database ---")
from utils.database.btreedb import BTreeDB
db = BTreeDB("test")
db.addOne("one","1")
db.listAll()
print("-"*20)

