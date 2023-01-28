def update(tar_url=None, config_url=None):
    import octopuslab_installer
    import sys
    from .network.shortcuts import network
    from .config import get_config
    config = get_config()

    if not network.is_connected():
        print('Connecting to wifi')
        network.connect()

    # update tar
    if tar_url is None:
        tar_url = config.get('update', {}).get('tar_url')
    if tar_url is None:
        print("Error update.tar_url not found in config")
    print("Downloading tar from", tar_url)
    octopuslab_installer.download(tar_url, "/lib/img/latest.tar")
    # update config
    if config_url is None:
        config_url = config.get('update', {}).get('config_url')
    if config_url is not None:
        print("Downloading config from", config_url)
        octopuslab_installer.download(config_url, "/lib/img/config.json")

    del octopuslab_installer
    del sys.modules['octopuslab_installer']
    reset()


def reset():
    import octopuslab_installer
    import sys
    octopuslab_installer.deploy("/lib/img/latest.tar")
    del octopuslab_installer
    del sys.modules['octopuslab_installer']
    reset_config()

def reset_config():
    import sensobox.config
    import sys
    sensobox.config.set_config_from_file('/lib/img/config.json')
    del sensobox.config
    del sys.modules['sensobox.config']


def setup():
    import utils.setup
    import sys
    utils.setup.setup()
    del utils.setup
    del sys.modules['utils.setup']


def status():
    import sys, gc
    gc.collect()
    print("free memory:", gc.mem_free())
    print("dir:")
    for i in dir():
        print("  - ", i)
    print("sys.modules:")
    for i in sys.modules:
        print("  - ", i)


def info():
    import binascii, machine, sys
    print("Machine ID:", binascii.hexlify(machine.unique_id()).decode())
    del binascii


