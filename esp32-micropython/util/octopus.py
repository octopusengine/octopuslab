# this module is to setup your board throuhg REPL
# it's loaded in boot.py and provides function setup()
# user is questioned in interactive mode

# ampy -p /COM6 put util/octopus.py util/octopus.py
import time
import uos
import ujson
import gc #mem_free
import machine, ubinascii
from machine import Pin, PWM, Timer

tim = Timer(-1)
led = Pin(2, Pin.OUT) # BUILT_IN_LED

#SPI_MOSI_PIN = const(23)
pwm0 = PWM(Pin(23)) # create PWM object from a pin
pwm0.duty(0)

def beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(200)   # set duty cycle
    time.sleep_ms(t)
    p.duty(0)
    #b.deinit()

def blink(t): # time sleep
    led.value(1)
    time.sleep_ms(t)
    led.value(0)
    time.sleep_ms(t)

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:]
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

#-------------
def octopus():
    beep(pwm0,500,100)
    tim.init(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print("test timer - delay"))
    #tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))

    print("      ,'''`.")
    print("     /      \ ")
    print("     |(@)(@)|")
    print("     )      (")
    print("    /,'))((`.\ ")
    print("   (( ((  )) ))")
    print("   )  \ `)(' / ( ")
    print()
    print("Hello, this is basic octopusLAB example (2018/11)")
    print("(Press Ctrl+C to abort)")
    print()

    time.sleep_us(10)       # sleep for 10 microseconds
    blink(500)
    time.sleep_ms(1000)     # 1s
    start = time.ticks_ms()

    print("-----")
    print("Menu: 1 setup WiFi | 2 basic test | 3 system info")
    print("-----")

    sel = input("select: ")
    #print("your select: "+str(sel))
    if sel == "1":
        print(">>> setup()")
    elif sel == "2":
        print("TODO)")
    elif sel == "3":
        print("> unique_id: "+str(get_eui()))
        #print("--- MAC: "+str(mac2eui(get_eui())))
        gc.collect()
        print("> mem_free: "+str(gc.mem_free()))
        print("> machine.freq: "+str(machine.freq()))

    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("> delta time: "+str(delta))
    beep(pwm0,2000,50)
    print("all OK, press CTRL+D to soft reboot")
    blink(50)
