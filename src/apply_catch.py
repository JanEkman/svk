#! /usr/bin/env python3


""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    catch.py 

    catch cvt faults
     
    
    For detected anomalies 3 situations are revealed that 
    may be chosen tp supress faults to be reported:

    (i)   duplication: closeness in time to previous alarm

    (ii)  noise: clearly anomalous maximum or minimum in 
          the reference data used for detecting the alarm

    (iii) unstanbility: the std of the reference data is
          large enough for putting the classification at stake
    

------------------------------------"""


from datetime import datetime as time
from datetime import timedelta as delta
import numpy as np
import cvt
import inference as inf
import common
import plot
import matplotlib.pyplot as mp
import pandas as pd
import apply_batches as batches
import classify as cly

pd.set_option('expand_frame_repr', False)


"""

   parameter settings controlling the 
   classification of found events

"""
n1    = 20     # size of predessor batch 
n2    = 1      # size of successor batch
start = 50     # the number of samples in the start to ignore
p     = 1e-6   # alarm probability level
eps   = 1e-20  # offset added to normality for plotting the neglog of it
w     = 30     # the width of the analysed parts around the alarms
gap   = 10     # the gap on each side of the alarm not analysed
stdlim= 0.05   # battch std limit for unstable situation
spike = 3.5    # point std limit for noise

# col   = 'Re(Zero)'  # the col. with the values used for anomaly detection



def phase_to_phase_voltage(df):
    """
    220 or 400
    """
    v = df[100:200]['u1'].mean()   
    p = v * np.sqrt(3)/1000 # phase to phase voltage in kV
    if (p > 200) and  (p < 250):
        return '220'
    if (p > 350) and  (p < 450):
        return '400'
    return 'none'


def stats(n):
    """
    for finding anomalies more data is produced in case 
    the successor batch has more than one data point
    """
    if n == 1:
        return ['m', 's', 'pm', 'ps' ]
    return ['m1', 'm2_'+str(n2), 's1', 's2', 'm1_'+str(n1), 'ps1' ]


def find_alarms(c, col, start):
    
    df      = c.df[['time', col]]
    df      = batches.alarm(df, p, col, n1, n2, stats(n2))
    dfa     = df[df['alarm'] == 1]
    alarms  = dfa.index
    alarms  = [ [i, dfa['time'][i]] for i in alarms if i > start]
    return df, alarms



def find_alarms2(c, cols, start):

    ws      = n1
    df      = c.df[['time'] + cols ]
    df      = batches.alarm2(df, p, cols, ws)
    dfa     = df[df['alarm'] == 1]
    alarms  = dfa.index
    alarms  = [ [i, dfa['time'][i]] for i in alarms if i > start]
    return df, alarms


def parts(df, i, w, gap):
    """
    the parts of the data used for fault classification
    """
    df  = df[['time', 'Re(Zero)', 'Im(Zero)']]
    df  = df[ (df.index >= i- w - gap) & (df.index <= i + w + gap)]
    df1 = df[ df.index < i-gap ]
    df2 = df[ df.index > i+gap ]
    return df1, df2

def classify_one_alarm(c, a, voltage, w, gap):
    """
    the data in df1 and df2 may be used for further analysing
    the alarm and used for impove the classification
    """

    [i, time] = a
    
    df1, df2 = parts(c.df, i, w, gap)
    d1 = df1.describe()
    d2 = df2.describe()
    re1 = d1['Re(Zero)']['mean']
    re2 = d2['Re(Zero)']['mean']
    im1 = d1['Im(Zero)']['mean']
    im2 = d2['Im(Zero)']['mean']

    std_re1 = d1['Re(Zero)']['std']
    std_re2 = d2['Re(Zero)']['std']
    std_im1 = d1['Im(Zero)']['std']
    std_im2 = d2['Im(Zero)']['std']

    min_re1 = (re1 - d1['Re(Zero)']['min']) / std_re1
    min_re2 = (re2 - d2['Re(Zero)']['min']) / std_re2
    min_im1 = (im1 - d1['Im(Zero)']['min']) / std_im1
    min_im2 = (im2 - d2['Im(Zero)']['min']) / std_im2

    max_re1 = (d1['Re(Zero)']['max'] - re1) / std_re1
    max_re2 = (d2['Re(Zero)']['max'] - re2) / std_re2
    max_im1 = (d1['Im(Zero)']['max'] - im1) / std_im1
    max_im2 = (d2['Im(Zero)']['max'] - im2) / std_im2


    # std = max(std_re1, std_re2, std_im1, std_im2)

    re = re2 - re1
    im = im2 - im1
    a = cly.classify(time, voltage, re, im)

    stddict = {
        'std_re1' : std_re1, 
        'std_re2' : std_re2, 
        'std_im1' : std_im1, 
        'std_im2' : std_im2,
    }
    
    for std in stddict:
        if stddict[std] > stdlim:
            a.unstable += [std] 
            a.std = stddict[std]
    a.spikes = []
    if (min_re1 > spike) or (max_re1 > spike):
        a.spikes += ['re1']
    if (min_re2 > spike) or (max_re2 > spike):
        a.spikes += ['re2']
    if (min_im1 > spike) or (max_im1 > spike):
        a.spikes += ['im1']
    if (min_im2 > spike) or (max_im2 > spike):
        a.spikes += ['im2']
    

    return a


def classify(c, alarms, voltage, w, gap):
    """
    add the fault class to each alarm in alarms
    """
    b=[]
    first_alarm = True
    for a in alarms:
        
        alarm = classify_one_alarm(c, a, voltage, w, gap)

        [i, time] = a
        if first_alarm:
            alarm.gap = 1e5
        else:
            alarm.gap = (time-pretime).total_seconds()
            

        b += [alarm]
        pretime = time
        first_alarm = False
    return b


def print_faults(alarms, name, voltage, dec = 4):


    print()
    if alarms == []:
        print ('\t No alarms in', name, ' (',voltage,')')
    else:
        print('\tAlarms', name, ' (',voltage,')')
        print('\ntime\t\t\tgap[s]\tfault type\tdetection')
    print()

    for a in alarms:
        print(a.time, end = '\t')
        if a.gap > 1e5: 
            print('large', end = '\t') 
        else:
            print(int(a.gap), end = '\t') 
        if a.phase == 'none':
            print('Unknown\t', end = '\t')
        else: 
            # print('Capacitor fault    stack', a.stack, '\tphase:', a.phase)
            print('Capacitor', a.stack+a.phase, end = '\t')
            # print('\tre:', round(a.re,dec), '\tim:', round(a.im,dec), '\t3abs:', round(a.r*3,dec))
    
        if not a.unstable == []:
            # print('std >',stdlim, '\t', end = ' ')
            print('unstable' '\t', end = ' ')
            for std in a.unstable:
                print(std[4:],':', round(a.std, dec) , end = '\t')
            print()


        if not (a.spikes == []):
            if not a.unstable == []:
                print(end = '\t\t\t\t\t\t')

            print('noisy\t\t ', end = '')
            for s in a.spikes:
                print(s, end = '  ')

            print()
        elif a.unstable == []: 
            print()
    print()

def plot_analysis(c, df, col, name):

    df['neg_log_norm'] = -np.log(df['norm'] + eps)/10
    df['lim'] = -np.log(p + eps)/10

    ax0 = plot.alarm_plot(df, p, name, n1, n2)
    ax1 = plot.stat_plot(df, [col, 'm', 'pm'], name, style = 'o', msize = 4)
    ax2 = plot.sym_plot(c.df, [col], name, style = 'o', unit = '%')
    ax3 = plot.sym_plot(c.df, ['Re(Zero)', 'Im(Zero)'], name, style = 'o', unit = '%')
    ax8 = plot.sym_plot(c.df, ['Re(Negative)', 'Im(Negative)'], name, style = 'o', unit = '%')
    
    ax4 = plot.sym_plot(c.df, ['Theta(Zero)'], name, style = 'o', unit = '%')
    ax5 = plot.stat_plot(df, ['ps'], name, 'Standard deviation', style = 'o')
    ax6 = plot.stat_plot(df, ['neg_log_norm', 'lim'], name, style = '-')


    ax7 = c.df.plot(
        'Re(Zero)', 
        ['Im(Zero)'], 
        xlim = [-1.5, 1.5],
        ylim = [-1.5, 1.5],
        style = '-', 
        legend = True)


    ax9 = c.df.plot(
        'Re(Negative)', 
        ['Im(Negative)'], 
        xlim = [-0.25, 2], 
        ylim = [-0.25, 2], 
        style = '-', 
        legend = True)


    mp.show()


def plot_analysis2(c, df, cols, name):

    df['neg_log_norm'] = -np.log(df['norm'] + eps)/10
    df['lim'] = -np.log(p + eps)/10

    ax0 = plot.alarm_plot(df, p, name, n1, n2)
    ax1 = plot.sym_plot(c.df, cols, name, style = 'o', unit = '%')
    ax2 = plot.sym_plot(c.df, ['Re(Zero)', 'Im(Zero)'], name, style = 'o', unit = '%')
    # ax3 = plot.sym_plot(c.df, ['Re(Negative)', 'Im(Negative)'], name, style = 'o', unit = '%')
    # ax4 = plot.sym_plot(c.df, ['Theta(Zero)'], name, style = 'o', unit = '%')
    ax5 = plot.stat_plot(df, ['neg_log_norm', 'lim'], name, style = 'o')



    mp.show()



def catch(name, cols, pa, w=w, gap=gap, start=start):
    c = cvt.cvt(name)
    c.read_input()
    voltage = phase_to_phase_voltage(c.df)
    df, alarms = find_alarms(c, cols[0], start)
    alarms = classify(c, alarms, voltage, w, gap)
    print_faults(alarms, name, voltage)
    if pa:
        plot_analysis(c, df, cols[0], name)

def catch2(name, cols, pa, w=w, gap=gap, start=start):
    c = cvt.cvt(name)
    c.read_input()
    voltage = phase_to_phase_voltage(c.df)
    df, alarms = find_alarms2(c, cols, start)
    alarms = classify(c, alarms, voltage, w, gap)
    print_faults(alarms, name, voltage)

    if pa:
        plot_analysis2(c, df, cols, name)  # should be cols




# catch(name, 1)

