# octopusLAB example - 2019
# simple dallas and relay thermostat

# (temperature < temperature1) -> relay(on)
# 
from time import sleep
from utils.octopus import temp_init, disp7_init
from components.iot import Relay

print("setup > ")
from config import Config 
keys = ["temperature1","temperature2","relaypin"]
config = Config("thermostat", keys)
print("press ctl+C and config.setup()")
sleep(3)

print("init > ")
d7 = disp7_init()	# 8 x 7segment display init
t = temp_init()
relay = Relay(config.config["relaypin"])
sleep(2)

print("start > ")
config_temp = config.config["temperature1"]
print("config temperature: " + str(config_temp))

while True:
    temp  = t.get_temp()
    print(temp, config_temp)
    d7.show(temp)
    if temp < config_temp:
        print("relayOn")
        relay.value(1)
        sleep(3)
    else:
        print("relayOff")
        relay.value(0)
        sleep(5)




