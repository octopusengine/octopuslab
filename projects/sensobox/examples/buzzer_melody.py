from sensobox.buzzer.shortcuts import buzzer
from sensobox import melody
from time import sleep

print("--- buzzer ---")

buzzer.beep()
sleep(0.5)
buzzer.beep()
sleep(1)

buzzer.play_melody(melody.indiana)


