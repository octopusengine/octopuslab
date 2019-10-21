from pinouts import const
from pinouts.base import Base


class WemosESP32WOled(Base):
    #I2C:
    I2C_SCL_PIN = const(4)
    I2C_SDA_PIN = const(5)

    def __str__(self):
        return "WeMos OLED"
