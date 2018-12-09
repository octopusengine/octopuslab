echo Welcome to basic octopusLAB script for ESP32 - Micropython!
pause

REM Setup your COM port
REM -------------------
SET PORT=/COM4
REM -------------------
echo your port is: %PORT%

REM To skip the following commands, put "REM" before them:

ampy -p  %PORT% ls

ampy -p  %PORT% put boot_prepare.py boot.py
REM ampy -p  %PORT% put ./octopus_robot_board.py

ampy -p  %PORT% mkdir pinouts
ampy -p  %PORT% put ./pinouts/olab_esp32_default.py pinouts/olab_esp32_default.py
ampy -p  %PORT% put ./pinouts/olab_esp8266_witty.py pinouts/olab_esp8266_witty.py
ampy -p  %PORT% put ./pinouts/olab_esp8266_tickernator.py pinouts/olab_esp8266_tickernator.py
ampy -p  %PORT% put ./pinouts/olab_esp8266_big_display.py pinouts/olab_esp8266_big_display.py


ampy -p  %PORT% mkdir lib
ampy -p  %PORT% put ./lib/ssd1306.py lib/ssd1306.py
ampy -p  %PORT% put ./lib/temperature.py lib/temperature.py
ampy -p  %PORT% put ./lib/max7219.py lib/max7219.py
ampy -p  %PORT% put ./lib/max7219_8digit.py lib/max7219_8digit.py
REM ampy -p  %PORT% put ./lib/sm28byj48.py lib/sm28byj48.py
REM ampy -p  %PORT% put ./lib/microWebSrv.py lib/microWebSrv.py
REM ampy -p  %PORT% put ./lib/microWebSocket.py  lib/microWebSocket.py

ampy -p  %PORT% mkdir config
ampy -p  %PORT% put ./config/device.json config/device.json

ampy -p  %PORT% mkdir util
ampy -p  %PORT% put ./util/setup.py util/setup.py
ampy -p  %PORT% put ./util/sys_info.py util/sys_info.py 
ampy -p  %PORT% put ./util/pinout.py util/pinout.py
ampy -p  %PORT% put ./util/octopus.py util/octopus.py
ampy -p  %PORT% put ./util/wifi_connect.py util/wifi_connect.py

ampy -p  %PORT% mkdir util/led
ampy -p  %PORT% put ./util/led/__init__.py util/led/__init__.py

ampy -p  %PORT% mkdir util/buzzer
ampy -p  %PORT% put ./util/buzzer/__init__.py util/buzzer/__init__.py
ampy -p  %PORT% put ./util/buzzer/melody.py util/buzzer/melody.py
ampy -p  %PORT% put ./util/buzzer/notes.py util/buzzer/notes.py

REM ampy -p  %PORT% mkdir wwwesp
REM ampy -p  %PORT% put ./wwwesp/index.html wwwesp/index.html
REM ampy -p  %PORT% put ./wwwesp/octopus-logo100.png wwwesp/octopus-logo100.png

ampy -p  %PORT% ls util
echo start:
echo >>> setup() / octopus()
