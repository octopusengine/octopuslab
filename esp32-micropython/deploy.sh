#!/usr/bin/env bash
set -euo pipefail

# TODO documentation
# TODO check arguments

export AMPY_PORT="/dev/ttyUSB0"
export AMPY_BAUD=115200

echo "Please only execute in venv with ampy installed"
echo "Deploying to $AMPY_PORT"

read -p "Press enter to continue"

# kill potential blocking screen sessions
# this blocks the device TODO improve
#pkill -f "screen $USB_DEV"

ampy ls

ampy put boot.py
# ampy put ./octopus_robot_board.py

ampy mkdir pinouts || true
ampy put ./pinouts/olab_esp32_default.py pinouts/olab_esp32_default.py
ampy put ./pinouts/olab_esp8266_tickernator.py pinouts/olab_esp8266_tickernator.py
ampy put ./pinouts/olab_esp8266_big_display.py pinouts/olab_esp8266_big_display.py
ampy put ./pinouts/olab_esp32_robot_board1_v1.py pinouts/olab_esp32_robot_board1_v1.py
ampy put ./pinouts/olab_esp32_robot_board1.py pinouts/olab_esp32_robot_board1.py
ampy put ./pinouts/olab_esp32_iot_board1.py pinouts/olab_esp32_iot_board1.py

ampy mkdir lib || true
ampy put ./lib/ssd1306.py lib/ssd1306.py
ampy put ./lib/temperature.py lib/temperature.py
ampy put ./lib/max7219.py lib/max7219.py
ampy put ./lib/max7219_8digit.py lib/max7219_8digit.py
ampy put ./lib/sm28byj48.py lib/sm28byj48.py
# ampy put ./lib/microWebSrv.py lib/microWebSrv.py
# ampy put ./lib/microWebSocket.py  lib/microWebSocket.py

ampy mkdir config || true
[ -e "config/device.json" ] && ampy put ./config/device.json config/device.json

ampy mkdir util || true
ampy put ./util/setup.py util/setup.py
ampy put ./util/pinout.py util/pinout.py
ampy put ./util/octopus.py util/octopus.py
ampy put ./util/wifi_connect.py util/wifi_connect.py

ampy mkdir util/led || true
ampy put ./util/led/__init__.py util/led/__init__.py

ampy mkdir util/buzzer || true
ampy put ./util/buzzer/__init__.py util/buzzer/__init__.py
ampy put ./util/buzzer/melody.py util/buzzer/melody.py
ampy put ./util/buzzer/notes.py util/buzzer/notes.py

ampy mkdir wwwesp || true
ampy put ./wwwesp/index.html wwwesp/index.html
ampy put ./wwwesp/octopus-logo100.png wwwesp/octopus-logo100.png

ampy ls util

# if local file with wifi setting exists, push it
if [ -f 'config/wifi.json' ]; then
    echo "Deploying local config/wifi.json"
    ampy put config/wifi.json config/wifi.json
fi
