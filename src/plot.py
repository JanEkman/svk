#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    plot.py 

 ------------------------------------"""

import pandas as pd
import numpy  as np
import matplotlib.pyplot as mp

ts_figsize = (16, 5)

def sym_plot(df, cols, name, style = '-', unit = '%', msize = 2):
    t = ':  Voltage Unbalance -- ' 
    ax = df.plot(
        'time',
        cols,
        figsize = ts_figsize,
        style = style,
        markersize = msize,
        fontsize = 10,
        # title = 'Dataset 2018-90-18 '+nr,
        # ylim = [-1500, 1500], # needed for dataset 2
        legend = True)
    title  = 'Dataset '+name+ t
    # title += titles[int(nr)-1]
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel('Time',  fontsize = 20)
    ax.set_ylabel('Unbalance [ ' + unit + ' ]', fontsize = 20)
    ax.legend(loc=2,prop={'size':15})
    return ax


def stat_plot(df, cols, name, title = '', style = 'o', msize = 2):
    ax = df.plot(
        'time',
        cols,
        figsize = ts_figsize,
        style = style,
        markersize = msize,
        fontsize = 10,
        # title = 'Dataset 2018-90-18 '+nr,
        # ylim = [-1500, 1500], # needed for dataset 2
        legend = True)
    title  = 'Dataset '+name+ title
    # title += titles[int(nr)-1]
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel('Time',  fontsize = 20)
    # ax.set_ylabel('Unbalance [ ' + unit + ' ]', fontsize = 20)
    ax.legend(loc=2,prop={'size':15})
    return ax

def alarm_plot(df, p, name, n1, n2, style = 'o', msize = 10):
    t = ': Alarms at normality level  ' 
    t += str(p) + '     n1 = ' + str(n1) + '   n2 = ' + str(n2)
    ax = df.plot(
        'time',
        ['alarm'],
        figsize = ts_figsize,
        style = style,
        markersize = msize,
        fontsize = 10,
        # title = 'Dataset 2018-90-18 '+nr,
        # ylim = [-1500, 1500], # needed for dataset 2
        legend = True)
    title  = 'Dataset '+name+ t
    # title += titles[int(nr)-1]
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel('Time',  fontsize = 20)
    ax.set_ylabel('Alarm', fontsize = 20)
    ax.legend(loc=2,prop={'size':15})
    return ax
 
def zn_plot(df, name, style = '-'):
    cols = ['Abs(Zero)', 'Abs(Negative)']
    return sym_plot(df, cols, name, style)

def z_plot(df, name, style = '-'):
    cols = ['Re(Zero)', 'Im(Zero)']
    return sym_plot(df, cols, name, style)


def plot_polar(df):
    df = df[['time', 'Abs(Zero)', 'Theta(Zero)']]
    ax0 = plot.sym_plot(c.df, ['Theta(Zero)'], '1', style = 'o', unit = 'degrees')
    ax1 = plot.sym_plot(c.df, ['Re(Zero)',  'Im(Zero)', 'Abs(Zero)'], '1', style = 'o')
    return ax0, ax1
   
