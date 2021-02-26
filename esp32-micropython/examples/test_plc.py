from time import sleep
from utils.octopus_lib import i2c_init
from components.lm75 import LM75B
from components.i2c_expander import Expander8
from utils.bits import neg, reverse, int2bin, get_bit, set_bit

IN1, IN2, IN3, IN4     = 0, 1, 2, 3
OUT1, OUT2, OUT3, OUT4 = 4, 5, 6, 7

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
    sleep(0.1)
    exp8.write_8bit(255)
    sleep(0.5)
    
exp8.write_8bit(set_bit(255,OUT1,0))
sleep(1)
exp8.write_8bit(set_bit(255,OUT2,0))
sleep(1)
exp8.write_8bit(set_bit(255,OUT3,0))
sleep(1)
exp8.write_8bit(set_bit(255,OUT4,0))

sleep(1)
exp8.write_8bit(255)

print("- EEPROM:")