from time import sleep, sleep_ms
from sensobox.display import instance as display
from sensobox.button import a_instance as pause_start_btn, b_instance as restart_btn
import time

# pauses or resumes the stopwatch
@pause_start_btn.on_press
def pause_start_button():
    global is_running
    is_running = not is_running
    if is_running:
        start()
    else:
        pause()
    
# calls restart()
@restart_btn.on_press
def restart_button():
    restart()

# starts stopwatch
def start():
    global total_time
    global start_time
    start_time = time.time_ns()
    print("start")
    while is_running:
        current_time = total_time + time.time_ns() - start_time
        display.show_right(current_time/1_000_000_000)
        sleep_ms(10)
# pauses stopwatch        
def pause():
    global total_time
    print("pause")
    total_time += time.time_ns() - start_time

# restarts stopwatch        
def restart():
    global is_running
    global current_time
    global total_time
    total_time = 0.0
    current_time = 0.0
    is_running = False
    display.show("00.00")
    print("restart")

restart()
