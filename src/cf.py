#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    cf.py 

    the impact of capacity failures
    on the voltage unbalance

 ------------------------------------"""

import numpy as np
import sys

n = int(sys.argv[1])  # total nr of capacitors
k = int(sys.argv[2])  # capacitors in the C2 stack


def unbalance(va, vb, vc):
    """
    The unbalances for line "symmetric phase" voltages
    The case v1 = v2 = v3 gives that both the negative
    sequence and the zero sequence is zero.
    """
    a  = 2*np.pi/3
    b  = [2*a, 0,   a]
    c  = [a,   0,   2*a]
    r  = []   # abs values of zero, pos., and neg. sequence
    re = []   # real parts of zero, pos., and neg. sequence
    im = []   # imaginary parts of zero, pos., and neg. sequence

    for i in range(0,3):
        x = va + vb * np.cos(b[i]) + vc * np.cos(c[i])
        y =      vb * np.sin(b[i]) + vc * np.sin(c[i])
        re += [x]   
        im += [y]
        r  += [np.sqrt(x**2 + y**2)]    # 3*|Vi|
    
    d = {}
    d['Re(Zero)']          = re[0]/r[1]
    d['Im(Zero)']          = im[0]/r[1]
    d['Abs(Zero)']         =  r[0]/r[1]
    d['Re(Positive)']      = re[1]/r[1]
    d['Im(Positive)']      = im[1]/r[1]
    d['Re(Negative)']      = re[2]/r[1]
    d['Im(Negative)']      = im[2]/r[1]
    return d


def pu(va, vb, vc):
    d = unbalance(va, vb, vc)
    mz = ['Re(Zero)', 'Im(Zero)'] 
    mp = ['Re(Positive)', 'Im(Positive)'] 
    mn = ['Re(Negative)', 'Im(Negative)']
    m = mz + mp + mn
    m = mz
    print()
    for k in m:
        print('\t'+k+'\t', 100*round(d[k] + 1e-15, 3))
    print()

def pz(va, vb, vc):
    # f  = 370
    f = 100
    d  = unbalance(va, vb, vc)
    a  = round(d['Abs(Zero)'], 5)
    re = round(d['Re(Zero)'], 5)
    im = round(d['Im(Zero)'], 5)
    print(f*a,'\t\t', f*re,'   \t', f*im)

def pz_interval(va, vb, vc):
    noise = 0.02
    f = 100
    d  = unbalance(va, vb, vc)
    a  = round(d['Abs(Zero)'], 5)
    re = round(d['Re(Zero)'], 5)
    im = round(d['Im(Zero)'], 5)
    fa =  np.array([f*a - noise, f*a + noise])
    fre = np.array([f*re - noise, f*re + noise])
    fim = np.array([f*im - noise, f*im + noise])
    print(fa,'\t', fre,'   \t', fim)

def vz(n, k):
    """
    assume a maximal noise at not more than
    0.02 in v1
    """

    
    n1 = n-1
    k1 = k-1
    v1 = n/n1
    v2 = v1* k1 / k 

    cases = {
        'U1 C1': (v1,  1, 1),
        'U1 C2': (v2,  1, 1),
        'U2 C1': (1,  v1, 1),
        'U2 C2': (1,  v2, 1),
        'U3 C1': (1,  1, v1),
        'U3 C2': (1,  1, v2),
    }

    
    c1 = ['U1 C1', 'U2 C1', 'U3 C1']
    c2 = ['U1 C2', 'U2 C2', 'U3 C2',]

    # c1_line_chage = v1 -1
    # c1_line_chage = v2 -1
    print()    
    print('\n\t', n, 'capacitors in total and\n\t', k, 'C2 capacitors')
    print()
    # print('\t C1 line voltage: new/old  =', round(v1, 5))
    # print('\t C2 line voltage: new/old  =', round(v2, 5))
    print('\t C1 line voltage change[%] =', round(100* (v1 -1), 3))
    print('\t C2 line voltage change[%] =', round(100* (v2 -1), 3))
    print()
    #print('\t C1 change[%] wrt abs value of pos.seq.=', round(100* (v1 -1)/3, 3))
    #print('\t C2 change[%] wrt abs value of pos.seq.=', round(100* (v2 -1)/3, 3))

    print()
    print('\t case\t\t|Zero| %\t Re(Zero) % \t Im(Zero) %\n')
    for c in c1:
        print('\t',c, end = '\t\t')
        pz(*cases[c])
    print()
    for c in c2:
        print('\t',c, end = '\t\t')
        pz(*cases[c])
    print()
 

    print()
    print('\t case\t\t|Zero| %\t\t Re(Zero) % \t\t Im(Zero) %\n')
    for c in c1:
        print('\t',c, end = '\t\t')
        pz_interval(*cases[c])
    print()
    for c in c2:
        print('\t',c, end = '\t\t')
        pz_interval(*cases[c])
    print()
 



       
def v(v, c):
    n  = int(v/c)
    k  = int(n/11) 
    print('\n\t',v,'kV,',n-k, 'C1 capacitors,', k, 'C2 capacitors')
    vz(n, k)

def change(na, nb, ka, kb, dec = 4):

    print('\n\tn\\k\tc1\t', end = '')
    for k in range (ka, kb+1):
        print('\t'+str(k), end = '\t')
    for n in range(na, nb+1):

        n1 = n-1
        c1 = round(100* (n/n1 - 1), dec)
        print('\n\t'+str(n) + '\t'+ str(c1), end = '\t')

        for k in range (ka, kb+1):
            k1 = k-1
            c2 = round(100* (n*k1 / (k*n1) - 1), dec)

            print('\t' + str(c2), end = '\t')
    print()    
    print()

# v(245, 1.5)

# v(420, 1.5)

# change(230, 250, 10, 15)
# vz(150, 15)
vz(n, k)

