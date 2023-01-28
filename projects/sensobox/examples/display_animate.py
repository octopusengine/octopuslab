from time import sleep_ms
from sensobox.display.shortcuts import display

print("---animate---")

display.show(" .   ")
sleep_ms(100)
display.show("  .  ")
sleep_ms(100)
display.show("   . ")
sleep_ms(100)
display.show("    .")
sleep_ms(100)
display.show("    ")

