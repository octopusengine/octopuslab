# pub sub kbd+display example
# EDU_KIT1 + TM1638 shield


from time import sleep
import pubsub
from octopus import ps_tm

print("--- TM1638 - pubsub - example ---")

print("display test")
pubsub.publish('tm_display', "test 123")
sleep(2)
pubsub.publish('tm_display', "        ")


# table1: matrix 4x4 - ABCD > K1 K2 K3 -
btn_tab = {1:'E',2:'8',4:'4',8:'123',16:'C',32:'7',64:'3',128:'123',512:'0',1024:'6',2048:'2',8192:'9',16384:'5',32768:'1'}

num = 0

def add_digit(dig):
  global num
  try:
     num = num*10 + (int(dig))
     rnum = num
  except:
     rnum = 0
  return rnum 

def format_digit(dig):
  return (8-len(str(dig)))*" "+str(dig)


@pubsub.subscriber("tm_button")
def kbd_action(btn_value):
    global num
    print("btn_value: ", btn_value, btn_tab[btn_value],num)
    if btn_tab[btn_value] == "C":
        num = 0
        pubsub.publish('tm_display', "        ")
    if btn_tab[btn_value] == "E":
        print("action: ", num)
        pubsub.publish('tm_display', format_digit("E"))
        num = 0
    else:
        num = add_digit(btn_tab[btn_value])
        pubsub.publish('tm_display', format_digit(num))
    
    
    

