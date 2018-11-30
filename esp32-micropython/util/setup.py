# this module is to setup your board throuhg REPL
# it's loaded in boot.py and provides function setup()
# user is questioned in interactive mode

#TODO DRY for filename
import uos
import ujson

def setup():
    print("Hello this will help you initialize your ESP")
    print("Press Ctrl+C to abort")
    print()

    # TODO improve this
    # prepare directory
    if 'config' not in uos.listdir():
        uos.makedirs('config')

    print("Step 1/2 - Device setting:")
    print()
    dc = {}
    dc['board_type'] = input("Board type ('oLAB RobotBoard1' or 'oLAB IoTBoard1'): ")
    dc['soc_type'] = input("SoC type ('esp32' or 'esp8266'): ")

    print("Writing to file config/device.json")
    with open('config/device.json', 'w') as f:
        ujson.dump(dc, f)
        # ujson.dump(wc, f, ensure_ascii=False, indent=4)
    print()

    print("Step 2/2 - WiFi setting:")
    print()
    wc = {}
    wc['wifi_ssid'] = input("SSID: ")
    wc['wifi_pass'] = input("PASSWORD: ")

    # TODO improve this
    if 'config' not in uos.listdir():
        uos.makedirs('config')

    print("Writing to file config/wifi.json")
    with open('config/wifi.json', 'w') as f:
        ujson.dump(wc, f)
        # ujson.dump(wc, f, ensure_ascii=False, indent=4)
    print()
    
    print("all OK, press CTRL+D to soft reboot")
