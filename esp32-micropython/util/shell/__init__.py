# This file is part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2020 Jan Copak, Petr Kracik, Vasek Chalupnicek

"""
from util.shell import shell
shell()
> cat / edit / ls / mkdir / cp / rm / find / df ...
---
clt / printHead / printTitle / printLog
last update: 
"""
ver = "0.23 - 18.01.2020"

# toto: ifconfig, ping? 

class Conf:  # for temporary global variables and config setup
      TW = 50  # terminal width


def terminal_color(txt,col=33): # default yellow
    # 30 black / 31 red / 32 green / 33 yellow / 34 blue / 35 violet / 36 cyan 
    # 21 underline
    # print("\033[32mgreen\033[m")
    return "\033[" + str(col) + "m" + str(txt) + "\033[m"


def runningEffect(num = 16):
    from time import sleep_ms
    for ii in range(num):
        print(".",end="")
        sleep_ms(200)


def printBar(num1,num2,char="|",col1=32,col2=33):
    print("[",end="")
    print((("\033[" + str(col1) + "m" + str(char) + "\033[m")*num1),end="")
    print((("\033[" + str(col2) + "m" + str(char) + "\033[m")*num2),end="")
    print("]  ",end="")


def cat(file='main.py', title = False): # concatenate - prepare
    """print data: f("filename") """
    fi = open(file, 'r')
    if title:
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

        print("Statistic > lines: " + str(lines) + " | words: " + str(words) + " | chars: " + str(characters))
        print('-' * Conf.TW)
        fi = open(file, 'r')
    for line in fi:
        print(line, end="")
    globals()["cat"]=cat


def edit(file="main.py"):
    from util.shell.editor import edit
    edit(file)


def getVer():
    return ver


def ls(directory="", line = False, cols = 2, goPrint = True):
    if goPrint: printTitle("list > " + directory)
    from os import listdir
    ls = listdir(directory)
    ls.sort()
    if goPrint:
        col = 0
        for f in ls:
            if line:
                print("%25s" %  f,end="")
                col += 1
                if col % cols:
                    print()
            else:
                print(f)
        print()
    return ls
    #globals()["ls"]=ls


def cp(fileSource, fileTarget="main.py"):

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


def mkdir(directory):
    try:
        from os import mkdir
        mkdir(directory)
    except Exception as e:
        print("Exception: {0}".format(e))


def rm(file = None):
    if file:
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


def find(xstr, directory = "examples"):
    printTitle("find file > " + xstr)
    from os import listdir
    ls = listdir(directory)
    ls.sort()
    for f in ls:
        if f.find(xstr) > -1:
            print(f)


def df(echo = True):
    from os import statvfs
    if echo: print("> flash info: "+str(statvfs("/")))
    flash_free = int(statvfs("/")[0])*int(statvfs("/")[3])
    if echo: print("> flash free: "+str(flash_free))
    return flash_free


def free(echo = True):
    from gc import mem_free
    if echo:
        print("--- RAM free ---> " + str(mem_free()))
    return mem_free()


def top():
    bar100 = 30
    print(terminal_color("-" * (bar100+20)))
    print(terminal_color("free Memory and Flash >"))
    ram100 = 128000
    b1 = ram100/bar100
    ram = free(False)
    print("RAM:   ",end="")
    printBar(bar100-int(ram/b1),int(ram/b1))
    print(terminal_color(str(ram/1000) + " kB"))

    flash100 = 4000000
    b1 = flash100/bar100
    flash = df(False)
    print("Flash: ",end="")
    printBar(bar100-int(flash/b1),int(flash/b1))
    print(terminal_color(str(flash/1000) + " kB"))

    print(terminal_color("-" * (bar100+20)))
    print("octopusLAB shell version: " + getVer())



def upgrade(urlTar = "https://octopusengine.org/download/micropython/stable.tar"):
    printTitle("upgrade from url > ")
    print(urlTar)
    from util.setup import deploy
    try:
        deploy(urlTar)
    except Exception as e:
        print("Exception: {0}".format(e))

def clt():
    print(chr(27) + "[2J") # clear terminal
    print("\x1b[2J\x1b[H") # cursor up


def run(file ="main.py"):
     exec(open(file).read(), globals())

def wget(urlApi ="http://www.octopusengine.org/api"):
    # get api text / jsoun / etc
    from util.octopus import w
    try:
        w()
    except Exception as e:
        print("Exception: {0}".format(e))

    from urequests import get
    urltxt=urlApi+"/text123.txt"
    try:
        response = get(urltxt)
        dt_str = response.text
    except Exception as e:
        print("Err. read txt from URL")
    return dt_str

# --------------------------------------------------------
commandList = ["",""]
def shell():
    subDir = ""
    # todo: curl, wget... 
    commlist = ["","ver","pwd","cd","clear","free","df","top","run","ls","cat","mkdir","rm","find","cp","wget","help","edit","exit"]
    while True:
        try:
            print("\033[32muPyShell\033[m",end="")
            sele = input(":~" + subDir+ "$ ")
            comm = sele.split(" ")
            c1 = comm[0]
            if c1 not in commlist and c1[:2] != "./":
                print(c1, ": command not found")

            if len(comm) > 1:
                c2 = comm[1]
                c2b = True
            else:
                c2 = ""
                c2b = False
            if len(comm) > 2: c3 = comm[2]
            else: c3 = ""

            if sele == "exit":
                # done with editing
                break
            if c1 == "clear": clt()
            if c1 == "ver": print("version: " + getVer())
            if c1 == "pwd": print(subDir)
            if c1 == "free": free()
            if c1 == "df": df()
            if c1 == "top": top()
            if c1[:2] == "./": run(c1[2:])

            if c2b:
                if c1 == "cd":
                    #ls = ls(goPrint=False)

                    subDir = "/"+c2
                    if c2 == "..":
                        subDir =""

                """
                if c1 == "cd":
                    ls = ls(goPrint=False)
                    if c2 in ls
                        subDir = c2
                    else:
                        print(c2 + "dir not found")
                """

                if c1 == "ls": ls(c2)
                if c1 == "cat": cat(c2)
                if c1 == "edit": edit(c2)
                if c1 == "mkdir": mkdir(c2)
                if c1 == "rm": rm(c2)
                if c1 == "find": find(c2)
                if c1 == "run": run(c2)
                if c1 == "wget": print(wget(c2))

                if c1 == "cp": cp(c2) # todo c3
            else:
                if c1 == "run": run()
                if c1 == "ls": ls(subDir)
                if c1 == "cat": cat()
                if c1 == "edit": edit()
                if c1 == "wget": print(wget())

            if c1 == "help":
                print("octopusLAB - simple shell help:")
                cat("util/octopus_shell_help.txt", False)
                print()
        except Exception as e:
            print("Shell Err. > Exception: {0}".format(e))

# --------------------------------------------------------

def printHead(s):
    print()
    print('-' * Conf.TW)
    print("[--- " + s + " ---] ")


def printTitle(t,w=Conf.TW):
    print()
    print('=' * w)
    print("|",end="")
    print(t.center(w-2),end="")
    print("|")
    print('=' * w)


def printLog(i,s=""):
    print()
    print('-' * Conf.TW)
    print("[--- " + str(i) + " ---] " + s)


def printInfo():
    import gc #mem_free
    print("> mem_free: "+str(gc.mem_free()))
    df()


def printMachineInfo():
    import machine
    print("> machine.freq: "+str(machine.freq()))