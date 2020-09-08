# simple basic example - ESP32 - Micropython - EDU_KIT1
# ROBOTboard with "BUILT_IN_LED", "WS RGB_LED" and "disp7"

from time import sleep

print("-"*30)
print("ESP32 + Mictopython | main-voltmeter.py")
print("-"*30)

from utils.octopus import disp7_init
d7 = disp7_init()

from components.analog import Analog
an36 = Analog(36)

k = 1.32/1423
while True:
    anRAW = an36.get_adc_aver()
    anV = round(anRAW*k,2)
    print(anRAW,anV)
    d7.show(anV)
    sleep(0.5)
