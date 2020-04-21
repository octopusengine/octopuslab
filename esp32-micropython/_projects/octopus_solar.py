import network
import urequests
import time
from machine import ADC, Pin, reset

post_url=""
post_data="solar,place=octopuslab,id=1 keepalive={0},solarVolt={1}"

print("Press CTRL+C to skip booting")
for _ in range(0,3):
    print(".")
    time.sleep(1)

net = network.WLAN()
net.active(1)

net.connect("", "")

keepalive=0
errorcount=0

def wait_connect():
    retry = 0
    print("Connecing")
    while not net.isconnected():
        print(".")
        retry += 1
        time.sleep(1)

        if retry > 30:
            break

def sendData(keepalive, solarRaw):
    global errorcount
    try:
        status = urequests.post(post_url, data=post_data.format(keepalive, solarRaw))
        print(status.status_code)
        status.close()
        errorcount = 0
    except Exception as e:
        print("Error no. {}".format(errorcount), e)
        errorcount+=1
        if errorcount > 4:
            machine.reset()
        else:
            net.disconnect()
            net.connect()
            wait_connect()


wait_connect()

solarVoltAdc = ADC(Pin(34))
solarVoltAdc.atten(ADC.ATTN_11DB)

while True:
    solarRaw = solarVoltAdc.read()

    sendData(keepalive, solarRaw)
    print("Solar RAW: {0}, freeMem: {1}".format(solarRaw, gc.mem_free()))
    gc.collect()
    time.sleep(30)
    keepalive+=1
