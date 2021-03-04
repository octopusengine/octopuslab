from time import sleep
from utils.octopus_lib import i2c_init
from components.lm75 import LM75B
from components.i2c_expander import Expander8
from utils.bits import neg, reverse, int2bin, get_bit, set_bit
from components.plc import *

IN1, IN2, IN3, IN4     = 0, 1, 2, 3
OUT1, OUT2, OUT3, OUT4 = 4, 5, 6, 7
# OUT4 - signalization

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
print("- PCF:", exp8.read())

# bits4 = "0101"
# exp8.write_8bit(bits4)

for i in range(3):
    exp8.write_8bit(0)
    sleep(0.1)
    exp8.write_8bit(255)
    sleep(0.1)
    
exp8.write_8bit(set_bit(255,OUT1,0))
sleep(0.2)
exp8.write_8bit(set_bit(255,OUT2,0))
sleep(0.2)
exp8.write_8bit(set_bit(255,OUT3,0))
sleep(0.2)
exp8.write_8bit(set_bit(255,OUT4,0))

sleep(0.3)
exp8.write_8bit(255)

print("- EEPROM:")
# todo

print("- modules")
in1 = Dummy_input()
in2 = Dummy_input()
in3 = Dummy_input()

gate_or = Operand_OR()
gate_or.add_input(in1)
gate_or.add_input(in2)
gate_or.add_input(in3)

gate_and = Operand_AND()
gate_and.add_input(in1)
gate_and.add_input(in2)

byte8 = 255

for test in range(10000):
    #in8 = exp8.read()
    """
    exp8.write_8bit(set_bit(temp8,OUT4,0))
    sleep(0.1)
    exp8.write_8bit(set_bit(temp8,OUT4,1))
    sleep(0.001)
    """
    
    in8 = exp8.read()
    in1._value = int(get_bit(in8,0))
    in2._value = int(get_bit(in8,1))
    in3._value = int(get_bit(in8,2))
    """
    set_bit(byte8,0,in1._value)
    set_bit(byte8,1,in2._value)
    set_bit(byte8,2,in3._value)
    """
    print(byte8, in1.output, in2.output, in3.output, "->", gate_or.output, gate_and.output)
    exp8.write_8bit(set_bit(byte8,OUT1,int(not gate_or.output)))

    sleep(0.1)
