import esp32
from time import sleep


print("hall_test")
while True:
    mg = esp32.hall_sensor()
    print(mg)
    sleep(1)
