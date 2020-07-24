# octopusLAB test - 2019
# web server - ap_setup_wifi

# ap = ap_init()
#from examples.ap_setup_wifi import *
#s = webserver_init() 
#webserver_run(s) 

ver = "9.9.2019 - 0.12"

from time import sleep
from utils.octopus import printLog, printFree, get_eui, temp_init, get_temp, w, ap_init
from utils.pinout import set_pinout
pinout = set_pinout()
from components.led import Led #?VCh
led = Led(pinout.BUILT_IN_LED)
wnum = 0
web_wifi = ""
ssidTemp = ""
passTemp = ""
winfo = ""

def webserver_init():
    
    printLog("simple web server2 ver: " + ver)
    print(ver)
    printFree()
    
    try:
        import usocket as socket
    except:
        import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    printFree()

    return s

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

wcss = """<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: Silver; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: Orange; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: Navy;}</style>"""

web_bott = "<br /><hr />octopusLAB - wifi setup - uID: <br />" + get_eui()
web_form = """
  <form>
  ssid: <br><input id="fssid" type="text" name="ssid"><br>
  password: <br><input type="text" name="pass"><br><br>
  <input type="submit" value="Submit">
  </form>"""

def web_page():
  html = """<html><head> <title>octopus ESP setup</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> """ + wcss + """
  <script>function autoFill(ssid){document.getElementById('fssid').value = ssid;}</script>
  </head><body> <h1>octopusLAB - ESP WiFi setup</h1>
  """ + web_info + web_form + """
  <p>""" + web_wifi + """</p>
  <p><br />""" + web_bott + """</p></body></html>"""
  return html

def webconn(s):
  printLog("> webconn ")
  led.blink(50)
  global wnum, web_info, ssidTemp, passTemp, web_wifi
  
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)

  try:
    rs = request.split(" ")[1]
    rs = (rs[2:]).split("&")
    ssidTemp = rs[0].split("=")
    passTemp = rs[1].split("=")

    if ssidTemp[0] == "ssid": 
      ssidTemp = ssidTemp[1]
      print("ssid.ok")
      if len(ssidTemp) > 1:
        web_info = "<i>last ssid from form: " + ssidTemp + "</i><hr />"

    if passTemp[0] == "pass": 
      passTemp = passTemp[1]
      print("pass.ok")

  except:
    rs = "err"
    
  print()
  print('Content = ' + str(rs))
  
  # led_on = request.find('/?led=on')
  print()
  print("wifi_config: ")
  from utils.wifi_connect import WiFiConnect
  wc = WiFiConnect()

  webWc = "<hr /><b>Saved networks: </b><br />"
  for k, v in wc.config['networks'].items():
      webWc += k + "<br />"

  try:
    print("try save new netw.")
    print("ssid: " + str(ssidTemp) + " | pass: " + str(passTemp))

    if len(passTemp) > 0 and len(ssidTemp) > 1:
        wc.add_network(str(ssidTemp), str(passTemp))
        print("ok")
        led.blink(1000)
        led.blink(1000)
  except:
      print("err")  

  wnum += 1
  web_wifi = webnets + webWc + "<br /> refresh (" + str(wnum) + ")"

  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

trySetup = True

def webserver_run(s):
    printLog("> web server run:")
    while trySetup:
        webconn(s)

# w()
ap = ap_init()
sleep(2)

print("ap_scan")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
nets = sta_if.scan()
webnets = "<hr /><b>Scan networks: </b><br />"
for net in nets:
    ssidList = net[0].decode()
    # <u onclick='autoFill("IoT-link1")'>link1</u>
    # webnets += ssidList + "<br />"
    webnets += "<u onclick='autoFill(\"" + ssidList + "\")'>" + ssidList + "</u><br />"

"""
try:
  sc = ap.scan()
  print(len(sc))
  for wi in sc:
    print(wi[0])
  # sc[0][0]
except:
  print("err")
"""

s = webserver_init()
webserver_run(s)