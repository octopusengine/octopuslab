from time import sleep
from util.octopus import w, web_server
from robot import start

w()
sleep(5)
web_server()

print('Ahoj')

start()
