# oled test - without octopusLIB
from time import sleep, sleep_ms
from utils.pinout import set_pinout
from components.display_segment import threeDigits 

pinout = set_pinout()     # set board pinout

def i2c_init(scan = False, freq=100000, HWorSW = 0, printInfo = True):
    from machine import Pin, I2C
    # HW or SW: HW 0 - | SW -1
    i2c = I2C(HWorSW, scl=Pin(pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=freq)
    if scan:
        print("i2c.scan() > devices:")
        # I2C address:
        OLED_ADDR = 0x3c
        LCD_ADDR = 0x27
        try:
            i2cdevs = i2c.scan()
            print(i2cdevs)
            if (OLED_ADDR in i2cdevs):
                if printInfo: print("ok > OLED: "+str(OLED_ADDR))
        except Exception as e:
            print("Exception: {0}".format(e))

    return i2c


def oled_init(ox=128, oy=64, runTest = True):
    from components.oled import Oled
    from components.display_segment import threeDigits
    sleep_ms(1000)

    i2c = i2c_init(scan = True)
    oled = Oled(i2c, 0x3c, ox, oy)
    return oled


print("--- oled_init() ---")

oled = oled_init()

print("--- oled.test() ---")
oled.test()
threeDigits(oled,123)
