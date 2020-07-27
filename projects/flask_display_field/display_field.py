from time import sleep
import urequests as requests
from utils.octopus import disp7_init
from utils.wifi_connect import WiFiConnect

# WiFi connection
net = WiFiConnect()
net.connect()

# Put your url here
url = "http://192.168.12.60:5000/display.txt"
d7 = disp7_init()

while True:
    response = requests.get(url)
    print(response.status_code)
    d7.show(response.text)
    sleep(5)
