from sensobox.display import instance as display
from sensobox.button import a_instance as start_btn, b_instance as stop_btn
from time import sleep_ms
import time
import random

# animate    
for i in range(3):
    display.show("8888")
    sleep_ms(500)
    display.show("    ")
    sleep_ms(500)
    
# initialize variables
display.show("8888")
startable = False
running = False
clickable = False
startable = True

# stop the time and calculate offset
@stop_btn.on_press
def stop():
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
        end(offset)

# start game
@start_btn.on_press
def start():
    global startable
    global start_time
    global random_time
    global clickable
    global running
    if startable:
        start_time = time.time_ns()
        random_time = random.uniform(2.2, 6.2)
        display.show("    ")
        running = True
        while running: # counting loop
            check = (time.time_ns() - start_time)/1_000_000_000
            if check > random_time:
                display.show("8888")
                clickable = True
		running = False
		
# animate and show result
def end(offset):
    for i in range(3):
        display.show_right(offset)
        sleep_ms(500)
        display.show("    ")
        sleep_ms(500)
	
    display.show_right(offset)
