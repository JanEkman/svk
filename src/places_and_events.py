#! /usr/bin/env python3

""" -------------------------------

    Copyright (C) 2018 RISE
    This code was produced by RISE

    places_and_events.py 

    We here use "space" to refer to the location
    of a data set, with data on one cvt or some 
    cvts, the events related to these cvts and
    names used for naming produced data files.


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
    'other',
]


------------------------------------"""


truth = '../data/truth/'
out   = '../data/out/'      # for temporary output
inp   = '../data/input/'  

spaces = {

    'data_1' : {
        'data' : '../data/original/Dataset1/Dataset1.csv',
        'names' : ['cvt_1'],
        'events' : [
            ['2017-11-26 00:00:00', 'normal', '1'],
            ['2017-11-28 21:08:03', 'cap_u2c1', '1'],
            ['2017-11-28 21:08:03', 'normal', '0'],
        ]
    },    

    'data_2' : {
        'data' : '../data/original/Dataset2/Dataset2.csv',
        'names' : ['cvt_2'],
        'events' : [
            ['2018-06-26 00:00:00', 'normal', '0'],
            ['2018-06-26 11:03:06', 'normal', '1'],
        ]
    },

    'data_3' : {
        'data' : '../data/original/Dataset3/Dataset3.csv',
        'names' : ['cvt_3'],
        'events' : [
            ['2016-10-24 00:00:00', 'normal', '1'],
            ['2016-10-24 08:08:54', 'cap_u3c1', '1'],
            ['2016-10-24 08:08:54', 'normal', '0'],
        ]
    },

 
    'data_4' : {
        'data' : '../data/original/Dataset4/Dataset4.csv',
        'names' : ['cvt_4'],
        'events' : [
            ['2018-09-18 00:00:00', 'normal', '1'],
            ['2018-09-18 05:30:06', 'cap_u3c1', '1'],
            ['2018-09-18 05:30:06', 'normal', '0'],
            ['2018-09-18 05:32:03', 'cap_u3c1', '2'],
        ]
    },

   
    'data_5' : {
        'data' : '../data/original/Dataset5/Dataset5.csv',
        'names' : ['cvt_5'],
        'events' : [
            ['2018-09-16 00:00:00', 'normal', '1'], ### Normal? 10 ggr mer variation jmf 6
        ]
    },

   
    'data_6' : {
        'data' : '../data/original/Dataset6/Dataset6.csv',
        'names' : ['cvt_6'],
        'events' : [
            ['2018-09-13 00:00:00', 'normal', '1'],
        ]
    },

    'data_7' : {
        'data' : '../data/original/Dataset7/Dataset7.csv',
        'names' : ['cvt_7'],
        'events' : [
            ['2018-09-03 00:00:00', 'normal', '1'],
            ['2018-09-03 04:36:39', 'normal', '0'],
        ]
    },


    'data_8' : {
        'data' : '../data/original/Dataset8/Dataset8.csv',
        'names' : ['cvt_8'],
        'events' : [
            ['2018-08-01 00:00:00', 'normal', '1'],
        ]
    },


    'data_9' : {
        'data' : '../data/original/Dataset9/Dataset9.csv',
        'names' : ['cvt_9'],
        'events' : [
            ['2018-03-01 10:18:18', 'normal', '1' ],
        ]
    },

    'data_10h' : {
        'data' : '../data/original/Dataset10/Dataset10h.csv',
        'comment' : 'data_10h: just for test, a few initial lines of data_10',
        'events' : [
        ]
    },
    
    'data_10' : {
        'data' : '../data/original/Dataset10/Dataset10.csv',
        'names' : ['cvt_10'],
        'events' :  [
            ['2017-11-22 00:00:00', 'normal', '0'],
            ['2017-11-22 00:00:00', 'unbalance', '1'],
            ['2017-11-23 12:23:54', 'unbalance', '0'],
            ['2017-11-23 13:00:15', 'normal', '1'], ### alt 13:01:15
        ]
     },

    'data_11' : {
        'data' : '../data/original/Dataset11/Dataset11.csv',
        'names' : ['cvt_11'],
        'events' : [
            ['2018-06-01 00:00:00', 'normal', '0'],
            ['2018-06-01 00:00:00', 'fuse_u3', '1'],
        ]
     },

    'data_12' : {
        'data' : '../data/original/Dataset12/Dataset12.csv',
        'names' : ['cvt_12'],
        'events' : [
            ['2018-07-01 00:00:00', 'normal', '1'],
        ]
     },


    'data_13' : {
        'data' : '../data/original/Dataset13/Dataset13.csv',
        'names' : ['cvt_13'],
        'events' : [
            ['2018-09-16 00:00:00', 'normal', '1'],
        ]
     },

    'data_14' : {
        'data' : '../data/original/Dataset14/Dataset14.csv',
        'names' : ['cvt_14_1', 
                   'cvt_14_2', 
                   'cvt_14_3', 
                   'cvt_14_4'],
        'events' : [
            [
                ['2018-09-18 00:00:00 ', 'normal', '1' ],
            ],
            [
                ['2018-09-18 00:00:00', 'normal', '1' ],
            ],
            [
                ['2018-09-18 00:00:00', 'normal', '1' ],
            ],
            [
                ['2018-09-18 00:00:00', 'normal', '1' ],
                ['2018-09-18 05:30:06', 'cap_u3c1', '1'],
                ['2018-09-18 05:30:06', 'normal', '0'],
                ['2018-09-18 05:32:03', 'cap_u3c1', '2'],
            ],
        ]
    },


    
    'data_15' : {
        'data' : '../data/original/Dataset15/Dataset15.csv',
        'names' : ['cvt_15_1', 
                   'cvt_15_2', 
                   'cvt_15_3', 
                   'cvt_15_4'],
        'events' : [
            [
                ['2018-09-20 00:00:00', 'normal', '1' ],
            ],
            [
                ['2018-09-20 00:00:00', 'normal', '1' ],
            ],
            [
                ['2018-09-20 00:00:00', 'normal', '1' ],
            ],
            [
                ['2018-09-20 00:00:00', 'normal', '1' ],
            ],
        ]
    },

}
