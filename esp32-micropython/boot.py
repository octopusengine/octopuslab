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

# when user enters REPL and executes setup()
#from util.setup import setup
#from util.octopus import octopus #beta
