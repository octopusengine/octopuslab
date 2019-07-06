# this module is to setup your board throuhg REPL
# it's loaded in boot.py and provides function setup()
# user is questioned in interactive mode

#TODO DRY for filename
import time, uos
import ujson
import machine #datetime

ver = "0.61 / 5.7.2019"

devices = [
["oLAB Default","esp32"],
["oLAB Witty","esp8266"],
["oLAB Tickernator","esp8266"],
["oLAB BigDisplay3","esp8266"],
["oLAB RobotBoard1 v1","esp32"],
["oLAB RobotBoard1","esp32"],
["oLAB IoTBoard1","esp8266"],
["oLAB IoTBoard1","esp32"]
]

octopuASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   )  \ `)(' / ( ",
]

def mainOctopus():
    for ol in octopuASCII:
        print(str(ol))
    print()

def deploy(url):
    import sys
    import os
    import lib.shutil as shutil
    import upip_utarfile as utarfile
    import urequests

    res = urequests.get(url)

    if not res.status_code == 200:
        return

    def dir_exists(path):
        try:
            os.stat(path)
            return True
        except:
            return False

    t = utarfile.TarFile(fileobj = res.raw)

    for f in t:
        print("Extracting {}: {}".format(f.type, f.name))
        if f.type == utarfile.DIRTYPE:
            if f.name[-1:] == '/':
                name = f.name[:-1]
            else:
                name = f.name

            if not dir_exists(name):
                os.mkdir(name)
        else:
            extracted = t.extractfile(f)
            shutil.copyfileobj(extracted, open(f.name, "wb"))

def setupMenu():
    print()
    print('=' * 30)
    print('        S E T U P')
    print('=' * 30)
    print("[w]   - wifi submenu")
    print("[cw]  - connect wifi")
    print("[sdp] - system download > petrkr (update octopus modules from URL)")
    print("[sdo] - system download > octopus (update octopus modules from URL)")
    print("[ds]  - device setting")
    print("[ios] - I/O setting submenu")
    print("[iot] - I/O test - run io_test()")
    print("[mq]  - mqtt() and sending data setup")
    print("[st]  - set time")
    print("[si]  - system info")
    print("[wr]  - run web repl")
    print("[od]  - run octopus() demo")
    print("[x]   - exit setup")

    print('=' * 30)
    sel = input("select: ")
    return sel

def wifiMenu():
    print()
    print('=' * 30)
    print('        S E T U P - W I F I')
    print('=' * 30)
    print("[a]  - Add wifi network")
    print("[r]  - Remove wifi network")
    print("[s]  - Show configuration")

    print('=' * 30)
    sel = input("select: ")
    return sel

def ioMenu():
    from util.io_config import io_conf_file, io_menu_layout, get_from_file as get_io_config_from_file
    while True:
        # read current settings from json to config object
        io_conf = get_io_config_from_file()

        print()
        print('=' * 50)
        print('        S E T U P - I / O    (interfaces)')
        print('=' * 50)
        # show options with current values
        c = 0
        for i in io_menu_layout:
            c += 1
            print("[%2d] - %8s [%s] - %s" % (c, i['attr'], io_conf.get(i['attr'], 0), i['descr']))
        print("[x]  - Exit from I/O setup")

        print('=' * 50)
        sele = input("select: ")

        if sele == "x":
            # done with editing
            break

        try:
            sele = int(sele)
        except ValueError:
            print("Invalid input, try again.")

        # change selected item if integer
        if sele > 0 and sele <= len(io_menu_layout):
            # print attribute name and description
            print()
            # print current value
            try:
                new_val = int(input("New Value [%s]: " % io_conf.get(io_menu_layout[sele - 1]['attr'], 0)))
            except ValueError:
                # if invalid input, 0 is inserted
                new_val = 0
            # update config object
            io_conf[io_menu_layout[sele - 1]['attr']] = new_val
            # dump updated setting into json
            print("Writing new config to file %s" % io_conf_file)
            with open(io_conf_file, 'w') as f:
                ujson.dump(io_conf, f)
        else:
            print("Invalid input, try again.")

def shutil():
    print("System download > (initial octopus modules)")
    import upip
    print("Installing shutil")
    upip.install("micropython-shutil")
    print("Running deploy")

def setup():
    mainOctopus()
    print("Hello, this will help you initialize your ESP")
    print("ver: " + ver + " (c)octopusLAB")
    print("Press Ctrl+C to abort")

    # TODO improve this
    # prepare directory
    if 'config' not in uos.listdir():
       uos.makedirs('config')

    run= True
    while run:
        sele = setupMenu()

        if sele == "x":
            print("Setup - exit >")
            time.sleep_ms(2000)
            print("all OK, press CTRL+D to soft reboot")
            run = False

        if sele == "si": #system_info()
            from util.sys_info import sys_info
            sys_info()

        if sele == "ds":
            print("Device setting:")
            print("   board_type  | soc_type (system on the board)")
            i=0
            for di in devices:
               print(str(i)+": "+str(di[0]) + " | " + str(di[1]))
               i=i+1

            print()
            sd = input("select: ")
            #print(str(devices[int(sd)]))
            print("> " + str(devices[int(sd)][0]) + " | " + str(devices[int(sd)][1]))

            dc = {}
            dc['board_type'] = str(devices[int(sd)][0]) #input("Board type ('oLAB RobotBoard1' or 'oLAB IoTBoard1'): ")
            dc['soc_type'] = str(devices[int(sd)][1])   #input("SoC type ('esp32' or 'esp8266'): ")

            print("Writing to file config/device.json")
            with open('config/device.json', 'w') as f:
                ujson.dump(dc, f)
                # ujson.dump(wc, f, ensure_ascii=False, indent=4)

        if sele == "ios":
            print("I/O setting:")
            # io menu
            ioMenu()

        if sele == "iot":
            print("Testing I/O")
            from util import io_test
            io_test.all()

        if sele == "w":
            from util.wifi_connect import WiFiConnect
            w = WiFiConnect()

            sel_w = wifiMenu()

            if sel_w == "a":
                wifi_ssid = input("SSID: ")
                wifi_pass = input("PASSWORD: ")
                w.add_network(wifi_ssid, wifi_pass)

            if sel_w == "r":
                wifi_ssid = input("SSID: ")
                w.remove_network(wifi_ssid)

            if sel_w == "s":
                print("Saved wifi networks")

                for k, v in w.config['networks'].items():
                    print ("SSID: {0}".format(k))

        if sele == "cw":
              print("Connect WiFi >")
              from util.wifi_connect import WiFiConnect
              w = WiFiConnect()
              if w.connect():
                  print("WiFi: OK")
              else:
                  print("WiFi: Connect error, check configuration")

        if sele == "mq":
            print("mqtt setup >")
            try:
                print()
                from util.mqtt import mqtt
                mqtt()
            except:
               print("Err.mqtt() or 'util.mqtt.py' does not exist")

        if sele == "st":
            print("Time setting >")
            rtc = machine.RTC()
            print(str(rtc.datetime()))
            setdatetime = input("input 6 numbers - format: RRRRR,M,D,wd,h,m > ")+(",0,0")
            dt_str = setdatetime.split(",")
            print(str(dt_str))
            dt_int = [int(numeric_string) for numeric_string in dt_str]
            rtc.init(dt_int)
            print(str(rtc.datetime()))

        if sele == "sdp":
            shutil()
            deplUrl = "http://iot.petrkr.net/olab/latest.tar"
            deploy(deplUrl)

        if sele == "sdo":
            shutil()
            deplUrl = "http://octopusengine.org/download/latest.tar"
            deploy(deplUrl)

        if sele == "od":
            from util.octopus import octopus
            octopus()

        if sele == "wr":
            print("under reconstruction <") 
            import esp
            esp.osdebug(None)
            import webrepl
            webrepl.start()
