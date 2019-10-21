# Default board, some basic interfaces like I2C, SPI and built-in led

from pinouts import const
from pinouts.olab_esp32_base import OlabESP32Base


class OlabESP32Default(OlabESP32Base):
    ANALOG_PIN = const(36)
    BUTT1_PIN = const(12)
    PIEZZO_PIN = const(14)
    WS_LED_PIN = const(15)
    ONE_WIRE_PIN = const(13)

    def platform(self):
        return "esp32"

    def __str__(self):
        return "oLAB Default"
