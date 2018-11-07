#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    common.py 

 ------------------------------------"""

import pandas as pd
import numpy  as np
from datetime import datetime as time
from datetime import timedelta as delta
from dateutil import parser

import places_and_events as pe


basiccols = [
    'time', 
    'phase1',
    'phase2',
    'phase3',
    'u1',
    'u2',
    'u3',
]

statuscols = [
    'cap_u1c1',
    'cap_u2c1',
    'cap_u3c1',
    'cap_u1c2',
    'cap_u2c2',
    'cap_u3c2',
    'fuse_u1',
    'fuse_u2',
    'fuse_u3',
    'unbalance',
    'other',
]

zn_cols = [
    'time', 
    'Abs(Zero', 
    'Abs(Negative)'
]

zero_cols = [
    'time', 
    'Re(Zero)', 
    'Im(Zero)',
    'Abs(Zero)',
    'Theta(Zero)',
]

def str2float(x):
    if isinstance(x, str):
        return float(x.replace(',','.'))
    elif isinstance(x, int) or isinstance(x, float):
        return x
    print(x, 'replaced by', np.nan)
    return np.nan

def arctan360(x,y):
    """
    t = arctan360(x,y) is the correspondence to 
    arctan such that t is in [0, 360], i.e the 
    polar coordinate angle in degrees also the 
    argument of the complex number z = x + iy
    """
    h = 180; a = x<0; b = y<0; z = 1/2 -b
    if not x == 0:
        z = np.arctan(y/x)/np.pi
    return h*(z + a + 2*b*(1-a))

def retype(df):
    """
    retype the 'time' column to datetime type
    and retype the rest of the columns to float
    """
    df['time'] = df['time'].apply(parser.parse)
    for c in df.columns[1:]:
        df[c] = df[c].apply(str2float)
    return df

def read_truth(name):
    f = pe.truth + name + '.csv'
    df = pd.read_csv(f, dtype = str, sep=';')
    return retype(df)

def read_input(name):
    f = pe.inp + name + '.csv'
    df = pd.read_csv(f, dtype = str, sep=';')
    return retype(df)


def save_input(df, name, sep = ';'):
    f = pe.inp + name + '.csv'
    df.to_csv(f, index = False, sep = sep, encoding='utf-8')

def save(df, name, sep = ';'):
    f = pe.out + name + '.csv'
    df.to_csv(f, index = False, sep = sep, encoding='utf-8')


