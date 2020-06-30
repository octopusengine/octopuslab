# this module is to setup your board
# iotBoard for project parallel garden
#

__version__ = "1.0.2"


#import machine, time, os, ubinascii, framebuf, gc

# ---------------- procedures
def getOctopusLibVer():
    return "octopus lib.ver: " + __version__ + " / 2020-06-30"


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


def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)


def get_hhmm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm


def get_hh_mm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+"-"+mm
