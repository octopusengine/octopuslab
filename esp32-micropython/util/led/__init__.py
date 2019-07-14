from time import sleep_ms

def blink(pin, length_on=1000, length_off=1000):
    print("WARGNING: DEPRECATED: Do not USE, Use Led class instead!!")

    if pin is None:
        print("DUMMY_LED DEPRECATED: Blink")
        return

    if length_off == 1000 and length_on != 1000:
        length_off = length_on

    pin.value(1)
    sleep_ms(length_on)
    pin.value(0)
    sleep_ms(length_off)

def ledvalue(pin_obj, value):
    if pin_obj is None:
        return

    pin_obj.value(value)
