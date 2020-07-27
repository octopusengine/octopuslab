# octopusLAB test - 2019
from time import sleep
from utils.octopus import button_init, button, w, web_server, ap_init
from components.led import Led
led = Led(2)
button0 = button_init(0)
debounce = 9
ap = False


print("esp32 web server - start >")
for id in range(10):
  print(10-id)
  led.blink()
  if button(button0)[0] >= debounce:
      print("button > AP_start")
      ap = True
      for id in range(5):
          led.blink(100,100)
      break

sleep(1)
if ap: wc = ap = ap_init()
else:  wc = w()

sleep(1)
web_server()