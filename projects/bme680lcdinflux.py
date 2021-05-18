import time
import bme680i
from utils.database.influxdb import InfluxDB


from utils.octopus_lib import w, printTitle # i2c_init
# i2c = i2c_init()
# i2c.scan() # > [39]

printTitle("i2c init")
from machine import Pin, I2C
scl = Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP)
sda = Pin(21,Pin.OPEN_DRAIN, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=400000)

printTitle("bme680i")
bme = bme680i.BME680_I2C(i2c)

printTitle("lcd init")
from lib.esp8266_i2c_lcd import I2cLcd
lcd = I2cLcd(i2c, 39, 2, 16)
lcd.putstr("octopusLab")

def influx_write(temp,humi,press,gas):
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    return influx.write(temp=temp,humi=humi,press=press,gas=gas)

printTitle("WiFi + influx")
w()
influx = InfluxDB.fromconfig()


printTitle("main loop")
while True:
    temp = bme.temperature
    humi = bme.humidity
    press = bme.pressure
    gas = bme.gas
    print(temp, humi, press, gas)
    print("influx write: ", influx_write(temp,humi,press,gas))
    lcd.move_to(0,0)

    lcd.putstr(str(round(temp,1))+chr(223)+"C | "+str(round(humi,1))+"%") 
    lcd.move_to(0,1)
    lcd.putstr("p:"+str(int(press))+"  g:"+str(gas)) 
    time.sleep(28)