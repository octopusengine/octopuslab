from machine import ADC,Pin,I2C
from time import sleep_ms, sleep_us, ticks_ms
from math import sqrt
from PID import PID
from max6675 import MAX6675
from lib.esp8266_i2c_lcd import I2cLcd

# I2C
scl = Pin(16, Pin.OPEN_DRAIN, Pin.PULL_UP)
sda = Pin(2, Pin.OPEN_DRAIN, Pin.PULL_UP)

# Thermo K MAX6675
so = Pin(26, Pin.IN)
sck = Pin(32, Pin.OUT)
cs = Pin(33, Pin.OUT)

maxK = MAX6675(sck, cs, so)


i2c = I2C(1, scl=scl, sda=sda, freq=100000)
i2c_exp_addr=34
i2c_lcd_addr=39

lcd = I2cLcd(i2c, i2c_lcd_addr, 4, 16) # addr, rows, col

# ADC pin
temp_adc = ADC(Pin(35))

# Set ADC pin
settemp_adc = ADC(Pin(34))

# Range 50+ C
temp_adc.atten(ADC.ATTN_6DB)

# Range 0 - 3.3v
settemp_adc.atten(ADC.ATTN_11DB)

# Calibration points
# Reversed 4095 - adc value
# values for atten 6DB
adc_ohm_x=[1, 227, 393, 610, 947]
adc_ohm_y=[1202, 1384, 1505, 1681, 2000]

# Temperature range ADC vs Temp
adc_temp_x=[0, 4095]
adc_temp_y=[60, 250]


pid_val = 0
relayState = 0


def interp(x_arr, y_arr, x):
    for i, xi in enumerate(x_arr):
        if xi >= x:
            break
    else:
        return None

    if i == 0:
        return None

    x_min = x_arr[i-1]
    y_min = y_arr[i-1]
    y_max = y_arr[i]
    factor = (x - x_min) / (xi - x_min)

    return y_min + (y_max - y_min) * factor


def GetPlatinumRTD(Rt, R0):
   A=3.9083E-3
   B=-5.775E-7
 
   T = -R0 * A + sqrt(R0*R0 * A*A - 4*R0*B * (R0-Rt))
   T /= 2*R0*B
   return T


def aver(array):
    return sum(array)/len(array)


def mean(array):
    r = array.copy()
    r.remove(max(r))
    r.remove(min(r))
    return sum(r)/len(r)


def read_adc(pin, num=10, usdelay=10):
    readings = []
    for i in range(num):
        readings.append(pin.read())
        sleep_us(usdelay)

    return readings


def get_adc_aver(pin, num=10):
    r = read_adc(pin, num)
    return int(aver(r))


def get_adc_mean(pin, num=10):
    r = read_adc(pin, num)
    r.remove(max(r))
    r.remove(min(r))

    return int(mean(r))


def getPT1000temp(adc):
    r = read_adc(adc, 50)
    adc_raw = 4095-int(aver(r))
    adc_raw2 = 4095-int(mean(r))
    temp_r = interp(adc_ohm_x, adc_ohm_y, adc_raw)
    temp_r2 = interp(adc_ohm_x, adc_ohm_y, adc_raw2)
    return (round(GetPlatinumRTD(temp_r, 1000), 1),round(GetPlatinumRTD(temp_r2, 1000), 1)) if temp_r and temp_r2 else None


def getPIDvalue():
    t = getPT1000temp(temp_adc)
    return t[0] if t else 50
    #return maxK.read()


def setPIDvalue(value):
    global pid_val
    pid_val = value


def getRelayState(Output):
    global windowStartTime, relayState
    if ticks_ms() - windowStartTime > pid_windows_size:
        windowStartTime += pid_windows_size

    if Output < ticks_ms() - windowStartTime:
        relayState=0
        i2c.writeto(i2c_exp_addr, b'\xff')
    else:
        relayState=pid.set_point
        i2c.writeto(i2c_exp_addr, b'\x00')


def prepareLcd():
    try:
        lcd.clear()
        lcd.putstr("TempP: ")
        lcd.move_to(0, 1)
        lcd.putstr("TempA: ")
        lcd.move_to(0, 2)
        lcd.putstr("TempK: ")
        lcd.move_to(0, 3)
        lcd.putstr("P{p:<2}I{i:<2}D{d:<2}".format(p=0, i=0, d=0))
    except Exception as e:
        pass


def printLcd(tempP, tempA, tempK, p, i, d):
    try:
        lcd.move_to(7, 0)
        lcd.putstr("{tempP: <6} C".format(tempP=tempP))
        lcd.move_to(7, 1)
        lcd.putstr("{tempA: <6} C".format(tempA=tempA))
        lcd.move_to(7, 2)
        lcd.putstr("{tempK: <6} C".format(tempK=tempK))
        lcd.move_to(0, 3)
        lcd.putstr("P{p:<2}I{i:<2}D{d:<2}".format(p=p, i=i, d=d))
    except Exception as e:
        pass


windowStartTime = ticks_ms()

# Relay windows size in ms
pid_windows_size = 10000
pid_update_interval = 10

#pid = PID(getPIDvalue, setPIDvalue, 5., 0., 30)
pid = PID(getPIDvalue, setPIDvalue, 4., 0.03, -2.)
pid.set_point = 70

i = 0

prepareLcd()

while True:
    temp = getPT1000temp(temp_adc)
    tempK = maxK.read()
    tempPraw = get_adc_aver(settemp_adc)
    if tempPraw > 0:
        tempP = int(interp(adc_temp_x, adc_temp_y, tempPraw))
    else:
        tempP = 0
    pid.set_point = tempP

    ws = int(pid_val*pid_windows_size)
    if i > pid_update_interval:
        pid.update()
        i = 0

    getRelayState(ws)

    if temp is not None:
        printLcd(tempP, temp[0], tempK, int(pid.P_value), round(pid.I_value, 1), round(pid.D_value, 1))
        print("Temp({}):{} WS:{} P:{} I:{} D:{} R:{} TempK({}):{} Set:{}".format(temp[0], temp[0], ws/100, pid.P_value, pid.I_value, pid.D_value, relayState, tempK, tempK, tempP))
    else:
        printLcd(tempP, "N/A", tempK, round(pid.P_value, 1), round(pid.I_value, 1), round(pid.D_value, 1))
        print("Temp({}):{} WS:{} P:{} I:{} D:{} R:{} TempK({}):{} Set:{}".format(0, 0, ws/100, pid.P_value, pid.I_value, pid.D_value, relayState, tempK, tempK, tempP))
    sleep_ms(100)
    i+=1
