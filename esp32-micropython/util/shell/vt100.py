import sys

def get_cursor_position():
    x=0
    y=0
    num=''

    sys.stdout.write('\x1b[6n')
    while True:
        char = sys.stdin.read(1)
        if char is 'R':
            y = int(num)
            break
        if char is '\x1b':
            x=0
            y=0
            num=''
            continue
        if char is '[':
            continue
        if char is ';':
            x=int(num)
            num=''
            continue
        num+=char
    return (x,y)

def get_terminal_size():
    # Save cursor position
    sys.stdout.write('\x1b[s')
    
    #Move cursor outside of screen
    sys.stdout.write('\x1b[999B\x1b[999C')
    (x,y) = get_cursor_position()
    
    # Restore cursor position
    sys.stdout.write('\x1b[u')

    return (x,y)
