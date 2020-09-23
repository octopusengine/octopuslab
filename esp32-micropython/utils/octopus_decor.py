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
