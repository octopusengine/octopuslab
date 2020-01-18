import sys
from util.shell import terminal_color


def edit(filename='main.py'):
    SEPARATOR_WIDTH = 50
    EDITOR_LINE_PREFIX_TPL = terminal_color('{:>4d}│')
    EDITOR_TITLE_TOP_PREFIX = terminal_color('    ┌')
    EDITOR_TITLE_TOP_SUFIX = terminal_color('┐')
    EDITOR_TITLE_PREFIX = terminal_color('    │')
    #EDITOR_TITLE_SUFIX = "\033[32m│\033[m" # '│'
    EDITOR_TITLE_SUFIX = terminal_color('│')
    EDITOR_TOP_PREFIX = terminal_color('    ├')
    EDITOR_TOP_TITLE_SUFIX = terminal_color('┴')
    EDITOR_BOTTOM_PREFIX = terminal_color('    └')

    show_line_numbers = True
    changed = False
    file_exists = True
    buff = []  # empty new file contains one line with a newline character

    def print_buff():
        editor_title = '{:s}{:s}{:s}'.format(
            filename,
            not file_exists and ' [NEW]' or '',
            changed and ' [CHANGED]' or '',
        )

        print()
        title_top_prefix = ''
        if show_line_numbers:
            title_top_prefix = EDITOR_TITLE_TOP_PREFIX
        print('{:s}{:s}{:s}'.format(title_top_prefix, terminal_color('─' * (len(editor_title)+4)), EDITOR_TITLE_TOP_SUFIX))
        title_prefix = ''
        if show_line_numbers:
            title_prefix = EDITOR_TITLE_PREFIX
        print('{:s}  {:s}  {:s}'.format(title_prefix, editor_title, EDITOR_TITLE_SUFIX))
        top_prefix = ''
        if show_line_numbers:
            top_prefix = EDITOR_TOP_PREFIX
        print('{:s}{:s}{:s}{:s}'.format(top_prefix, terminal_color('─' * (len(editor_title)+4)), EDITOR_TOP_TITLE_SUFIX, terminal_color('─' * (SEPARATOR_WIDTH-len(top_prefix)-(len(editor_title)+4)))))

        line_cnt = 0
        line_prefix = ''
        for line in buff:
            if show_line_numbers:
                line_cnt += 1
                line_prefix = EDITOR_LINE_PREFIX_TPL.format(line_cnt)
            print('{:s}{:s}'.format(line_prefix, line))
        if show_line_numbers:
            line_cnt += 1
            line_prefix = EDITOR_LINE_PREFIX_TPL.format(line_cnt)
        print('{:s}{:s}'.format(line_prefix, ''))

        bottom_prefix = ''
        if show_line_numbers:
            bottom_prefix = EDITOR_BOTTOM_PREFIX
        print('{:s}{:s}'.format(bottom_prefix, terminal_color('─' * (SEPARATOR_WIDTH-len(bottom_prefix)))))

    def print_help():
        print('  h      print this help')
        print('  p      print file (current state in buffer)')
        print('  l      toggle line numbers (copy mode)')
        print('  q      quit')
        print('  w      write file (save)')
        print('  wq     write into file and quit')
        print()
        print('  i<int> [<str>]   insert new line at given position [int], containing [str] or empty')
        print('  a<int> [<str>]   insert new line after given [int], containing [str] or empty')
        print('  e<int> [<str>]   edit line number [int], replace line with [str] or will be prompted')
        print('  d<int>           delete line number [int]')
        print()

    def parse_line_no(input):
        try:
            line_no = int(input)
            if 1 <= line_no <= len(buff) + 1:
                return line_no
        except:
            pass
        print('Line number must be between 1 and {0}, "h" for help'.format(len(buff) + 1))
        return 0

    def parse_line_no_txt(input):
        line_no_el = input.split(' ')[0]
        line_no = parse_line_no(line_no_el)
        txt = ''
        try:
            # +1 for a space separator between [int] and [txt]
            txt = input[len(line_no_el)+1:]
        except:
            pass
        return line_no, txt

    try:
        # read file into buff
        with open(filename, 'r') as fi:
            for line in fi:
                l = line
                if line.endswith('\n'):
                    l = line[:-1]
                buff.append(l)
    except FileNotFoundError:
        file_exists = False

    # welcome messages
    print('Welcome to MicroPython text file line editor. New line at the end of every non empty file is enforced. Use "h" for help.')
    print_buff()
    print()

    while True:
        action = input('action: ')

        # action print current buffer
        if action == 'p':
            print_buff()

        # action print help
        elif action == 'h':
            print_help()

        # action print help
        elif action == 'l':
            show_line_numbers = not show_line_numbers
            print_buff()

        # action edit one line
        elif action.startswith('e'):
            line_no, txt = parse_line_no_txt(action[1:])
            if not line_no:
                continue
            # get new text interactivelly if was not provided
            if not txt:
                try:
                    print('         ┌───┬───┬───┬───┬───┬───')
                    print('Current:', buff[line_no-1])
                    txt = input('    New: ')
                except IndexError:
                    txt = ''
            if line_no == len(buff) + 1:
                # editing last line means append to buffer
                buff.append('{0}'.format(txt))
            else:
                # edit regular line
                buff[line_no-1] = '{0}'.format(txt)
            changed = True
            print_buff()

        # action insert new line
        elif action.startswith('i'):
            line_no, txt = parse_line_no_txt(action[1:])
            if not line_no:
                continue
            # insert txt and shift all records in buffer
            buff.insert(line_no-1, '{0}'.format(txt))
            changed = True
            print_buff()

        # action append new line
        elif action.startswith('a'):
            line_no, txt = parse_line_no_txt(action[1:])
            if not line_no:
                continue
            if line_no == len(buff) + 1:
                print('Can not append after the last line in file, use insert instead')
                continue
            # inserting after index means index is line_no-1 +1
            buff.insert(line_no, '{0}'.format(txt))
            changed = True
            print_buff()

        # action delete a line
        elif action.startswith('d'):
            line_no = parse_line_no(action[1:])
            if not line_no:
                continue
            if line_no == len(buff) + 1:
                print('Last line in file can not be removed')
                continue
            del(buff[line_no-1])
            changed = True
            print_buff()

        # action save buffer to file
        elif action in ('w', 'wq'):
            print('Writing into file "{0}"'.format(filename))
            file_mode = 'w'
            # save buff into file
            with open(filename, file_mode) as fo:
                for line in buff:
                    fo.write(line + '\n')
            file_exists = True
            changed = False
        elif action == 'q':
            pass
        else:
            print('Bad option, try again, "h" for help')

        # exit condition
        if action in ('q', 'wq'):
            print('Bye')
            break

        print()

if __name__ == '__main__':
    # print command line arguments
    if len(sys.argv) > 1:
        edit(sys.argv[1])
    else:
        edit()
