print("--- octopusLAB: led_test ---")

print("-> init")

from components.analog import Analog
an2 = Analog(33)

print("-> get_adc_aver() value:")
data =  an2.get_adc_aver(8)
print(data)

print("-"*30)
