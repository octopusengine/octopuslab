from time import sleep_ms

def blink(pin_obj, length_on=1000, length_off=1000):
    if pin_obj is None:
        return

    if length_off == 1000 and length_on != 1000:
        length_off = length_on

    pin_obj.value(1)
    sleep_ms(length_on)
    pin_obj.value(0)
    sleep_ms(length_off)

def ledvalue(pin_obj, value):
    if pin_obj is None:
        return

    pin_obj.value(value)
