from components.plc.inputs.dummy import PLC_input_dummy
from components.plc.inputs.fixed import plc_input_fixed_high, plc_input_fixed_low
from components.plc.elements.rs import PLC_element_RS
from components.plc.elements.rs_pulse import PLC_element_RS_pulse
from components.plc.operands.op_and import PLC_operand_AND
from components.plc.operands.op_or import PLC_operand_OR
from components.plc.operands.op_not import PLC_operand_NOT

from utime import sleep


i1 = PLC_input_dummy(False)
i2 = PLC_input_dummy(False)

a1 = PLC_operand_AND([i1, plc_input_fixed_high])

o1 = PLC_operand_OR()
o1.add_input(i1)
o1.add_input(plc_input_fixed_high)

n1 = PLC_operand_NOT(i1)

rs = PLC_element_RS(i1, i2)
rsp = PLC_element_RS_pulse(i1, plc_input_fixed_low)
rspn = PLC_element_RS_pulse(i1, PLC_operand_NOT(i1))


print("Init: ", rs.output)
i1.value = True
print("SET 1", rs.output)
i1.value = False
print("SET 0", rs.output)

i2.value = True
print("RESET 1", rs.output)

i2.value = False
print("RESET 0", rs.output)

i1.value = False
print("AND: ", a1.output)
print("OR: ", o1.output)
print("NOT: ", n1.output)

i1.value = True
print("AND: ", a1.output)
print("OR: ", o1.output)
print("NOT: ", n1.output)
print("RS Pulse {}".format(rsp.output))
print("RS Pulse {}".format(rsp.output))

print("RS Pulse N {}".format(rspn.output))
print("RS Pulse N {}".format(rspn.output))

for i in range(0, 20):
    if i > 10:
        i1.value = False

    print("RS Pulse ({}): RS: {} RSN: {}".format(i, rsp.output, rspn.output))
    sleep(1)
