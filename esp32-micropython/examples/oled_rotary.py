# octopusLAB - rotary encoder example with oled display

from time import sleep_ms
from utils.octopus import oled_init
from components.rotary_encoder.rotary_irq import RotaryIRQ
from components.button import Button

print("simple test: rotary encoder and oled display")
oled = oled_init()
oled.clear()
oled.text("octopusLAB 2020", 3, 1)
oled.show()

#               ROBOTboard
ROT_SW = 13   # MOTOR_34EN
ROT_DT = 25   # MOTOR_12EN
ROT_CLK = 26  # MOTOR_1A

#sw = button_init(ROT_SW)
rot_button = Button(ROT_SW, release_value=1)
rot = RotaryIRQ(pin_num_clk=ROT_CLK, pin_num_dt=ROT_DT, min_val=0, max_val=5, reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)

@rot_button.on_press
def on_press_button():
    global st
    print("btn")
    st  = 500
    oled.oledSegment(oled,st)

st = 500
lastval = rot.value()
while True:
    val = rot.value()

    if lastval != val:

        if lastval > val:
            st = st + 1
        else:
            st = st - 1
        lastval = val

        print('result =', str(val))
        oled.fill(0)
        oled.oledSegment(oled,st)
        # oled.text(str(st), 3, 20)
        oled.show()

        print(st)

    sleep_ms(20)
F