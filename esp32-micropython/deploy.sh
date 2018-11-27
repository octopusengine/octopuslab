#!/usr/bin/env bash
set -euo pipefail

# TODO documentation
# TODO check arguments

export AMPY_PORT="/dev/ttyUSB0"
export AMPY_BAUD=115200

MAIN_SCRIPT="$1"
echo "Please only execute in venv with ampy installed"
echo "Deploying to $AMPY_PORT"

read -p "Press enter to continue"

# kill potential blocking screen sessions
# this blocks the device TODO improve
#pkill -f "screen $USB_DEV"

echo "Deploying config"
ampy put ./config
echo "Deploying lib"
ampy put ./lib
echo "Deploying util"
ampy put ./util
# TODO repeated execution is not updating content
ampy put ./util/setup.py util/setup.py
ampy put ./util/wifi_connect.py util/wifi_connect.py
echo "Deploying boot.py"
ampy put ./boot.py
echo "Deploying main script $MAIN_SCRIPT"
ampy put "$MAIN_SCRIPT" main.py

# if local file with wifi setting exists, push it
if [ -f 'config/wifi.json' ]; then
    echo "Deploying local config/wifi.json"
    ampy put config/wifi.json config/wifi.json
fi
