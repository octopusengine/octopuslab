# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

def setup():
    import utils.setup
    utils.setup.setup()

def octopus():
    import utils.octopus
    utils.octopus.octopus()
    return utils.octopus

def reset():
    from machine import reset
    reset()

def shell():
    import shell
    shell.shell()

try:
    print("auto start from: config/boot.json")
    from config import Config
    autostart = Config("boot")

    if autostart.get("connect_wifi"):
        from utils.octopus import w
        w()

    if autostart.get("start_web_server"):
        from utils.octopus import web_server
        web_server()

except:
    print("Autostart Err.")

# when user enters REPL and executes setup()
