from time import sleep, sleep_ms
from sensobox.display import instance as display
from sensobox.button import a_instance as pause_start_btn, b_instance as restart_btn

time = 0.0
is_running = False

# pauses or resumes the stopwatch
@pause_start_btn.on_press
def pause_start_button():
    global is_running
    is_running = not is_running
    if is_running:
        print("start")
        start()
    else:
        print("pause")

# calls restart()
@restart_btn.on_press
def restart_button():
    restart()

# starts stopwatch
def start():
    global time
    while is_running:
        time += 0.01;
        display.show_right(time)
        sleep_ms(10)

# restarts stopwatch        
def restart():
    global time
    global is_running
    time = 0.0
    is_running = False
    display.show("00.00")
    
restart()
