from machine import ADC,Pin,I2C
from time import sleep_ms, sleep_us, ticks_ms
from math import sqrt

scl = Pin(16, Pin.OPEN_DRAIN, Pin.PULL_UP)
sda = Pin(2, Pin.OPEN_DRAIN, Pin.PULL_UP)

i2c = I2C(1, scl=scl, sda=sda, freq=100000)

i2c_exp_addr=34

# ADC pin
temp_adc = ADC(Pin(35))

# Range 50+ C
temp_adc.atten(ADC.ATTN_6DB)

# Calibration points
# Reversed 4095 - adc value
# values for atten 6DB
adc_ohm_x=[1, 227, 393, 610, 947]
adc_ohm_y=[1202, 1384, 1505, 1681, 2000]


# Relay windows size in ms
pid_windows_size = 5000

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


def get_adc_aver(pin, num=10):
    sumAn = 0
    for i in range(num):
        an = pin.read()
        sumAn += an
        sleep_us(10)
    return int(sumAn/num)


def getPT1000temp(adc):
    adc_raw = 4095-get_adc_aver(adc, 50)
    temp_r = interp(adc_ohm_x, adc_ohm_y, adc_raw)
    return round(GetPlatinumRTD(temp_r, 1000), 1) if temp_r else None


def getPIDvalue():
    return getPT1000temp(temp_adc) or 50


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


windowStartTime = ticks_ms()

pid = PID(getPIDvalue, setPIDvalue, 5., 0.05, 1)
pid.set_point = 120

while True:
    temp = getPT1000temp(temp_adc)
    ws = int(pid_val*pid_windows_size)
    pid.update()
    getRelayState(ws)
    print("Temp:{} WS:{} P:{} I:{} D:{} R:{}".format(temp, ws/1000, pid.P_value, pid.I_value, pid.D_value, relayState))
    sleep_ms(100)
