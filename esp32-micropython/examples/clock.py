# simple basic example - ESP32
# cp("examples/clock.py") > main.py


from time import sleep
from util.octopus import w, get_hhmm, time_init, clt
from shell.terminal import printTitle


def clock():
    clt()
    print(get_hhmm(":"))
    sleep(1)
    clt()
    print(get_hhmm(" "))
    sleep(1)

w()	# wifi connect
time_init() # server > time setup

printTitle("examples/clock.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

while True:
	clock()
