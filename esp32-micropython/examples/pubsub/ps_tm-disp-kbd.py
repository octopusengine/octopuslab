from time import sleep
import pubsub
from octopus import ps_tm

print("--- TM1638 - pubsub - example ---")

print("display test")
pubsub.publish('tm_display', "test 123")
sleep(2)
pubsub.publish('tm_display', "        ")

print("kbd test")
@pubsub.subscriber("tm_button")
def kbd_action(btn_value):
    print("btn_value: ", btn_value)
    

