# upip.install("micropython-mpu9250")

from time import sleep, sleep_ms, ticks_ms
from machine import Pin, I2C
from mpu6500 import MPU6500

print("init")
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
mpu = MPU6500(i2c)

print("start")
t0 = ticks_ms

for i in range(1000):
   gyro = mpu.gyro
   accel = mpu.acceleration
   print(gyro[0],gyro[1],gyro[2], accel[0], accel[1], accel[2])
   sleep_ms(50)
   
print("stop", ticks_ms - t0)
