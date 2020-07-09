# this module is to setup your board
# iotBoard for project parallel garden
#

__version__ = "1.0.3"


#import machine, time, os, ubinascii, framebuf, gc

# ---------------- procedures
def getOctopusLibVer():
    return "octopus lib.ver: " + __version__ + " / 2020-07-09"


def printTitle(t,num = 25):
    print()
    print('=' * num)
    print(t.center(num))
    print('=' * num)


def printLog(i = 1,s = ""):
    print()
    print('-' * 35)
    print("[--- " + str(i) + " ---] " + s)


def printFree():
    import gc
    print("Free: "+str(gc.mem_free()))


def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)


def add0(sn): # 1 > 01
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str


#def get_eui():
#    id = ubinascii.hexlify(machine.unique_id()).decode()
#    return id #mac2eui(id)


def getUid(short = False): # full or short (5 chars: first 2 + last 3)
    import machine, ubinascii
    id = ubinascii.hexlify(machine.unique_id()).decode()
    if short:
        return id[:2]+id[-3:]
    else:
        return id


def get_hhmm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm


def get_hh_mm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+"-"+mm
#-----------------------------------


def spi_init():
    from machine import Pin, SPI
    from utils.pinout import set_pinout
    pinout = set_pinout()
    spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
    return spi


def i2c_init(HWorSW=0,freq=100000):
    from machine import Pin, I2C
    from utils.pinout import set_pinout
    pinout = set_pinout()
    # i = I2C(scl=Pin(22), sda=Pin(21), freq=f)
    # HW or SW: HW 0 - | SW -1
    i2c = I2C(HWorSW, scl=Pin(pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=freq)
    return i2c