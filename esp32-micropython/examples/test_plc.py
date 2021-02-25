from time import sleep
from utils.octopus_lib import i2c_init
from components.lm75 import LM75B
from components.i2c_expander import Expander8
from utils.bits import neg, reverse, int2bin, get_bit, set_bit

print("--- PLC shield ---")
print("-"*50)

print("- I2C:")
# i2c = i2c_init()
i2c = i2c_init(True,200)
print(i2c.scan())
# 34 expander / 73 therm. / 84 eeprom

lm = LM75B(i2c)
temp = lm.get_temp()
print("- Temp: ", temp)

exp8 = Expander8(34)
print("- PCF:", print(exp8.read()))

# bits4 = "0101"
# exp8.write_8bit(bits4)

for i in range(3):
    exp8.write_8bit(0)
    sleep(0.5)
    exp8.write_8bit(255)
    sleep(1)

print("- EEPROM:")
