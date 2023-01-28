from machine import Pin
from sensobox.button import a_instance as start_btn, b_instance as stop_btn
from sensobox.display import instance as display
from time import sleep_ms
import time

# show target time    
display.show("10.00")

# stop the time
@stop_btn.on_press
def stop():
    global start_time
    global total_time
    total_time = (time.time_ns()-start_time)/1_000_000_000
    end()

# start game
@start_btn.on_press
def start():
    global start_time
    display.show("    ")
    start_time = time.time_ns()

# show result
def end():
    display.show_right(abs(total_time-10))
