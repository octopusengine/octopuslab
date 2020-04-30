# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

def setup():
    import util.setup
    util.setup.setup()

def octopus():
    import util.octopus
    util.octopus.octopus()
    return util.octopus

def h():
    from util.octopus import o_help
    o_help()

def reset():
    from machine import reset
    reset()

def shell():
    import util.shell
    util.shell.shell()

try:
    print("auto start from: config/boot.json")
    from config import Config
    autostart = Config("boot")

    if autostart.get("connect_wifi"):
        from util.octopus import w
        w()

    if autostart.get("start_web_server"):
        from util.octopus import web_server
        web_server()

except:
    print("Autostart Err.")

# when user enters REPL and executes setup()

