#!/usr/bin/env bash

# TODO documentation

[ -z "$AMPY_PORT" ] && export AMPY_PORT="/dev/ttyUSB0"
[ -z "$AMPY_BAUD" ] && export AMPY_BAUD=115200

set -euo pipefail

echo "Please only execute in venv with ampy installed"
echo "Deploying to $AMPY_PORT"

read -p "Press enter to continue"

# kill potential blocking screen sessions
# this blocks the device TODO improve
#pkill -f "screen $USB_DEV"

ampy ls

echo "boot"
ampy put boot.py boot.py

echo "Config dir"
ampy mkdir config 2> /dev/null || true
[ -e "config/device.json" ] && ampy put ./config/device.json config/device.json

echo "Util folder"
ampy mkdir util 2> /dev/null || true

echo "util/setup"
ampy put ./util/setup.py util/setup.py

echo "util/wifi_connect"
ampy put ./util/wifi_connect.py util/wifi_connect.py

echo "util/mqtt_connect"
ampy put ./util/mqtt_connect.py util/mqtt_connect.py

echo "util/mqtt"
ampy put ./util/mqtt.py util/mqtt.py

# if local file with wifi setting exists, push it
if [ -f 'config/wifi.json' ]; then
    echo "Deploying local config/wifi.json"
    ampy put config/wifi.json config/wifi.json
fi
