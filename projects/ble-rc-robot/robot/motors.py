from machine import PWM, Pin


class Motor:
    def __init__(self, pin_1, pin_2, pin_3):
        # TODO add corrections
        self._pin_1 = Pin(pin_1, Pin.OUT)
        self._pin_2 = Pin(pin_2, Pin.OUT)
        self._pin_3 = Pin(pin_3, Pin.OUT)
        self._pin_3_pwm = None

    def _init(self):
        if self._pin_3_pwm is None:
            self._pin_3_pwm = PWM(self._pin_3, freq=500, duty=0)

    def speed(self, value):
        self._init()
        forward = value >= 0
        self._pin_1.value(forward)
        self._pin_2.value(not forward)
        self._pin_3_pwm.duty(abs(value))
