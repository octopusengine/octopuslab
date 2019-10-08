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

def reset():
    import machine
    machine.reset()


# when user enters REPL and executes setup()

