from _thread import start_new_thread
from machine import Pin, Timer
import time

from micropython import schedule

__version__ = "2.0.0"

class Button:
    debounce_time_ms = 10

    def __init__(self, pin, release_value=0):
        self._on_press_callbacks = []
        self._on_release_callbacks = []
        self.pin = pin
        # TODO we assume now the button is not pressed during startup
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
        if value != self._original_value:
            if value == self._release_value:
                callback = self._on_release_callback
            else:
                callback = self._on_press_callback
            schedule(callback, None)
            self._original_value = value

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
