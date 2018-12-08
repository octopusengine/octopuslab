echo Welcome to basic octopusLAB script for ESP32 - Micropython!
pause

REM --- TODO documentation
REM --- TODO check arguments

REM --> Setup your COM port
SET PORT=/COM6
echo your port is: %PORT%
echo "Please only execute in venv with ampy installed"


REM To skip the following commands, put "REM" before them:

ampy -p  %PORT% ls

ampy -p  %PORT% put boot.py

echo "boot prepare"
ampy put boot_prepare.py boot.py

echo "config:"
ampy -p  %PORT% mkdir config
ampy -p  %PORT% put ./config/device.json config/device.json

echo "Util:"
ampy -p  %PORT% mkdir util
ampy -p  %PORT% put ./util/setup.py util/setup.py
ampy -p  %PORT% put ./util/wifi_connect.py util/wifi_connect.py

echo "ok - start: setup() in Mircopython"




