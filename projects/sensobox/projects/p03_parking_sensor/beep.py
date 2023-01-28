from time import sleep_ms
from sensobox.ultrasound import instance as ultrasound
from sensobox.buzzer import instance as buzzer

# loop updating the pause between beeps
while True:
    buzz.play_tone(1000, 32, 1000)
    cm = echo.distance_cm()
    if cm > 0:
        sleep_ms(int(cm)*5)
    
