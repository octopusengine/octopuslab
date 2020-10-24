from time import sleep
from machine import Pin
from utils.octopus import w
from microWebSrv import MicroWebSrv
from neopixel import NeoPixel
import json

np = NeoPixel(Pin(15), 1)


def _httpHandlerLEDPost(httpClient, httpResponse):
    content = httpClient.ReadRequestContent()  # Read JSON color data
    colors = json.loads(content)
    blue, green, red = [colors[k] for k in sorted(colors.keys())]
    np[0] = (red, green, blue)
    np.write()
    httpResponse.WriteResponseJSONOk()


print("-"*50)
print("ftp and WebServer - RGB neopixel")
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




