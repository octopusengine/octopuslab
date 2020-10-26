print("--- octopusLAB: test_WiFi ---")

print("-> init")
from utils.octopus_lib import w
net = w()  # wifi connection

ip = net.sta_if.ifconfig()[0]

print("--- IP: ", ip)