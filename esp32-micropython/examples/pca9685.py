# octopusLAB - simple test for gimbal two servos

from pca9685.servo import Servos
from utils.octopus import i2c_init
from time import sleep_ms
from utils.transform import * # include all - only for example


# blocking - simple test
def sweep(s, start, stop, delay=5, step=1):
   ang = start
   servo.position(s, ang)
   sleep_ms(delay)

   if start < stop:
      print("a")
      while ang < stop:
         ang = ang + step
         servo.position(s, ang)
         sleep_ms(delay)

   if start > stop:
      print("b")
      while ang > stop:
         ang = ang - step
         servo.position(s, ang)
         sleep_ms(delay)


i2c = i2c_init(1)
servo = Servos(i2c)

def sweeptest():
    sweep(0,30,160)
    sweep(1,30,180)
    sweep(0,160,30)
    sweep(1,180,30)
    
sweeptest()


