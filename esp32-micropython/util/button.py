from machine import Pin, Timer
from micropython import schedule


class Button:
    debounce_time_ms = 10

    def __init__(self, pin_num: int, release_value=0):
        self._on_press_callbacks = []
        self._on_release_callbacks = []
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_DOWN)  # TODO pull
        self._debounce_timer = Timer(1)
        self._value = release_value
        self._release_value = release_value
        self._register_irq()

    def _register_irq(self):
        self.pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=self._irq,
        )

    def _irq(self, pin):
        value = pin.value()
        if value == self._value:
            return

        pin.irq(trigger=0)
        self._value = value
        self._debounce_timer.init(
            period=Button.debounce_time_ms,
            mode=Timer.ONE_SHOT,
            callback=self._debounce
        )

    def _debounce(self, _):
        if self.pin.value() == self._value:
            if self._value == self._release_value:
                callback = self._on_release_callback
            else:
                callback = self._on_press_callback
            schedule(callback, None)
        self._register_irq()

    def _on_press_callback(self, _):
        for callback in self._on_press_callbacks:
            callback()

    def _on_release_callback(self, _):
        for callback in self._on_release_callbacks:
            callback()

    def on_press(self, callback):
        self._on_press_callbacks.append(callback)
        return callback

    def on_release(self, callback):
        self._on_release_callbacks.append(callback)
        return callback
