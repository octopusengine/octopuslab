# octopusLab "decorators" lib

def octopus_debug(fnc):
    print()
    print("--- decorator --- @octopus_debug:")
    import time
    
    def ff(*args, **kwargs):
        start = time.time()
        result = fnc(*args, **kwargs)
        end = time.time() - start
        try:
           fname = fnc.__name__
        except:
           fname = "?"
        print("=== function name: ", fname)
        print("=== duration (sec.) --->", str(end))
        return result

    return ff


def octopus_led_on(fnc):
    print()
    print("--- decorator --- @octopus_led_on:")
    import time
    from components import Led
    led = Led(2)
    
    def ff(*args, **kwargs):
        led.value(1)
        start = time.time()
        result = fnc(*args, **kwargs)
        end = time.time() - start
        led.value(0)
        try:
           fname = fnc.__name__
        except:
           fname = "?"
        print("=== function name: ", fname)
        print("=== duration (sec.) --->", str(end))
        return result

    return ff
