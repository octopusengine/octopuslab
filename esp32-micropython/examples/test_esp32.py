print("--- octopusLAB: test_esp32 ---")

import esp32

def f2c(Fahrenheit):
    Celsius = (Fahrenheit - 32) * 5.0/9.0
    return Celsius

print("-> hall_sensor:")
mg = esp32.hall_sensor()
print(mg)

print("-> esp_temperature:")
raw_c = int(f2c(esp32.raw_temperature())*10)/10
print(str(raw_c)+"C")

print("-"*30)