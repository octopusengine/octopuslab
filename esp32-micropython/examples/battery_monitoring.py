# octopusLAB simple example 
# ESP32board + wifi -> analog 36, 39, ...

from util.analog import Analog
octopus()       # include main library

anIn = Analog(36) #analog input

def sendValue(value = 0,urlPOST = "http://www.octopusengine.org/iot17/add18.php"):
    from urequests import post
    header = {}
    header["Content-Type"] = "application/x-www-form-urlencoded"
    deviceID = Env.uID
    place = "octoPy32"
    # value =  int(float(Env.ver)*100)
    try:
        postdata_v = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, value,"batRaw")
        res = post(urlPOST, data=postdata_v, headers=header)
        sleep_ms(100)
        print("sendValue.ok")
    except:
        print("E.sendValue")

print('Start >')
led.value(1)
w()
led.value(0)

sleep(3)
print('Battery monitoring')

#sleep for 10 seconds (10000 milliseconds)
#machine.deepsleep(10000)
ii = 0
while True:
    valRaw = anIn.get_adc_aver()
    valPrint = str(ii)+ ": "+str(valRaw)
    print(valPrint)

    if ii%100 == 0:
        sendValue(valRaw)

    ii += 1
    sleep(6)



