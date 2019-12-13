# This file is main part of the octopusLAB project
# The MIT License (MIT)
# Copyright (c) 2016-2020 Jan Copak, Petr Kracik, Vasek Chalupnicek

# 

# ******** alfa prepare / beta test **********
# todo: Env.set/get


class Octopus:
    def __init__(self, test):
        self.version = "2.00"
        self.test = test

    def hello(self,name = "octopus"):
        print("hello " + name)
# **********************************
