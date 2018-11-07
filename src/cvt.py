#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    cvt.py 

 ------------------------------------"""

# import matplotlib.pyplot as mp
import pandas as pd
import common
import power
import plot

#import places_and_events as pe

class cvt:
    def __init__(I, name):
        I.name = name
        I.datatype = 'null'

    def read_truth(I):
        I.df = common.read_truth(I.name)
        I.datatype = 'truth'

    def read_input(I):
        I.df = common.read_input(I.name)
        I.datatype = 'input'

    def dropna(I):
        I.df = I.df.dropna()

    def add_symmetric(I):
        if I.datatype == 'null':
            I.basic()
        if I.datatype == 'truth' or I.datatype == 'basic':
            I.df = power.add_symmetric(I.df)
        if I.datatype == 'basic':
            I.datatype == 'input'
        elif I.datatype == 'truth':
            I.datatype == 'input_and_status'

    def basic(I):
        if I.datatype == 'null':
            I.read_truth()
        I.df = I.df[common.basiccols]
        I.datatype = 'basic'

    def zn_plot(I, style = '-'):
        ax = plot.zn_plot(I.df, I.name, style)
        return ax

    def z_plot(I, style = '-'):
        ax = plot.z_plot(I.df, I.name, style)
        return ax

    def zn_cols(I):
        zn = common.zn_cols
        I.df = I.df[zn]

    def z_cols(I):
        z = common.zero_cols
        I.df = I.df[z]

    def save_input(I, sep = ';'):
        if I.datatype == 'input':
            common.save_input(I.df, I.name, sep)
        else:
            print('data is not of input type')

    def save(I, sep = ';'):
        common.save(I.df, I.name, sep)

        
        
