#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    truth.py 

    make and save the ground truth as specified 
    by the events in places_and_events.py

    places_and_events.py also gives the place
    and name for the truth file 
    

------------------------------------"""



import pandas as pd
import numpy  as np
from datetime import datetime as time
from datetime import timedelta as delta
from dateutil import parser
import places_and_events as pe



origcols = [
    'Datum', 
    'PhaseSymmetryUL1', 
    'PhaseSymmetryUL2', 
    'PhaseSymmetryUL3',
    'UL1', 
    'UL2', 
    'UL3']


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
    'normal',
]


def str2float(x):
    if isinstance(x, str):
        return float(x.replace(',','.'))
    elif isinstance(x, int) or isinstance(x, float):
        return x
    print(x, 'replaced by', np.nan)
    return np.nan


def divide_cols(cols, dc=[]):
    """
    given a col.list [x0, ... , xn],   for 6*k <= n < 6*(k+1) 
    return [[x0, x1, ..., x6],  ..., [x0, xt, ..., xk]], t = k-5
    """
    if len(cols) < 7:
        return dc
    col0  = list([cols[0]])
    head  = list(cols[:7])
    tail  = list(cols[7:])
    return divide_cols(col0 + tail, dc + [head])


def divide_df(df):
    """
    divide the data into one df for each cvt
    """
    dc = divide_cols(df.columns)
    dfs = []
    for cols in dc:
        dfs += [df[cols]]
    return dfs

def retype(df):
    df.columns = basiccols
    df = df.sort_values('time').reset_index(drop=True)    
    df = df.dropna()
    for c in basiccols[1:7]:
        df[c] = df[c].apply(str2float)
    return df

def add_status_cols(df):
    if len(df.columns) == 7:
        for c in statuscols:
            df[c] = 0
    return df

def add_events(df, events):
    """
    for events[i] = [time, col, status]
    df['time'] > time   gives    df[col] = status 
    """
    for e in events:
        time = parser.parse(e[0])
        col = e[1]
        status = int(e[2])
        df[col] = np.where(df['time'] >= time, status, df[col])
    return df


def read_data(ref):
    """
    the data set s14 make pandas read_csv type confused,
    therefore the "dtype = str" is used. The retype
    method takes care of the types, which is to consider 
    all values, but timestamps, to be floats
    """

    space = pe.spaces[ref]
    events  = space['events']
    df = pd.read_csv(space['data'], dtype = str, sep=';')
    if len(df.columns) == 7:
        events = [events]
        df = df[origcols]
    return df, events


def rm_zero(df):
        df = df[ (df['u2'] != 0) | (df['u3'] != 0) ]
        return df

def make(ref):

    df, events = read_data(ref)
    time  = df.columns[0]
    df[time] = df[time].apply(parser.parse)
    dfs = []
    for z in zip(divide_df(df), events):
        df = retype(z[0])
        df = rm_zero(df)
        df = add_status_cols(df)
        df = add_events(df, z[1])
        dfs += [df]
    return dfs


def save(dfs, ref):

    space = pe.spaces[ref]
    place = pe.truth

    names  = space['names']
    for z in zip(names, dfs):

        name = z[0]
        df   = z[1]
        f     = place + name + '.csv'
        print('saving', f)
        df.to_csv(f, index = False, sep =';', encoding='utf-8')
