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
    print("Step 1/1 - WiFi setting:")
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
