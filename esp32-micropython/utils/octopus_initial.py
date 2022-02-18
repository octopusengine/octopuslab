# this module is to setup your board throuhg REPL
# it's loaded in boot.py and provides function setup()
# user is questioned in interactive mode

#TODO DRY for filename
import time, uos
import ujson
import machine #datetime

ver = "0.1/ 13.8.2019"

octopusASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   )  \ `)(' / ( ",
]

def printOctopus():
    for ol in octopusASCII:
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

    def exists(path):
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

            if not exists(name):
                os.mkdir(name)
        else:
            extracted = t.extractfile(f)

            #if exists(f.name):
            #    os.remove(f.name)

            with open(f.name, "wb") as fobj:
                shutil.copyfileobj(extracted, fobj)


def setupMenu():
    print()
    print('=' * 30)
    print('        S E T U P')
    print('=' * 30)
    print("[w]   - wifi submenu")
    print("[cw]  - connect wifi")
    print("[cl]  - connect LAN")
    print("[sd]  - system download")
    print("[q]   - quit setup")

    print('=' * 30)
    sel = input("select: ")
    return sel

def wifiMenu():
    print()
    print('=' * 30)
    print('       S E T U P - W I F I')
    print('=' * 30)
    print(" [a] - add wifi network")
    print(" [r] - remove wifi network")
    print(" [s] - show configuration")
    print(" [q] - quit")

    print('=' * 30)
    sel = input("select: ")
    return sel

def shutil():
    print("System download > (initial octopus modules)")
    import upip
    print("Installing shutil")
    upip.install("micropython-shutil")
    print("Running deploy")

def setup():
    printOctopus()
    print("Hello, this will help you initialize your ESP")
    print("ver: " + ver + " (c)octopusLAB")
    print("Press Ctrl+C to abort")

    # TODO improve this
    # prepare directory
    if 'config' not in uos.listdir():
       uos.mkdir('config')

    run= True
    while run:
        sele = setupMenu()

        if sele == "q":
            print("all OK, press CTRL+D to soft reboot")
            run = False

        if sele == "w":
            from utils.wifi_connect import WiFiConnect
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
              from utils.wifi_connect import WiFiConnect
              w = WiFiConnect()
              if w.connect():
                  print("WiFi: OK")
              else:
                  print("WiFi: Connect error, check configuration")

        if sele == "cl":
              print("Connect LAN >")
              import network
              if "ETH_CLOCK_GPIO17_OUT" in dir(network)
                  lan = network.LAN(mdc = machine.Pin(23), mdio=machine.Pin(18), phy_type=network.PHY_LAN8720, phy_addr=1, clock_mode=network.ETH_CLOCK_GPIO17_OUT)
              else:
                  lan = network.LAN(mdc = machine.Pin(23), mdio=machine.Pin(18), phy_type=network.PHY_LAN8720, phy_addr=1)

              lan.active(1)
              retry = 0
              while not lan.isconnected() or lan.ifconfig()[0] is '0.0.0.0':
                  retry+=1
                  time.sleep_ms(500)

                  if retry > 20:
                      break;

              if lan.isconnected():
                  print("LAN: OK")
              else:
                  print("LAN: Connect error, check cable or DHCP server")

        if sele == "sd":
            shutil()
            deplUrl = "https://octopusengine.org/download/micropython/stable.tar"
            deploy(deplUrl)
