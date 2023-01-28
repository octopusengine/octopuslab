from sensobox.display.shortcuts import display
from time import sleep_ms

display.show("   a")
sleep_ms(300)
display.show("  ah")
sleep_ms(300)
display.show(" aho")
sleep_ms(300)
display.show("ahoj")
sleep_ms(300)
display.show("hoj ")
sleep_ms(300)
display.show("oj ")
sleep_ms(300)
display.show("j   ")
sleep_ms(300)
display.show("    ")
sleep_ms(300)

sleep_ms(1000)

# does the same action
display.scroll("ahoj", scroll=true)
