from time import sleep_ms
from sensobox.display import instance as display
from sensobox.button import a_instance as set_btn, b_instance as change_btn
import time

# saves the time
hours = 0
minutes = 0
seconds = 0
display.show('00.00')
# state 0 = running, 1 = setting hours, 2 = setting minutes, 3 = waiting for start
state = 3
blink = True

# shifts state to the next one
@set_btn.on_press
def set():
    global state
    global timer
    global hours
    global minutes
    global blink
    if state == 3 or state == 2:
        timer = time.time_ns()
        seconds = 0
        run()
    elif state == 0:
        state = 1
        show_time(hours, minutes, True)
    elif state == 1:
        state = 2
        
        
# changes values if state = 1/2        
@change_btn.on_press
def change():
    global state
    global hours
    global minutes
    global seconds
    global blink
    if state == 1:
        if hours > 22:
            hours = 0
        else:
            hours += 1
    elif state == 2: 
        if minutes > 58:
            minutes = 0
        else:
            minutes += 1
    show_time(hours, minutes, True)

# starts clock if stopped
def run():
    global state
    global timer
    global blink
    state = 0
    while state == 0:
        if ((time.time_ns() - timer) / 1_000_000_000) > 1:
            add_second()
            timer = time.time_ns()
            blink = not blink
        sleep_ms(1)
    
# adds one second to the time
# changes the minute or hour value if needed    
def add_second():
    global hours
    global minutes
    global seconds
    global running
    if seconds > 58:
        if minutes > 58:
            if hours > 22:
                seconds = 0
                minutes = 0
                hours = 0
            else:
                seconds = 0
                minutes = 0
                hours += 1
        else:
            seconds = 0
            minutes += 1
    else:
        seconds += 1
    show_time(hours, minutes, blink)
    
# shows the time on display in the correct format    
def show_time(hours, minutes, blink):
    txt = ''
    if hours < 10:
        txt += '0'
    txt += str(hours)
    if blink:
        txt += '.'
    if minutes < 10:
        txt += '0'
    txt += str(minutes)
    display.show(txt)
