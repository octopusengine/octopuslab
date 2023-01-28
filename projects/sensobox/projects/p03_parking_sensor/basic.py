from time import sleep, sleep_ms
from sensobox.ultrasound import instance as ultrasound
from sensobox.display import instance as display

# loop updating the distance value
while True:
    tm.show_right(echo.distance_cm())
    sleep.ms(100)
    
