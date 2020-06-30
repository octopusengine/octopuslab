# octopusLAB empty.py

print("--- empty.py ---> main.py --- test")
print("This is simple Micropython example | ESP32 & octopusLAB")
print('-' * 50)
from gc import mem_free
print("--- RAM before octopus(): " + str(mem_free()))

from utils.octopus import getFree
getFree(True)
print()

