from pinouts import const
from pinouts.olab_esp32_robot_board1 import OlabESP32RobotBoard1

class OlabESP32RobotBoard1v1(OlabESP32RobotBoard1):
    WS_LED_PIN = const(13)   # Robot Board v1 - WS RGB ledi diode
    MOTOR_34EN = const(15)   # Robot Board v1

    def __str__(self):
        return "oLAB RobotBoard1 v1"
