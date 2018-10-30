"""
This is first basic test ESP32 UART2 - serial
needs Serial display TFT 320x240 with Arduino

Installation:
ampy -p /COM6 put ./octopus_robot_board.py
ampy -p /COM6 put ./05-serial-display.py main.py
# reset device
"""

from machine import UART
from machine import Pin
from time import sleep

import octopus_robot_board as o #octopusLab main library - "o" < octopus

uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
uart.write('C')      #test quick clear display

led = Pin(o.BUILT_IN_LED, Pin.OUT)
for _ in range(3):
    led.value(0)
    sleep(1/2)
    led.value(1)
    sleep(1/2)

uart.write('C')    #clear

uart.write('W7')   #change color
uart.write('h30')  #horizontal line
uart.write('h230') #horizontal line

uart.write('R0')
uart.write('W2')   #color
uart.write('QoctopusLAB - UART2 test*')
sleep(1/10)
uart.write('R2')
uart.write('W1')   #color
uart.write('QESP32 & ROBOTboard*')
sleep(1/10)

uart.write('R5')
uart.write('W2')   #color

num=9
for i in range(num):
    uart.write('Q')
    uart.write(str(num-i-1))
    uart.write('*')
    sleep(1/2)
