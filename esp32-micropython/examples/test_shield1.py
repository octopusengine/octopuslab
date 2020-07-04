from time import sleep

print("--- Led2 | Led3 ---")
from components.led import Led
l2 = Led(25)
l3 = Led(27)

l2.blink()
l3.blink()

print("--- buzzer ---")
from components.buzzer import Buzzer
piezzo = Buzzer(15)
piezzo.beep()
sleep(0.5)
piezzo.beep()

print("--- OLED ---")
from utils.octopus import oled_init
oled = oled_init()

print("--- ok ---")

from components.buzzer.melody import jingle1
piezzo.play_melody[jingle1]
l2.blink()
l3.blink()
oled.poweroff()

