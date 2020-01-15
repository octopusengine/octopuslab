import sys

SEPARATOR_WIDTH = 50

def edit(filename='main.py'):
    changed = False
    buff = []  # empty new file contains one line with a newline character

    def print_buff():
        print('{2} {0}{1} {2}'.format(
            filename,
            changed and ' [CHANGED]' or '',
            '=' * int((SEPARATOR_WIDTH - len(filename)) / 2))
        )
        print()

        line_cnt = 0
        for line in buff:
            line_cnt += 1
            print('{:>4d}'.format(line_cnt), line, end='')
        if line.endswith('\n'):
            line_cnt += 1
            print('{:>4d}'.format(line_cnt))
        else:
            # adding newline without linenumber if missing on the last line in the file
            print()

        print()
        print('=' * SEPARATOR_WIDTH)
        print()

    def buff_lines():
        if buff[-1].endswith('\n'):
            return len(buff) + 1
        return len(buff)

    def print_help():
        print('Welcome to MicroPython text file line editor. New line at the end')
        print('of the file is enforced. Possible Actions are:')
        print()
        print('  h      print this help')
        print('  p      print file (current state in buffer)')
        print('  q      quit')
        print('  w      write file (save)')
        print('  wq     write into file and quit')
        print()
        print('  i<int> [<str>]   insert new line after line number [int], containing [txt] or empty')
        print('  e<int> [<str>]   edit line number [int], replace line with [txt] or interactive editing')
        print('  d<int>           delete line number [int]')
        print()

    def parse_lineno(input):
        try:
            lineno = int(input)
            if 1 <= lineno <= buff_lines():
                return lineno
        except:
            pass
        print('Line number must be between 1 and {0}'.format(buff_lines()))
        return 0

    def parse_lineno_txt(input):
        lineno_el = input.split(' ')[0]
        lineno = parse_lineno(lineno_el)
        txt = ''
        try:
            # +1 for a space separator between [int] and [txt]
            txt = input[len(lineno_el)+1:]
        except:
            pass
        return lineno, txt

    # read file into buff
    with open(filename, 'r') as fi:
        for line in fi:
            buff.append(line)
    # ensure last line ends with a newline
    if not buff[-1].endswith('\n'):
        buff[-1] += '\n'
        changed = True

    print_help()
    print_buff()

    while True:
        print('action: ', end='')
        action = input()
        if action == 'p':
            print_buff()
        elif action == 'h':
            print_help()
        elif action.startswith('e'):
            lineno, txt = parse_lineno_txt(action[1:])
            if not lineno:
                continue
            if not txt:
                print('Current:', buff[lineno-1], end='')
                txt = input('New:     ')
            buff[lineno-1] = '{0}\n'.format(txt)
            changed = True
            print_buff()
        elif action.startswith('i') or action.startswith('a'):
            lineno, txt = parse_lineno_txt(action[1:])
            if not lineno:
                continue
            # inserting after index means list index is the same as lineno
            buff.insert(lineno, '{0}\n'.format(txt))
            changed = True
            print_buff()
        elif action.startswith('d'):
            lineno = parse_lineno(action[1:])
            if not lineno:
                continue
            if lineno == buff_lines():
                print('Last line in file can not be removed')
                continue
            del(buff[lineno-1])
            changed = True
            print_buff()
        elif action in ('w', 'wq'):
            print('Writing into file "{0}"'.format(filename))
            # save buff into file
            with open(filename, 'w') as fo:
                for line in buff:
                    fo.write(line)
        else:
            print('Bad option, try again')

        # exit condition
        if action in ('q', 'wq'):
            print('Bye')
            break

if __name__ == '__main__':
    # print command line arguments
    if len(sys.argv) > 1:
        edit(sys.argv[1])
    else:
        edit()
