# simple example with sensor bmp280
# import examples.bmp280
# from examples.bmp280 import bmp_init

def bmp_init():
   from util.octopus import i2c_init
   # "-1" > SW for old lib:
   i2c = i2c_init(1,100000,-1)

   from bmp280 import BMP280

   bmp = BMP280(i2c)
   return bmp

bmp = bmp_init()
# bmp.oversample_sett = 2
# bmp.baseline = 101325

temp = bmp.temperature
p = bmp.pressure
# altitude = bmp.altitude
print("temperature: ", temp)
print("pressure: " , p)