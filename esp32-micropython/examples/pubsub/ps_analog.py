from time import sleep

from pubsub import PubSub

pubsub = PubSub(100)
pubsub.start()

from util.analog import Analog
an2 = Analog(33)


while True:
    value =  an2.get_adc_aver(8)
    print(value)
    pubsub.publish('value', value) 
    sleep(5)
