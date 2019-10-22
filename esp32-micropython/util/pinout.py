"""this module is to load proper pinout per config"""
from pinouts import Pinout
import json

def set_pinout():
    print("Deprecated warning: This method will be removed soon. Use pinouts.Pinout.getPinout instead.")
    try:
        import json
        with open('config/device.json', 'r') as f:
            d = f.read()
            f.close()
            device_config = json.loads(d)
    except:
        print("Device config 'config/device.json' does not exist, please run setup()")

    return Pinout.getPinout(device_config.get('soc_type'), device_config.get('board_type'))
