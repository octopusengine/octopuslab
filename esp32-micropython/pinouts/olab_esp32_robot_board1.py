from pinouts import const
from pinouts.olab_esp32_default import OlabESP32Default


class OlabESP32RobotBoard1(OlabESP32Default):
    ##WS_LED_PIN 13          # Robot Board v1
    WS_LED_PIN = const(15)   # Robot Board v2 - WS RGB ledi diode
    ONE_WIRE_PIN = const(32)  #one wire (for Dallas temperature sensor)
    PIEZZO_PIN = const(27)

    # DC motors
    MOTOR_12EN = const(25)
    # Select version of robot board
    ##MOTOR_34EN 15          # Robot Board v1
    MOTOR_34EN = const(13)   # Robot Board v2
    MOTOR_1A = const(26)
    MOTOR_2A = const(12)
    MOTOR_3A = const(14)
    MOTOR_4A = const(27)

    #main analog input (for power management)
    ANALOG_PIN = const(36)

    #PWM/servo:
    PWM1_PIN = const(17)
    PWM2_PIN = const(16)
    PWM3_PIN = const(4)
    #pwm duty for servo:
    SERVO_MIN = const(38)
    SERVO_MAX= const(130)

    #inputs:
    I39_PIN = const(39)
    I34_PIN = const(34)
    I35_PIN = const(35)

    #temp
    MFET_PIN = const(17) # PWM1
    RELAY_PIN = const(16) # PWM2

    # DEV pins
    DEV1_PIN = const(32)
    DEV2_PIN = const(33)

    def __str__(self):
        return "oLAB RobotBoard1"
       