from time import sleep

print("--- examples/test_shield.py ---")
print("-"*30)
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

print("--- Button ---")
from components.button import Button
btn_L = Button(34, release_value=1)
btn_R = Button(35, release_value=1)

@btn_L.on_press
def on_press_L_button():
    print("on_press_L_button")
    piezzo.beep()
    l2.toggle()

@btn_R.on_press
def on_press_R_button():
    print("on_press_R_button")
    piezzo.beep()
    l3.toggle()

print("--- ok ---")

from components.buzzer.melody import jingle1
piezzo.play_melody(jingle1)
l2.blink()
l3.blink()
oled.poweroff()
print("-"*30)

