# upip.install("micropython-mpu9250")

from time import sleep, sleep_ms, ticks_ms
from machine import Pin, I2C
from mpu6500 import MPU6500
from neopixel import NeoPixel
from max1704x import MAX1704x


class StatusLed(NeoPixel):
    _last_state = (0,0,0)

    def show_led(self, color, force=False):
        if self._last_state == color and not force:
            return

        self.fill(color)
        self.write()
        self._last_state = color
        print("Write new color ({},{},{})".format(color[0],color[1],color[2]))

print ('ws init')
led = StatusLed(Pin(8), 1)

print("i2c init")
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

print ('Init MAX gauge')
m = MAX1704x(i2c)

mpu = None
while not mpu:
    try:
        led.show_led((20,20,0))
        sleep_ms(250)
        mpu = MPU6500(i2c)
    except Exception as e:
        led.show_led((20,0,0))
        sleep(1)
        print(e)

led.show_led((20,0,20))
sleep_ms(250)

print("start")
led.show_led((0,20,0))


while True:
   gyro = mpu.gyro
   accel = mpu.acceleration
   #print(gyro[0],gyro[1],gyro[2], accel[0], accel[1], accel[2])
   #print("VBAT:{} VCELL:{} GX:{} GY:{} GZ:{}".format(m.soc, m.vcell, gyro[0],gyro[1],gyro[2]))
   #if accel[2] < 0:
   #    led.show_led((20,0,0))
   #else:
   #    led.show_led((0,0,20))
   led.show_led((int(abs(gyro[0]*5)),
                 int(abs(gyro[1]*5)),
                 int(abs(gyro[2]*5))))
   sleep_ms(15)

