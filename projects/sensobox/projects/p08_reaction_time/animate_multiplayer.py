from sensobox.display import instance as display
from sensobox.button import a_instance as one_btn, b_instance as two_btn
from time import sleep_ms
import time
import random

# animate
for i in range(3):
    tm.show("8888")
    sleep_ms(500)
    tm.show("    ")
    sleep_ms(500)
    
# initialize variables    
tm.show("8888")
startable = False
running = False
clickable = False
startable = True

# handle both player actions
# only ends the game if called for the first time
@one_btn.on_press
def stop(player="one"):
    global start_time
    global random_time
    global running
    global clickable
    if running:
        wrong()
        running = False
    elif clickable:
        clickable = False
        offset = abs(random_time-((time.time_ns() - start_time)/1_000_000_000))
        end(offset, player)

# starts the game
@two_btn.on_press
def start():
    global startable
    global start_time
    global random_time
    global clickable
    global running
    if startable:
        startable = False
        start_time = time.time_ns()
        random_time = random.uniform(2.2, 6.2)
        tm.show("    ")
        running = True
        while running: # counting loop
            check = (time.time_ns() - start_time)/1_000_000_000
            if check > random_time:
                tm.show("8888")
                clickable = True
                running = False
    elif running or clickable: # if started, calls stop("two")
        stop("two")

# end and show result with animation
def end(offset, player):
    text = "****"
    if player == "two":
        text = "vvvv"
    for i in range(3):
        tm.show(text)
        sleep_ms(500)
        tm.show("    ")
        sleep_ms(500)
        
    tm.show_right(offset)
