'''
This is simple interactive text file editor to be used as part of uPyShell

This module has a dependency on re module and
local .terminal for color support

This can be executed locally (without micropython or a controller):
step one dir up and execute:
$ python 3 -m shell.editor [optional filename]

# This file is part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2020 Jan Copak, Vasek Chalupnicek
'''
import re


def edit(filename='/main.py'):
    from .terminal import terminal_color
    SEPARATOR_WIDTH = 50
    EDITOR_LINE_PREFIX_TPL = terminal_color('{:>4d}│')
    EDITOR_TITLE_TOP_PREFIX = terminal_color('    ┌')
    EDITOR_TITLE_TOP_SUFIX = terminal_color('┐')
    EDITOR_TITLE_PREFIX = terminal_color('    │')
    # EDITOR_TITLE_SUFIX = "\033[32m│\033[m" # '│'
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
        print('{:s}{:s}{:s}'.format(title_top_prefix, terminal_color('─' * (len(editor_title) + 4)), EDITOR_TITLE_TOP_SUFIX))
        title_prefix = ''
        if show_line_numbers:
            title_prefix = EDITOR_TITLE_PREFIX
        print('{:s}  {:s}  {:s}'.format(title_prefix, editor_title, EDITOR_TITLE_SUFIX))
        top_prefix = ''
        if show_line_numbers:
            top_prefix = EDITOR_TOP_PREFIX
        print('{:s}{:s}{:s}{:s}'.format(
            top_prefix,
            terminal_color('─' * (len(editor_title) + 4)),
            EDITOR_TOP_TITLE_SUFIX,
            terminal_color('─' * (SEPARATOR_WIDTH - len(top_prefix) - (len(editor_title) + 4))))
        )

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
        print('{:s}{:s}'.format(bottom_prefix, terminal_color('─' * (SEPARATOR_WIDTH - len(bottom_prefix)))))

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
        print('  c<int>[-<int>]   comment/uncomment line [int] with a #, or multiple lines if a range is provided (does each line separately)')
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
            txt = input[len(line_no_el) + 1:]
        except:
            pass
        return line_no, txt

    try:
        # read file into buff
        with open(filename, 'r') as fi:
            for line in fi:
                ln = line
                if line.endswith('\n'):
                    ln = line[:-1]
                buff.append(ln)
    except OSError:
        file_exists = False

    # welcome messages
    print('Welcome to MicroPython text file line editor. New line at the end of every non empty file is enforced. Use "h" for help.')
    print_buff()
    print()

    while True:
        action = input(terminal_color('action: '))

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
                    print('Current:', buff[line_no - 1])
                    txt = input('    New: ')
                except IndexError:
                    txt = ''
            if line_no == len(buff) + 1:
                # editing last line means append to buffer
                buff.append('{0}'.format(txt))
            else:
                # edit regular line
                buff[line_no - 1] = '{0}'.format(txt)
            changed = True
            print_buff()

        # action insert new line
        elif action.startswith('i'):
            line_no, txt = parse_line_no_txt(action[1:])
            if not line_no:
                continue
            # insert txt and shift all records in buffer
            buff.insert(line_no - 1, '{0}'.format(txt))
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
            del(buff[line_no - 1])
            changed = True
            print_buff()

        # action comment/uncomment a line
        elif action.startswith('c'):
            idxs = action[1:].split('-')
            line_no = parse_line_no(idxs[0])
            if not line_no:
                # for invalid inputs skip
                continue
            line_idx_start = line_no - 1
            line_idx_end = line_idx_start
            if len(idxs) == 2:
                # if we have a range on input
                line_no = parse_line_no(idxs[1])
                if not line_no:
                    # for invalid inputs skip
                    continue
                line_idx_end = line_no - 1
            # check start < end
            if line_idx_start > line_idx_end:
                print('Line range start can not be greater than end')
                continue
            # for each line in range
            for line_idx in range(line_idx_start, line_idx_end):
                initial_ws = ''
                line_content = ''
                try:
                    mo = re.search(r'^(\s*)(.*)', buff[line_idx])
                    # remember starting whitespaces
                    initial_ws = mo.group(1)
                    line_content = mo.group(2)
                except IndexError:
                    pass
                # if first non-whitespace character is #, then uncomment
                if len(line_content) and line_content[0] == '#':
                    # remove hash and any whitespaces until first character
                    mo = re.search(r'^(#\s*)(.*)', line_content)
                    buff[line_idx] = initial_ws + mo.group(2)
                # else comment
                else:
                    # add "# " after initial whitespaces and then the rest of the line
                    buff[line_idx] = initial_ws + '# ' + line_content
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
    import sys

    if len(sys.argv) > 1:
        edit(sys.argv[1])
    else:
        edit()
