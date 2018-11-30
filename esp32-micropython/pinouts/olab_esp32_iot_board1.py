
from micropython import const

# PIN as on octopusLAB Wemos ESP32 IoTBoard1
BUILT_IN_LED = const(2)

#---esp32---
BUTT1_PIN = 12 #d6 x gpio16=d0
PIEZZO_PIN = const(27)  #14 //MOTOR_4A = const(27)
WS_LED_PIN = const(13) #v2+ > 15
ONE_WIRE_PIN = const(32)

#SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)

#I2C:
I2C_SCL_PIN = const(22)
I2C_SDA_PIN = const(21)


#PWM/servo:
PWM1_PIN = const(17)
PWM2_PIN = const(16)
PWM3_PIN = const(4)

HALL_SENSOR = const(8)
PIN_ANALOG = const(36)
#---------------------
