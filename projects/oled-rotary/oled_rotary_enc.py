# octopusLAB - rotary encoder example with oled display

from time import sleep_ms
from util.octopus import button_init, button, oled_init
from util.rotary_encoder.rotary_irq import RotaryIRQ

print("simple test: rotary encoder and oled display")
oled = oled_init()
oled.clear()
oled.text("octopusLAB 2019", 3, 1)
oled.show()

#               ROBOTboard
ROT_SW = 13   # MOTOR_34EN
ROT_DT = 25   # MOTOR_12EN
ROT_CLK = 26  # MOTOR_1A

sw = button_init(ROT_SW)
# button(sw)[0] > 9

rot = RotaryIRQ(pin_num_clk=ROT_CLK, pin_num_dt=ROT_DT, min_val=0, max_val=5, reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)

lastval = rot.value()
while True:
    val = rot.value()
    
    if lastval != val:
        lastval = val
        print('result =', str(val))
        oled.text(str(val), 3, 20)
        oled.show()

    if button(sw)[0] > 9:
        print("button pressed")

    sleep_ms(20)