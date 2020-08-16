# octopusLAB - main.py - BLE and BlueFruit mobile app.
## uPyShell:~/$ run examples/ble/ble_pwm.py
# 8.6.2020

print("---> IoT light - PIR, Light, Temp")

from utils.octopus_lib import getUid
uID5 = getUid(short=5)

from time import sleep
from machine import Pin,PWM,Timer
from components.iot.pwm_fade import fade_in
from components.led import Led
from components.button import Button
from time import ticks_ms, ticks_diff
from components.analog import Analog
from components.iot import Thermometer
from utils.database.influxdb import InfluxDB
from utils.wifi_connect import WiFiConnect

print("init")
led_light = False
led = Led(2)
duty = 0
pir = 0
keep_alive = 0
light_treshold = 1500
led_button = Button(0, release_value=1)
anLight = Analog(36)
pwm = PWM(Pin(17, Pin.OUT), 500, duty) # PWM1
tt = Thermometer(32)
print("light", anLight.get_adc_aver(8))
print("temp.",tt.get_temp())

print("wifi")
net = WiFiConnect()
net.connect()

led.blink()
sleep(3)
led.blink()


min = 0
def timer60s():
    global min
    min += 1
    influx_write()
    print("--- ",min,ticks_ms())

influx = InfluxDB.fromconfig()

def influx_write():
    global pir, keep_alive
    light =  anLight.get_adc_aver(8)
    temp = tt.get_temp()
    try:
        print(influx.write(light=light,temperature=temp,pir_ch=pir,keep_alive=keep_alive),pir,keep_alive)
    except Exception as e:
        print("try influx write except: ",e)
    pir = 0
    keep_alive += 1


print("test influx")
influx_write()

t0 = Timer(0)
t0.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:timer60s())

p = Pin(16, Pin.IN)
sfa = ticks_ms()
while True:
    if p.value():
        son = ticks_ms()
        print(sfa,son,son-sfa)
        led.value(1)
        sleep(0.2)
        if son-sfa > 6000:
            print("fade_on")
            if anLight.get_adc_aver(8)<light_treshold:
                fade_in(pwm,600)
            sfa = ticks_ms()
            pir += 500
        duty = 600
        pwm.duty(duty)
        if anLight.get_adc_aver(8)<light_treshold:
            sleep(6)
        son = ticks_ms()
    else:
        led.value(0)
        sleep(0.2)
        duty = 0
    pwm.duty(duty)