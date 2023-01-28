from time import sleep

from sensobox.thermometer import instance as thermometer
from sensobox.database import instance as database
from sensobox.display import instance as display
from time import sleep, sleep_ms

display.show(" .   ")
sleep_ms(100)
display.show("  .  ")
sleep_ms(100)
display.show("   . ")
sleep_ms(100)
display.show("    .")
sleep_ms(100)
display.show("    ")

# smycka programu
while True:
    temperature  = thermometer.get_temp()
    print("Temperature {}".format(temperature))

    # write temperature on most right postition on the display
    disp_list = [" ", " ", " ", " ", " "]
    str_temp = str(temperature)[0:5] # trim in case of more than 5 chars (one for decimal point)
    # use negative index to access characters from the last
    for i in range(1, len(str_temp)+1):
        disp_list[-i] = str_temp[-i]

    display.show("".join(disp_list))

    print("InfluxDB write")
    database.write(temperature=temperature)
    sleep(5)
