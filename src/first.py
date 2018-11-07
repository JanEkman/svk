#! /usr/bin/env python3


""" -------------------------------


    Copyright (C) 2018 RISE
    This code was produced by RISE

    first.py 


-------------------------------"""


import pandas as pd
import sys
import cvt

name = sys.argv[1]


def first(name):
    c = cvt.cvt(name)
    c.read_input()
    f = c.df.values[0]
    l = c.df.values[-1]
    print()
    print('first:  [\'' +str(f[0]) +'\', \'normal\', \'1\' ],')
    print('last: ', l[0], '\tvoltages: ', l[2:5])
    print()

first(name)
