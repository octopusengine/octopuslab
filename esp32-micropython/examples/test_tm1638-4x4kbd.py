# TM1638 kbd example

from time import sleep
from lib.tm1638 import TM1638
from machine import Pin
from utils.bits import neg, reverse, set_bit, get_bit
from utils.pinout import set_pinout
pinout = set_pinout() 

# right OCTOBUS SCI:
# STB = MOSI 23
# CLK = MISO 19
# DIO = SCLK 18

tm = TM1638(stb=Pin(pinout.SPI_MOSI_PIN), clk=Pin(pinout.SPI_MISO_PIN), dio=Pin(pinout.SPI_CLK_PIN))

# table1: matrix 4x4 - ABCD > K1 K2 K3 -
btn_tab = {1:'E',2:'8',4:'4',8:'123',16:'C',32:'7',64:'3',128:'123',512:'0',1024:'6',2048:'2',8192:'9',16384:'5',32768:'1'}

num = 0

def add_digit(dig):
   global num
   if dig >= 0:
     try:
        num = num*10 + (int(dig))
        rnum = num
     except:
        rnum = 0
   else:
      rnum = 0
   return rnum 


def format_digit(dig):
   return (8-len(str(dig)))*" "+str(dig) 

print("TM1638 matrix kbd example")

tm.show2("octopus ")
sleep(2)

while True:
    btn_read = tm.keys()
    if btn_read[0] > 0:  
       btn_val = btn_tab[btn_read[0]]
 
       print("btn_value: ", btn_val,num)
       sleep(0.3)
  
       if btn_val == "C": num  = add_digit(-1)
       if btn_val == "E": print("action: ", num)
       if btn_val != "C" and btn_val != "E":
           num = add_digit(int(btn_val))

    tm.show2(format_digit(num))
    sleep(0.1)
