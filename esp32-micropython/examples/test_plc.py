from time import sleep
from machine import Timer
from utils.octopus_lib import i2c_init
from components.lm75 import LM75B
from components.i2c_expander import Expander8
from utils.bits import neg, reverse, int2bin, get_bit, set_bit

from components.plc.inputs.dummy import PLC_input_dummy
from components.plc.inputs.fixed import plc_input_fixed_high, plc_input_fixed_low
from components.plc.elements.rs import PLC_element_RS
from components.plc.operands.op_and import PLC_operand_AND
from components.plc.operands.op_or import PLC_operand_OR


IN1, IN2, IN3, IN4     = 0, 1, 2, 3
OUT1, OUT2, OUT3, OUT4 = 4, 5, 6, 7
# OUT4 - signalization

timer_counter = 0
periodic = False
tim1 = Timer(0)

byte8 = 255 # all leds off


def timer_init(per= 2000): # period 10 s (10000 ms)
    print("timer_init")
    print("timer tim1 is ready - periodic")
    print("for deactivite: tim1.deinit()")
    tim1.init(period=per, mode=Timer.PERIODIC, callback=lambda t:timer_action())

def timer_action():
    global timer_counter, periodic, byte8  
    print("timerAction " + str(timer_counter))
    timer_counter += 1
    periodic = not periodic
    byte8 = set_bit(byte8,OUT4,int(periodic)) 


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
in1 = PLC_input_dummy()
in2 = PLC_input_dummy()
in3 = PLC_input_dummy()

gate_or = PLC_operand_OR()
gate_or.add_input(in1)
gate_or.add_input(in2)
gate_or.add_input(in3)

gate_and = PLC_operand_AND()
gate_and.add_input(in1)
gate_and.add_input(in2)

rs = PLC_element_RS(in1, in2)


sleep(3)
# timer_init()


for test in range(10000):  
    in8 = exp8.read()
    in1._value = int(get_bit(in8,0))
    in2._value = int(get_bit(in8,1))
    in3._value = int(get_bit(in8,2))
        
    set_bit(byte8,OUT1,int(not gate_or.output))
    set_bit(byte8,OUT4,periodic)
    print(periodic, byte8, in1.output, in2.output, in3.output, "->", gate_or.output, gate_and.output)

    byte8 = set_bit(byte8,OUT1,not gate_or.output)
    byte8 = set_bit(byte8,OUT2,not gate_and.output)
    # byte8 = set_bit(byte8,OUT3,not in2._value)
    byte8 = set_bit(byte8,OUT3,not rs.output)
    exp8.write_8bit(byte8)

    sleep(0.05)
