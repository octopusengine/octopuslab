try:
    from micropython import const
except ModuleNotFoundError:
    def const(value):
        return value


class Pinout:
    board_pinouts={
        "esp32": {
            "oLAB Default":        { "class": "OlabESP32Default",       "module": "olab_esp32_default" },
            "oLAB ESP32board1":    { "class": "OlabESP32ESP32Board1",   "module": "olab_esp32_esp32_board1" },
            "oLAB RobotBoard1":    { "class": "OlabESP32RobotBoard1",   "module": "olab_esp32_robot_board1" },
            "oLAB RobotBoard1 v1": { "class": "OlabESP32RobotBoard1v1", "module": "olab_esp32_robot_board1v1" },
            "oLAB IoTBoard1":      { "class": "OlabESP32IoTBoard1",     "module": "olab_esp32_iot_board1" },
            "oLAB LANboard1":      { "class": "OlabESP32LANBoard1",     "module": "olab_esp32_lan_board1" },
            "WeMos OLED":          { "class": "WemosESP32WOled",        "module": "wemos_esp32_w_oled" }
        },
        "esp8266": {
            "oLAB Witty":       { "class": "OlabESP8266Witty",       "module": "olab_esp8266_witty" },
            "oLAB Tickernator": { "class": "OlabESP8266Tickernator", "module": "olab_esp8266_tickernator" },
            "oLAB BigDisplay3": { "class": "OlabESP8266BigDisplay",  "module": "olab_esp8266_big_display" },
            "oLAB IoTBoard1":   { "class": "OlabESP8266IoTBoard1",   "module": "olab_esp8266_iot_board1" },
        }
    }

    def getPinout(platform, board):
        try:
            boarddef = Pinout.board_pinouts[platform][board]
        except KeyError:
            raise AttributeError("Error: Unknown pinouts for Platform: {0} and board {1}".format(platform, board))

        try:
            module = __import__('pinouts.{0}'.format(boarddef["module"]), fromlist=[boarddef["class"]])
            cl = getattr(module, boarddef["class"])()
            return cl
        except Exception as e:
            print(e)

    def set_pinout():
        print("Deprecated, use getPinout()")
