# this module is to setup your board throuhg REPL
# it's loaded in boot.py and provides function setup()
# user is questioned in interactive mode

#ampy -p /COM6 put util/octopus.py util/octopus.py
import uos
import ujson
import gc #mem_free

def octopus():
    print("      ,'''`.")
    print("     /      \ ")
    print("     |(@)(@)|")
    print("     )      (")
    print("    /,'))((`.\ ")
    print("   (( ((  )) ))")
    print("   )  \ `)(' / ( ")
    print()
    print("Hello, this basic octopusLAB example")
    print("(Press Ctrl+C to abort)")
    print()
    print("Step 1/1 - WiFi setting:")
    print()

    sel = input("select: ")
    print("your select: "+str(sel))
    gc.collect()
    print("mem_free: "+str(gc.mem_free()))
    print("all OK, press CTRL+D to soft reboot")
