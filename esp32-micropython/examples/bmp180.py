# MIT
# https://github.com/micropython-IMU/micropython-bmp180

from bmp180 import BMP180

octopus()

bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

temp = bmp180.temperature
p = bmp180.pressure
altitude = bmp180.altitude
print(temp, p, altitude)