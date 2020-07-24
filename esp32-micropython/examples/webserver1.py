# octopusLAB test - 2019
# more project details at https://RandomNerdTutorials.com
ver = "23.7.2019 #79"

from utils.octopus import printLog, printFree, get_eui

from utils.pinout import set_pinout
pinout = set_pinout()
from components.led import Led #?VCh
led = Led(pinout.BUILT_IN_LED)

def webserver_init():
    printLog("simple web server")
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
  if led.value() == 1: gpio_state="ON"
  else: gpio_state="OFF"
  
  html = """<html><head> <title>octopusLAB - ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> """ + wcss + """</head><body> <h1>octopus LAB - ESP Web Server</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a><br />""" + wbott + """</p></body></html>"""
  return html

def webconn(s):
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  if led_on == 6:
    print('LED ON')
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

def webserver_run(s):
    printLog("> run:")
    while True:
        webconn(s)