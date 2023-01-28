from sensobox.influxdb.shortcuts import influxdb
from sensobox.thermometer.shortcuts import thermometer
from sensobox.display.shortcuts import display
from sensobox.network.shortcuts import network
from time import sleep, sleep_ms

print("---thermometer-cloud---")

display.show(" .   ")
sleep_ms(100)
display.show("  .  ")
sleep_ms(100)
display.show("   . ")
sleep_ms(100)
display.show("    .")
sleep_ms(100)
display.show("    ")

network.connect()

# smycka programu
while True:
    temp  = thermometer.get_temp()
    print("Temperature {}".format(temp))

    # write temperature on most right postition on the display
    disp_list = [" ", " ", " ", " ", " "]
    str_temp = str(temp)[0:5] # trim in case of more than 5 chars (one for decimal point)
    # use negative index to access characters from the last
    for i in range(1, len(str_temp)+1):
        disp_list[-i] = str_temp[-i]

    display.show("".join(disp_list))

    print("databaseDB write")
    influxdb.write(temperature=temp)
    sleep(5)

