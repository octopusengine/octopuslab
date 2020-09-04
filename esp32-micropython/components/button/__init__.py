#https://github.com/basecue/micropython-button

from _thread import start_new_thread
from machine import Pin, Timer
import time

__version__ = "2.0.1"


def _call_callbacks(callbacks):
    for callback in callbacks:
        callback()


class Button:
    debounce_time_ms = 10

    def __init__(self, pin, release_value=0, long_press_ms=1000):
        self._long_press_ms = long_press_ms
        self._on_long_press_callbacks = []
        self._on_press_callbacks = []
        self._on_release_callbacks = []
        self._pressed_at = None
        self.pin = pin
        self._original_value = release_value
        self._release_value = release_value
        self._register_irq()

    def _register_irq(self):
        if self._original_value == 1:
            waiting_for_irq = Pin.IRQ_FALLING
        else:
            waiting_for_irq = Pin.IRQ_RISING

        self.pin.irq(
            trigger=waiting_for_irq,
            handler=self._irq,
        )

    def _irq(self, pin):
        if pin.value() == self._original_value:
            return

        pin.irq(trigger=0)
        start_new_thread(self._debounce, tuple())

    def _debounce(self):
        time.sleep_ms(Button.debounce_time_ms)
        value = self.pin.value()
        callback = None
        if value != self._original_value:
            if value == self._release_value:
                callback = self._on_release_callback
            else:
                callback = self._on_press_callback
            self._original_value = value

        self._register_irq()

        if callback is not None:
            callback()

    def _on_press_callback(self):
        if self._pressed_at is None:
            start_thread = True
        else:
            start_thread = False
        self._pressed_at = time.ticks_ms()
        if start_thread:
            start_new_thread(self._wait_for_long_press, tuple())

        _call_callbacks(self._on_press_callbacks)

    def _wait_for_long_press(self):
        while self._pressed_at:
            if time.ticks_diff(time.ticks_ms(), self._pressed_at) > self._long_press_ms:
                if self._pressed_at is None:
                    return
                self._pressed_at = None
                _call_callbacks(self._on_long_press_callbacks)

    def _on_release_callback(self):
        self._pressed_at = None
        _call_callbacks(self._on_release_callbacks)

    def on_press(self, callback):
        self._on_press_callbacks.append(callback)
        return callback

    def on_release(self, callback):
        self._on_release_callbacks.append(callback)
        return callback

    def on_long_press(self, callback):
        self._on_long_press_callbacks.append(callback)
        return callback