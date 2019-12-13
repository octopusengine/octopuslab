# This file is part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2019 Jan Copak, Petr Kracik, Vasek Chalupnicek

"""
cat / ls / mkdir / cp / rm / find / df
---
clt / printHead / printTitle / printLog
last update: 13.12.2019
"""

class Conf:  # for temporary global variables and config setup
      TW = 50  # terminal width


def runningEffect(num = 16):
    from time import sleep_ms
    for ii in range(num):
        print(".",end="")
        sleep_ms(200)


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


def ls(directory="", line = False, cols = 2):
    printTitle("list > " + directory)
    from os import listdir
    ls = listdir(directory)
    ls.sort()
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


def df():
    from os import statvfs
    print("> flash info: "+str(statvfs("/")))
    print("> flash free: "+str(int(statvfs("/")[0])*int(statvfs("/")[3])))


def free(echo = True):
    from gc import mem_free
    if echo: 
        print("--- RAM free ---> " + str(mem_free()))
    return mem_free()


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

# ------------------------------------------------------------------

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
