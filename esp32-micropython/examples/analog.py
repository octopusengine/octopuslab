# octopusLAB simple exampple

from time import sleep
from components.analog import Analog
an2 = Analog(33) # DEV2


while True:
    data =  an2.get_adc_aver(8) # get average of 8 values
    print(data)
    sleep(5)