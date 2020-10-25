from time import sleep
from machine import Pin
from utils.octopus_lib import w
from microWebSrv import MicroWebSrv
from neopixel import NeoPixel
import json

print("-"*50)
print("ftp and WebServer - RGB neopixel")
print("-"*50)

np = NeoPixel(Pin(15), 1)

def _httpHandlerLEDPost(httpClient, httpResponse):
    content = httpClient.ReadRequestContent()  # Read JSON color data
    colors = json.loads(content)
    blue, green, red = [colors[k] for k in sorted(colors.keys())]
    np[0] = (red, green, blue)
    np.write()
    httpResponse.WriteResponseJSONOk()


btnum = 0
button = Pin(0, Pin.IN)
print("press button / CTRL+C or continue")
sleep(1)

for i in range(12):
    print("-",end="")
    btnum += button.value()
    sleep(0.2)

w()
print()

if (btnum==0):
    print("button0 -> start WebServer www/rgb")
    #mws = MicroWebSrv(webPath="www/rgb")
    #mws.Start(threaded=True)
    routeHandlers = [ ( "/led", "POST",  _httpHandlerLEDPost ) ]
    srv = MicroWebSrv(routeHandlers=routeHandlers, webPath='/www/rgb/')
    srv.Start(threaded=False)
else:
    print("button1 -> start FTP")
    import ftp

print("="*50)
