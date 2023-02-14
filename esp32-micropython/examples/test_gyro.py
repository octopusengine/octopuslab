# upip.install("micropython-mpu9250")

from time import sleep, sleep_ms, ticks_ms
from machine import Pin, I2C
import mpu6050

print("init")
i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
mpu= mpu6050.accel(i2c)

"""
vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
"""

print("start")
t0 = ticks_ms

for i in range(1000):
   mpu.get_values()
   vals = mpu.get_values()
   print(vals["AcX"],vals["AcY"],vals["AcZ"])
   sleep_ms(50)
   
print("stop", ticks_ms - t0)
