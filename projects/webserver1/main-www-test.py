from time import sleep
from machine import Pin
from utils.octopus import w
from microWebSrv import MicroWebSrv

print("-"*50)
print("ftp and webrerver - version 1")
print("-"*50)

button = Pin(0, Pin.IN)

w() # wifi connect

print("CTRL+C or continue")
sleep(1)
btn = button.value()
if (btn): print("button ok")

for i in range(12):
    print("-",end="")
    sleep(0.3)

print()

if (btn):
    print("button0 -> start WebServer")
    mws = MicroWebSrv(webPath="www/rgb")
    mws.Start(threaded=True)
else:
    print("button1 -> start FTP")
    import ftp

print("="*50)




