# octopusLAB test - 2019
# web server - ap_setup_wifi

# ap = ap_init()
#from examples.ap_setup_wifi import *
#s = webserver_init() 
#webserver_run(s) 

ver = "8.9.2019 - 0.11"

from util.octopus import printLog, printFree, get_eui, temp_init, get_temp, w

from util.pinout import set_pinout
pinout = set_pinout()
from util.led import Led #?VCh
led = Led(pinout.BUILT_IN_LED)


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

wbott = "<br /><hr />2019 - workskop test<br />" + get_eui()

def web_page():
  web_info = "web-info"
  web_wifi = "test-wifi"

  html = """<html><head> <title>octopusLAB - ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> """ + wcss + """
  </head><body> <h1>octopus LAB - ESP Web Server</h1>
  <form>
  ssid: <br><input type="text" name="ssid"><br>
  password: <br><input type="text" name="pass"><br><br>
  <input type="submit" value="Submit">
  </form>
  <p>""" + web_wifi + """</p>
  <p><br />""" + wbott + """</p></body></html>"""

  return html

def webconn(s):
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  try:
    rs = request.split(" ")[1]
    rs = (rs[2:]).split("&")
  except:
    rs = "err"
    
  print()
  print('Content = ' + str(rs))
  led_on = request.find('/?led=on')
  
  """
  from util.wifi_connect import WiFiConnect
  w = WiFiConnect()
  wifi_ssid = input("SSID: ")
  wifi_pass = input("PASSWORD: ")
  w.add_network(wifi_ssid, wifi_pass)
  """
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

trySetup = True
def webserver_run(s):
    printLog("> run:")
    while trySetup:
        webconn(s)


w()
s = webserver_init()
webserver_run(s)