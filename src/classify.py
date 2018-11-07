#! /usr/bin/env python3


""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    classify.py 


    class_values are the limits for the absolute 
    voltage values and the absolute values of the 
    real and imaginary parts used for classifying 
    cvt faults

    The fault classification limit values may be 
    computed from the limits for the unknown nrs
    of capacitors in the C1 and C2 stacks. Here
    we rely on some pre-made production of these
    values, made by cf.py program to be found in 
    the same directory as this program. 


------------------------------------"""


import numpy as np

class alarm:    
    def __init__(I, time, voltage, re, im):
        I.time = time
        I.voltage = voltage
        I.re = re
        I.im = im
        I.r = np.sqrt(re**2 + im**2)
        I.phase = 'none'
        I.stack = 'none'
        I.unstable = []


    def write(I):
        print('   time:', I.time)
        print('voltage:', I.voltage)
        print('     re:', I.re)
        print('     im:', I.im)
        print('   phase:', I.phase)
        print('  stack:', I.stack)
        print(' unstab:', I.unstable)


class_values = {
    '220': {
        'c1': [[0.17, 0.3], [0.075, 0.17], [0.14, 0.26]],
        'c2': [[1.5, 6.0],   [0.8, 3.0],   [1.6,  5.5]]
    },
    '400': {
        'c1': [[0.09, 0.18], [0.04, 0.1], [0.075, 0.15]],
        'c2': [[1.5, 6.0],  [0.8,  3.0], [1.7,  5.1]]
    }
}

def belong(x, i):
    return (x >= i[0]) and (x <= i[1])


def neg(i):
    return [-i[1], -i[0]]


def classify(time, voltage, re, im):

    a = alarm(time, voltage, re, im)
    zero1 = [-0.05, 0.05]
    zero2 = [-0.5, 0.5]
    
    """
    if std > 0.02:
        return 'none'
    """

    [abs_c1, re_c1, im_c1] = class_values[str(voltage)]['c1']
    [abs_c2, re_c2, im_c2] = class_values[str(voltage)]['c2']

    if belong(re, neg(abs_c2))  and belong(im, zero2):
        a.stack = 'c2'
        a.phase = 'u1'
        # return 'c2', 'u1'

    elif belong(re, re_c2):  

        if belong(im, im_c2):     
            a.stack = 'c2'
            a.phase = 'u2'
            #return 'c2', 'u2'
        elif belong(im, neg(im_c2)):
            a.stack = 'c2'
            a.phase = 'u3'
            # print()
            print('\t -- c2 u3 --', time,'\t',re,'\t',im)
            # print()
            #return 'c2', 'u3'

    elif belong(re, abs_c1) and belong(im, zero1):
        a.stack = 'c1'
        a.phase = 'u1'
        #return 'c1', 'u1'

    elif belong(re, neg(re_c1)): 
        if belong(im, neg(im_c1)):   
            a.stack = 'c1'
            a.phase = 'u2'
            #return 'c1', 'u2'
        if belong(im, im_c1):
            a.stack = 'c1'
            a.phase = 'u3'
            #return 'c1', 'u3'
    
    return a
