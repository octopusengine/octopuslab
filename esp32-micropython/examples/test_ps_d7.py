from time import sleep
from os import urandom
import pubsub # /lib
import octopus.ps_disp7
   

print("start ps_random")

while True:
    value =  int(urandom(1)[0])
    print("rnd.: ", value)
    pubsub.publish('d7_text', value)
    sleep(1)
