# octopusLab "decorators" lib


def octopus_debug(fnc):
    print("--- decorator --- @octopus_debug:")
    import time
    
    def ff(*args, **kwargs):
        start = time.time()
        result = fnc(*args, **kwargs)
        end = time.time() - start

        print("=== function name: ", str(fnc.__name__))
        print("=== duration (sec.) --->", str(end))
        return result

    return ff
