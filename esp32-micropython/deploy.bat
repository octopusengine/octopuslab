echo Welcome to basic octopusLAB script for ESP32 - Micropython!
pause

REM Setup your COM port
SET PORT=/COM6
echo your port is: %PORT%

REM To skip the following commands, put "REM" before them:

ampy -p  %PORT% put boot.py
ampy -p  %PORT% put ./octopus_robot_board.py

ampy -p  %PORT% mkdir lib
ampy -p  %PORT% put ./lib/ssd1306.py lib/ssd1306.py
ampy -p  %PORT% put ./lib/temperature.py lib/temperature.py
ampy -p  %PORT% put ./lib/max7219.py lib/max7219.py
ampy -p  %PORT% put ./lib/max7219_8digit.py lib/max7219_8digit.py

ampy -p  %PORT% put ./lib/microWebSrv.py lib/microWebSrv.py
ampy -p  %PORT% put ./lib/microWebSocket.py  lib/microWebSocket.py
ampy -p  %PORT% put ./lib/sm28byj48.py lib/sm28byj48.py

ampy -p  %PORT% mkdir wwwesp
ampy -p  %PORT% put ./wwwesp/index.html wwwesp/index.html
ampy -p  %PORT% put ./wwwesp/octopus-logo100.png wwwesp/octopus-logo100.png

ampy -p  %PORT% mkdir config
ampy -p  %PORT% mkdir util
ampy -p  %PORT% put ./util/setup.py util/setup.py
ampy -p  %PORT% put ./util/octopus.py util/octopus.py
ampy -p  %PORT% put ./util/wifi_connect.py util/wifi_connect.py
ampy -p  %PORT% ls util
echo start:
echo >>> octopus()
