# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

def setup():
    import utils.setup
    utils.setup.setup()

def octopus():
    from utils.octopus import *
    octopus()

import builtins
builtins.octopus=octopus

def octopus_demo():
    import utils.octopus_demo
    utils.octopus_demo.octopus_demo()

def reset():
    import machine
    machine.reset()


# when user enters REPL and executes setup()

