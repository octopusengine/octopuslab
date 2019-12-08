# This file is part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2019 Jan Copak, Petr Kracik, Vasek Chalupnicek

# this module is "octopus commander" - for other modules
"""
cat / ls / cp
---
clt / printHead / printTitle / printLog
"""


class Conf:  # for temporary global variables and config setup
      TW = 50  # terminal width


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


def ls(directory=""):
    printTitle("list > " + directory)
    from os import listdir
    ls = listdir(directory)
    ls.sort()
    for f in ls:
        print(f)
    #globals()["ls"]=ls


def cp(fileSource, fileTarget="main.py"):
    printTitle("file_copy to " + fileTarget)
    print("(Be careful)")
    fs = open(fileSource)
    data = fs.read()
    fs.close()
    for ii in range(12):
        print(".",end="")
        sleep_ms(300)
    ft = open(fileTarget, 'w')
    ft.write(data)
    ft.close()
    print(" ok")


def clt():
    print(chr(27) + "[2J") # clear terminal
    print("\x1b[2J\x1b[H") # cursor up


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
