# This file is part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2020 Jan Copak, Petr Kracik, Vasek Chalupnicek, Jan Cespivo

"""
from util.shell import shell
shell()

> cat / edit / ls / mkdir / cp / rm / find / df ...
--------
autostart:
>>> from config import Config
>>> cc = Config("boot")
>>> cc.set("import_shell",1)
>>> cc.save()
--------
last update: 
"""
__version__ = "0.28 - 1.2.2020"

# toto: ifconfig, kill, wifion, wifioff, wget, wsend, ... 
# from util.shell.terminal import printTitle

SEPARATOR_WIDTH = 50

_command_registry = {}
_background_jobs = {}
_is_wifi_connect = False


def _thread_wrapper(func, job_id, *arguments):
    try:
        func(*arguments)
    finally:
        del _background_jobs[job_id]
        print('[{job_id}] stopped'.format(job_id=job_id))


def _background_func(func, command_list):
    def _wrapper(*arguments):
        from _thread import start_new_thread
        from time import ticks_ms
        job_id = start_time = ticks_ms()
        start_new_thread(_thread_wrapper, (func, job_id) + arguments)
        _background_jobs[job_id] = {'start_time': start_time, 'command_list': command_list}
        print('[{job_id}] started'.format(job_id=job_id))

    return _wrapper


def _register_command(func_name):
    def _command(func):
        _command_registry[func_name] = func
        return func

    return _command


def command(func_or_name):
    if callable(func_or_name):
        return _register_command(func_or_name.__name__)(func_or_name)
    elif isinstance(func_or_name, str):
        name = func_or_name
        return _register_command(name)

    raise ImportError('bad decorator command')
 

def w_connect():
    global _is_wifi_connect
    # led.value(1)

    from util.wifi_connect import WiFiConnect
    sleep(1)
    w = WiFiConnect()
    if w.connect():
        print("WiFi: OK")
        _is_wifi_connect = True
    else:
        print("WiFi: Connect error, check configuration")

    # led.value(0)
    return w


@command
def sleep(seconds):
    from time import sleep
    sleep(float(seconds))


@command
def ifconfig():
    from .terminal import terminal_color
    # test for wifi on / off/ connect / disconnect
    #from util.octopus import led_init
    #led =  led_init()
    
    from ..octopus import w
    #w = w_connect()
    if (not _is_wifi_connect):
        w = w(echo = False)
        # _is_wifi_connect = True # todo
    
    print('-' * SEPARATOR_WIDTH)
    # print("_is_wifi_connect", _is_wifi_connect)
    print('IP address:', terminal_color(w.sta_if.ifconfig()[0]))
    print('subnet mask:', w.sta_if.ifconfig()[1])
    print('gateway:', w.sta_if.ifconfig()[2])
    print('DNS server:', w.sta_if.ifconfig()[3])
    from ubinascii import hexlify
    try:
        MAC = terminal_color(hexlify(w.sta_if.config('mac'),':').decode())
    except:
        MAC = "Err: w.sta_if"
    print("HWaddr (MAC): " + MAC)
    print('-' * SEPARATOR_WIDTH)


@command
def cat(file='/main.py', title=False):  # concatenate - prepare
    """print data: f("filename") """
    fi = open(file, 'r')
    if title:
        from .terminal import printTitle
        printTitle("file > " + file)
        # file statistic
        lines = 0
        words = 0
        characters = 0
        for line in fi:
            wordslist = line.split()
            lines = lines + 1
            words = words + len(wordslist)
            characters = characters + len(line)

        print("Statistic > lines: " + str(lines) + " | words: " + str(
            words) + " | chars: " + str(characters))
        print('-' * SEPARATOR_WIDTH)
        fi = open(file, 'r')
    for line in fi:
        print(line, end="")
    print()
    globals()["cat"] = cat


@command
def edit(file="/main.py"):
    from .editor import edit
    edit(file)


@command
def ls(directory="", line=False, cols=2, goPrint=True):
    from .terminal import terminal_color
    debug = False
    # if goPrint: printTitle("list > " + directory)
    # from os import listdir
    from uos import ilistdir
    from os import stat
    ls_all = ilistdir(directory)
    if debug:
        print(directory)
        print(str(ls_all))
    # ls.sort()
    if goPrint:
        col = 0
        print("%8s %s " % ("d/[B]", "name"))
        for f in ls_all:
            if f[1] == 16384:
                # print(terminal_color(str(f[0])))
                print("%8s %s " % ("---", terminal_color(str(f[0]))))

            if f[1] == 32768:
                # print(str(f[0]) + "" + str(stat(f[0])[6]))
                try:
                    print(
                        "%8s %s" % (str(stat(f[0])[6]), terminal_color(str(f[0]), 36)))
                except:
                    # print("%8s %s" % ( str(stat(directory+f[0])[6]), terminal_color(str(f[0]),36)))
                    print("%8s %s" % ("?", terminal_color(str(f[0]), 36)))

            """if line:
                print("%25s" %  f,end="")
                col += 1
                if col % cols:
                    print()
            else:"""
        print()
    return ls
    # globals()["ls"]=ls


@command
def cp(fileSource, fileTarget="/main.py"):
    from .terminal import printTitle, runningEffect
    printTitle("file_copy to " + fileTarget)
    print("(Always be careful)")
    fs = open(fileSource)
    data = fs.read()
    fs.close()

    runningEffect()
    ft = open(fileTarget, 'w')
    ft.write(data)
    ft.close()
    print(" ok")


@command
def mkdir(directory):
    try:
        from os import mkdir
        mkdir(directory)
    except Exception as e:
        print("Exception: {0}".format(e))


@command
def rm(file=None):
    if file:
        from .terminal import printTitle, runningEffect
        printTitle("remove file > " + file)
        try:
            from os import remove
            print("(Always be careful)")
            remove(file)
            runningEffect()
        except Exception as e:
            print("Exception: {0}".format(e))
    else:
        print("Input param: path + file name")


@command
def find(xstr, directory="examples"): # ?getcwd()
    from os import listdir
    from .terminal import printTitle
    printTitle("find file > " + xstr)
    ls = listdir(directory)
    ls.sort()
    for f in ls:
        if f.find(xstr) > -1:
            print(f)


@command
def df(echo=True):
    from os import statvfs
    if echo:
        print("> flash info: " + str(statvfs("/")))
    flash_free = int(statvfs("/")[0]) * int(statvfs("/")[3])
    if echo:
        print("> flash free: " + str(flash_free))
    return flash_free


@command
def free(echo=True):
    from gc import mem_free
    if echo:
        print("--- RAM free ---> " + str(mem_free()))
    return mem_free()


@command
def top():
    import os, ubinascii, machine
    from time import ticks_ms, ticks_diff
    from machine import RTC
    import esp32

    from .terminal import terminal_color, printBar

    def add0(sn):
        ret_str = str(sn)
        if int(sn) < 10:
            ret_str = "0" + str(sn)
        return ret_str

    def get_hhmmss(separator=":"):
        rtc = RTC()  # real time
        # get_hhmm(separator) | separator = string: "-" / " "
        hh = add0(rtc.datetime()[4])
        mm = add0(rtc.datetime()[5])
        ss = add0(rtc.datetime()[6])
        return hh + separator + mm + separator + ss

    def f2c(Fahrenheit):
        Celsius = (Fahrenheit - 32) * 5.0/9.0
        return Celsius

    bar100 = 30
    print(terminal_color("-" * (bar100 + 20)))
    print(terminal_color("free Memory and Flash >"))
    ram100 = 128000
    b1 = ram100 / bar100
    ram = free(False)
    print("RAM:   ", end="")
    printBar(bar100 - int(ram / b1), int(ram / b1))
    print(terminal_color(str(ram / 1000) + " kB"))

    flash100 = 4000000
    b1 = flash100 / bar100
    flash = df(False)
    print("Flash: ", end="")
    printBar(bar100 - int(flash / b1), int(flash / b1))
    print(terminal_color(str(flash / 1000) + " kB"))

    print(terminal_color("-" * (bar100 + 20)))
    uid = ubinascii.hexlify(machine.unique_id()).decode()
    print(terminal_color("> ESP32 unique_id: ") + str(uid))
    print(terminal_color("> uPy version:  ") + str(os.uname()[3]))
    print(terminal_color("> octopusLAB shell: ") + __version__)

    print(terminal_color("-" * (bar100 + 20)))
    raw_c = int(f2c(esp32.raw_temperature())*10)/10
    print(terminal_color("> proc. raw_temperature: ") + terminal_color(str(raw_c) + " C", 31))

    now = ticks_ms()
    for job_id, job_info in _background_jobs.items():
        job_duration = ticks_diff(now, job_info['start_time'])
        job_command = ' '.join(job_info['command_list'])
        print(
            terminal_color(
                "[{job_id}] {job_duration}s {job_command}".format(
                    job_id=job_id,
                    job_duration=job_duration / 1000,
                    job_command=job_command,
                ),
                35
            ),
        )
    print(terminal_color(get_hhmmss()), 36)


@command
def ping(url='google.com'):
    from .uping import ping
    ping(url)


@command # TODO
def upgrade(urlTar="https://octopusengine.org/download/micropython/stable.tar"):
    from ..setup import deploy
    from .terminal import printTitle
    printTitle("upgrade from url > ")
    print(urlTar)
    try:
        deploy(urlTar)
    except Exception as e:
        print("Exception: {0}".format(e))


@command
def clear():
    print(chr(27) + "[2J")  # clear terminal
    print("\x1b[2J\x1b[H")  # cursor up


@command
def run(file="/main.py"):
    exec(open(file).read(), globals())


@command
def ver():
    print(__version__)


@command
def wget(urlApi="https://www.octopusengine.org/api"):
    # https://www.octopusengine.org/api/message.php
    # get api text / jsoun / etc
    from ..octopus import w
    try:
        w(echo = False)
    except Exception as e:
        print("Exception: {0}".format(e))

    from urequests import get
    urltxt = urlApi + "/text123.txt"
    try:
        response = get(urltxt)
        dt_str = response.text
    except Exception as e:
        print("Err. read txt from URL")
    print(dt_str)


@command
def pwd():
    from uos import getcwd
    print(getcwd())


@command
def cd(directory):
    from uos import chdir
    chdir(directory)


@command
def exit():
    raise SystemExit


@command
def help():
    print("octopusLAB - simple shell help:")
    cat("util/octopus_shell_help.txt", False)
    print()


class _release_cwd:
    def __enter__(self):
        from uos import getcwd
        self.current_directory = getcwd()

    def __exit__(self, type, value, traceback):
        from uos import chdir
        chdir(self.current_directory)


def parse_input(input_str):
    command_list = input_str.strip().split()

    # support for background jobs via `&` at the end of line
    # TODO tests:
    # arguments = ['one', 'two', 'three&']
    # arguments = ['one', 'two', 'three', '&']
    # arguments = ['&']
    # arguments = ['one&']
    # arguments = ['one', 'two', 'three']
    # arguments = ['one']
    # arguments = []
    if command_list and command_list[-1][-1] == '&':
        run_in_background = True
        command_list[-1] = command_list[-1][:-1]
        if not command_list[-1]:
            command_list = command_list[:-1]
    else:
        run_in_background = False

    return command_list, run_in_background


def shell():
    from uos import getcwd
    from sys import print_exception
    from .terminal import terminal_color
    with _release_cwd():
        while True:
            try:
                input_str = input(
                    terminal_color("uPyShell", 32) + ":~" + getcwd() + "$ "
                )
            except KeyboardInterrupt:
                print('^C')
                continue
            except EOFError:
                print()
                return

            command_list, run_in_background = parse_input(input_str)

            if not command_list:
                continue

            # hacky support for run ./file.py
            if command_list[0][:2] == "./":
                cmd = command_list.pop(0)
                command_list = ['run', cmd[2:]] + command_list

            cmd, *arguments = command_list

            try:
                func = _command_registry[cmd]
            except KeyError:
                print('{cmd}: command not found'.format(cmd=cmd))
                continue

            if run_in_background:
                func = _background_func(func, command_list)

            try:
                func(*arguments)
            except Exception as exc:
                print_exception(exc)
            except KeyboardInterrupt:
                print('^C')
            except SystemExit:
                return
