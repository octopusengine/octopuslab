from pca9685.servo import Servos
from util.octopus import i2c_init

i2c = i2c_init(1)
servo = Servos(i2c)

servo.position(0,50)
servo.position(1,50)

