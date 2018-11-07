#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    power.py 

    analysis of 3-phase power systems 

------------------------------------"""

import numpy as np
import common
def add_symmetric(df):

    """
    to df add the zero and negative sequences
    in percentages of the positive
    """

    va  = df['u1']
    vb  = df['u2']
    vc  = df['u3']
    b0  = df['phase2']  # phase of vb for zero comp
    c0  = df['phase3']  # phase of vc for zero comp
    a  = 2*np.pi/3     
    b  = [b0,   b0 + a,   b0 + 2*a]
    c  = [c0,   c0 + 2*a, c0 + a]
    r  = []   # abs values of zero, pos., and neg. sequence
    re = []   # real parts of zero, pos., and neg. sequence
    im = []   # imaginary parts of zero, pos., and neg. sequence

    for i in range(0,3):
        x = va + vb * np.cos(b[i]) + vc * np.cos(c[i])
        y =      vb * np.sin(b[i]) + vc * np.sin(c[i])
        re += [x]   
        im += [y]
        r  += [np.sqrt(x**2 + y**2)]    # 3*|Vi|

    df['V1'] = r[1]   

    def atan360(d, c):
        x = d['Re('+c+')']
        y = d['Im('+c+')']
        return common.arctan360(x, y)

    t   = [lambda d: atan360(d, 'Zero')]
    t  += [lambda d: atan360(d, 'Positive')]
    t  += [lambda d: atan360(d, 'Negative')]


    df['V1'] = r[1]   

    df['Re(Positive)']        = 100 * re[1]/r[1]
    df['Im(Positive)']        = 100 * im[1]/r[1]
    df['Theta(Positive)']     = df.apply(t[1], axis = 1)

    df['Re(Zero)']            = 100 * re[0]/r[1]
    df['Im(Zero)']            = 100 * im[0]/r[1]
    df['Abs(Zero)']           = 100 * r[0]/r[1]
    df['Theta(Zero)']         = df.apply(t[0], axis = 1)

    df['Re(Negative)']        = 100 * re[2]/r[1]
    df['Im(Negative)']        = 100 * im[2]/r[1]
    df['Abs(Negative)']       = 100 * r[2]/r[1]
    df['Theta(Negative)']     = df.apply(t[2], axis = 1)

    df['Re(Zero)diff']        = df['Re(Zero)'].diff()
    df['Im(Zero)diff']        = df['Im(Zero)'].diff()
    df['Abs(Zero)diff']       = df['Abs(Zero)'].diff()
    df['Theta(Zero)diff']     = df['Theta(Zero)'].diff()

    df['Re(Positive)diff']    = df['Re(Positive)'].diff()
    df['Im(Positive)diff']    = df['Im(Positive)'].diff()
    df['Theta(Positive)diff'] = df['Theta(Positive)'].diff()

    df['Re(Negative)diff']    = df['Re(Negative)'].diff()
    df['Im(Negative)diff']    = df['Im(Negative)'].diff()
    df['Abs(Negative)diff']   = df['Abs(Negative)'].diff()
    df['Theta(Negative)diff'] = df['Theta(Negative)'].diff()

    return df

   

  
