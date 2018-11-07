#! /usr/bin/env python3


""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    batches.py 

------------------------------------"""

import pandas as pd
import numpy as np
import inference as inf
import scipy.stats as ss
from numpy import linalg as la


# pd.set_option('expand_frame_repr', False)


def batch_mean(col, size, mp = 0):
    y = col.rolling(window=size, min_periods =0 ).mean()
    return y

def batch_std(col, size):
    y = col.rolling(window=size, min_periods =0 ).std()
    return y

def add_mean(df, col, mcol, n, freq):
    """
    on each freq row add the mean of the last n rows
    """
    df.is_copy = False
    r = df.index % freq == freq-1
    x = batch_mean(df[col], n)
    df[mcol] = np.where(r, x, 0)

def add_std(df, col, scol, n, freq):
    """
    on each freq row add the std of the last n rows
    """
    df.is_copy = False
    r = df.index % freq == freq-1
    x = batch_std(df[col], n)
    df[scol] = np.where(r, x, 0)

def compact(df, freq, drop = False):
    r = df.index % freq == freq-1
    df = df[r]
    if drop:
        df = df.reset_index(drop = True)
    return df 

def shift(df, c, pc, k):
    df[pc] = df[c].shift(k)

def add_set_normality(df, col, n1, n2, statistics, delay =1):
    """
    compare a set d1 of previous n1 samples with d2, the last
    n2 samples, where d1 ends delay*n2 steps ahead of the end
    of d2. The comparision concernes column col.
    """
    
    [m1, m2, s1, s2, pm1, ps1] = statistics 
    
    add_mean(df, col, m1, n1, n2)
    add_std( df, col, s1, n1, n2)


    add_mean(df, col, m2, n2, n2)
    add_std( df, col, s2, n2, n2)

    shift(df, m1, pm1,  n2 * delay)
    shift(df, s1, ps1,  n2 * delay)

    df = compact(df, n2, drop = True)
    df = df.drop([m1, s1], axis=1)    
    df = df.dropna()
    df['norm'] = inf.set_norm(n1, n2, df[pm1], df[m2], df[ps1], df[s2])
    return df

def add_sample_normality(df, col, n, statistics, delay =1):
    [m, s, pm, ps] = statistics 
    add_mean(df, col, m, n, 1)
    add_std( df, col, s, n, 1)
    shift(df, m, pm,  delay)
    shift(df, s, ps,  delay)
    # df = df.drop([m, s], axis=1)     
    df = df.dropna()  
    df.is_copy = False
    df['norm'] = inf.sample_norm(df[col], n, df[pm], df[ps])
    return df


def diagonal_matrix(x):
    return  np.mat([ [x[0], 0 ], [ 0, x[1]] ])

def transform(cov):
    l, R = la.eig(cov)
    L    = diagonal_matrix(l)
    S    = np.sqrt(L)
    return (R*S).T, L


def normality(z, m, cov, n, c_prior = 0.5):
    
    def gam(z, m, v, n):
        n1 = n + 1
        q  = (n-1) *v
        d  = n * (z - m)**2
        b  = d / q
        return n1 / (b + n1)

    T, L = transform(cov)
    v    = np.diag(L*L) 

    """
    print('\n ------- \n')
    print('z         = ', z)
    print('np.mat(z) = ', np.mat(z.values) )
    print('T         = ', T)
    print('\n ------- \n')
    """

    z    = (T* np.mat(z).T).flat
    m    = (T* np.mat(m).T).flat

    k    = (c_prior+ n-2)/2
    g0   = gam(z[0], m[0], v[0], n)
    g1   = gam(z[1], m[1], v[1], n)
    norm = (n/(n+1)) * g0**k * g1**k

    return norm

def add_sample_normality2(df, cols, ws, prior =0.5, delay =1):

    dfc     = df[cols]
    df_cov  = dfc.rolling(window=ws, min_periods=ws).cov()
    df_eig  = df_cov.groupby(level=0).apply(inf.eig).shift(delay)
    df_mean = dfc.rolling(window=ws, min_periods=ws).mean().shift(delay)
    dfa     = pd.concat([dfc, df_eig, df_mean], axis=1)
    dfa.columns = cols + ['Eig', 'Re_mean', 'Im_mean']
    fn      = lambda x: inf.normalize(x, cols, ws, prior)
    norm    = dfa[ws:].apply(fn, axis = 1)
    init    = pd.Series(np.ones(ws))
    norm    = init.append(norm)
    dfcols  = list(df.columns)
    df      = pd.concat([df, norm], axis = 1)
    df.columns = dfcols + ['norm']

    return df



def alarm(df, p, col, n1, n2, statistics, delay =1):
    if n2 == 1:
        df = add_sample_normality(df, col, n1, statistics, delay)
    if n2 > 1:
        df = add_set_normality(df, col, n1, n2, statistics, delay)
    df.is_copy = False
    df['alarm'] = df['norm'] < p
    df['alarm'] = df['alarm'].apply(int)
    return df


def alarm2(df, p, cols, ws, prior =0.5, delay =1):
    print(cols)
    df = add_sample_normality2(df, cols, ws, prior, delay)
    df.is_copy = False
    df['alarm'] = df['norm'] < p
    df['alarm'] = df['alarm'].apply(int)

    # print(df[0:10])
    return df


