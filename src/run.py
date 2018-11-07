#! /usr/bin/env python3


""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    run.py 

    sample commands:

       $ run.py t data_1
       $ run.py c2 cvt_1
       $ run.py ca cvt_15_2

------------------------------------"""

import pandas as pd
import matplotlib.pyplot as mp
import sys
import time

import truth
import power
import cvt
import catch
import apply_catch

action = sys.argv[1]

if not action == 'h' or action == 'help':
    name = sys.argv[2]


data_sets = [
    'data_1',
    'data_2',
    'data_3',
    'data_4',
    'data_5',
    'data_6',
    'data_7',
    'data_8',
    'data_9',
    'data_10',
    'data_11',
    'data_12',
    'data_13',
    'data_14',
    'data_15',
]


cols   = ['Re(Zero)', 'Im(Zero)']

def mk_truth(x):
    dfs = truth.make(x)
    truth.save(dfs, x)

"""
def mk_nztruth(x):
    dfs = truth.make_nz(x)
    truth.save_nz(dfs, x)
"""
    
def mk_all_truths():
    for x in data_sets:
        mk_truth(x)

def zn_save(name):
    """
    saves zero and negative sequence data on the 
    nowhere to be used data directory, named out
    """
    c = cvt.cvt(name)
    c.add_symmetric()
    c.zn_cols()
    c.save(sep = '\t')

def z_save(name):
    """
    saves zero sequence data on the directory 
    named out, where we find nowhere used data
    """
    c = cvt.cvt(name)
    c.add_symmetric()
    c.z_cols()
    c.save(sep = '\t')

def save_input(name):
    """
    saves 'symmetric' data on the input directory 
    where we find the input to the fault detection
    """
    c = cvt.cvt(name)
    c.basic()
    c.add_symmetric()
    c.datatype = 'input'
    c.save_input()

    
def zn_plot(name):
    c = cvt.cvt(name)
    c.basic()
    c.add_symmetric()
    ax = c.zn_plot()
    mp.show()

def z_plot(name):
    c = cvt.cvt(name)
    c.basic()
    c.add_symmetric()
    ax = c.z_plot()
    mp.show()

def hepl():
    print()
    print('\t  t: make truth files (which are used for making input)')
    print('\t  p: plot abs values of the zero and negative sequences')
    print('\t zp: plot Re and Im of the zero sequence')
    print('\t  s: make and save abs values of the zero and negative sequences')
    print('\t zs: make and save Re and Im of the zero sequence')
    print('\t  i: make and save input data')
    print('\t  c: find, using Re(Zero) only, and classify punctured capacitors ')
    print('\t ca: c with plots of analysis data')
    print('\t c2: find, using Re(Zero) and Im(Zero), and classify punctured capacitors')
    print('\tc2a: c2 with plots of analysis data')
    print()


if action == 't' or action == 'truth':
    if name == 'all':
        mk_all_truths()
    else:
        mk_truth(name)

elif action == 'p' or action == 'zn_plot':
    zn_plot(name)

elif action == 'zp' or action == 'z_plot':
    z_plot(name)

elif action == 's' or action == 'zn_save':
    zn_save(name)

elif action == 'zs' or action == 'z_save':
    z_save(name)

elif action == 'i' or action == 'save_input':
    save_input(name)

elif action == 'c' or action == 'classify':
    catch.catch(name, cols, 0)

elif action == 'ca':
    catch.catch(name, cols, 1)

elif action == 'c2' or action == 'classify2':
    start_time = time.time()
    catch.catch2(name, cols, 0)
    print("--- %s seconds ---" % round(time.time() - start_time, 3))
    print()

elif action == 'ca2':
    start_time = time.time()
    catch.catch2(name, cols, 1)
    print("--- %s seconds ---" % round(time.time() - start_time, 3))
    print()

elif action == 'ac2':
    start_time = time.time()
    apply_catch.catch2(name, cols, 0)
    print("--- %s seconds ---" % round(time.time() - start_time, 3))
    print()

elif action == 'h' or action == 'help':
    hepl()
