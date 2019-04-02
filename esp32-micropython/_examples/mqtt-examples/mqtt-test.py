"""
import upip
upip.install('micropython-umqtt.robust')
"""
print("test mqtt")

from umqtt.robust import MQTTClient
client = MQTTClient("", "ip")  # IP broker addr 

print("connect()")
client.connect()

# client.publish("test123","567") # topic, message (value) to publish


