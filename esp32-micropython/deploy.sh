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
echo "Deploying boot.py and main.py"
ampy put ./boot.py
ampy put ./main.py
echo "Deploying all scripts"
ampy put ./01-blink.py
ampy put ./02-ws1-analog.py
ampy put ./02-ws1.py
ampy put ./04-hall.py
ampy put ./05-oled-analog.py
ampy put ./05-oled-graphics.py
ampy put ./05-oled-image.py
ampy put ./05-oled.py
ampy put ./05-oled_v2.py
ampy put ./05-serial-display.py
ampy put ./06-dcmotor.py
ampy put ./06-i2c-step.py
ampy put ./06-i2c-step1.py
ampy put ./06-i2c-step2.py
ampy put ./06-servo.py
ampy put ./06-servo2.py
ampy put ./07-i2c-test.py
ampy put ./08-blink-wifi.py
ampy put ./08-ws1-wifi.py
ampy put ./09-demo3.py
ampy put ./09-remote-wsled.py
ampy put ./09-remote-wsled-servo.py
ampy put ./09-scann-i2c-oled.py
ampy put ./09-temperature-oled.py
ampy put ./09-wwwesp.py


# if local file with wifi setting exists, push it
if [ -f 'config/wifi.json' ]; then
    echo "Deploying local config/wifi.json"
    ampy put config/wifi.json config/wifi.json
fi
