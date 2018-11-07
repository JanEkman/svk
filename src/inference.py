#! /usr/bin/env python3


""" -------------------------------


    Copyright (C) 2018 RISE
    This code was produced by RISE

 
    inference.py 

------------------------------------"""

import numpy as np
from numpy import linalg as la
import scipy.stats as ss


def sample_norm(x, n, m, s):
    z = np.sqrt( n/(n+1) ) * (x - m) / s
    p = ss.t.cdf(z, n-1)
    return 1 - abs(2*p -1)


def omega(n1, n2, s1, s2):
    h1 = n1-1
    h2 = n2-1
    h  = h1 + h2
    s  = np.sqrt( (h1*s1**2 + h2*s2**2) / h)
    return s * np.sqrt(1/n1 + 1/n2)

def pooled_F(n1, n2, m1, m2, s1, s2):
    q  = omega(n1, n2, s1, s2)
    x =  (m2 - m1)/q
    return ss.t.cdf(x, n1+n2-2)

def pooled_t(p, n1, n2):
    return ss.t.isf(p/2, n1+n2-2)

def pooled_interval(p, t, m, n1, n2, s1, s2):
    q  = omega(n1, n2, s1, s2)
    z1 = m - t*q
    z2 = m + t*q
    return (z1, z2)

def set_norm(n1, n2, m1, m2, s1, s2):
    p = pooled_F(n1, n2, m1, m2, s1, s2)
    return 1 - abs(2*p -1)

def g(z, m, v, n):
    n1 = n + 1
    q  = (n-1) *v
    d  = n * (z - m)**2
    b  = d / q
    return n1 / (b + n1)
 
def uncorr_normality(z, m, v, n, c_prior = 0.5):
    k = (c_prior+ n-2)/2
    g0 = g(z[0], m[0], v[0], n)
    g1 = g(z[1], m[1], v[1], n)
    norm = (n/(n+1)) * g0**k * g1**k
    return norm


def rotate(df):
    sigma = df.cov()
    mean  = df.mean()
    l, e = la.eig(sigma)
    j0 = int(l[0] < l[1])
    j1 = 1-j0
    l0 = l[j0]
    l1 = l[j1]
    e0 = e[:, j0]
    e1 = e[:, j1] 

    v0 = l0 * np.dot(e0, e0)
    v1 = l1 * np.dot(e1, e1)
    v  = np.array([v0, v1])

    u0 =  df.dot(e0)
    u1 =  df.dot(e1)
    df['u0'] = u0
    df['u1'] = u1

    v  = np.array([v0, v1])
    e  = np.array([e0, e1])
    
    return df, e, v


def diagonal_matrix(x):
    return  np.mat([ [x[0], 0 ], [ 0, x[1]] ])


def n2(z, m, v, n, prior = 0.5):
    k = (n + prior -2)/2
    t =  (n+1)/n
    b0 = (z[0] -m[0])**2 / ((n-1)*v[0])
    b1 = (z[1] -m[1])**2 / ((n-1)*v[1])
    g0 = 1/(t + b0)
    g1 = 1/(t+ b1)
    norm = t ** (2*k - 1) * g0**k * g1**k
    return norm


def eig(x):
   try:                
       e,r = la.eig(x)
   except: 
       e,r = None, None
   return e, r

def normalize(data, cols, ws, prior=0.5):
    [(l, R)] = data[['Eig']].values
    z    = data[cols].values
    m    = data[['Re_mean', 'Im_mean']].values
    L    = diagonal_matrix(l)
    S    = np.sqrt(L)
    T    = (R*S).T
    z    = (T* np.mat(z).T).flat
    m    = (T* np.mat(m).T).flat
    v    = np.diag(L*L) 
    norm = n2(z, m, v, ws, prior)
    return norm
