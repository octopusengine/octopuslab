#!/usr/bin/env bash
set -euo pipefail

# TODO documentation
# TODO check arguments

USB_DEV="/dev/ttyUSB0"
MAIN_SCRIPT="$1"
echo "Please only execute in venv with ampy installed"
echo "Deploying to $USB_DEV"

read -p "Press enter to continue"

# kill potential blocking screen sessions
# this blocks the device TODO improve
#pkill -f "screen $USB_DEV"

echo "Deploying config"
ampy -p $USB_DEV put ./config
echo "Deploying lib"
ampy -p $USB_DEV put ./lib
echo "Deploying util"
ampy -p $USB_DEV put ./util
# TODO repeated execution is not updating content
ampy -p $USB_DEV put ./util/setup.py util/setup.py
ampy -p $USB_DEV put ./util/wifi_connect.py util/wifi_connect.py
echo "Deploying boot.py"
ampy -p $USB_DEV put ./boot.py
echo "Deploying main script $MAIN_SCRIPT"
ampy -p $USB_DEV put "$MAIN_SCRIPT" main.py

# if local file with wifi setting exists, push it
if [ -f 'config/wifi.json' ]; then
    echo "Deploying local config/wifi.json"
    ampy -p $USB_DEV put config/wifi.json config/wifi.json
fi
