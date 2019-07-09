# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 17:41:21 2019

@author: gregoire
"""

import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    #Needed for running line-by-line
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\BatchProcesses\merge_xrfs_into_ana_v7_2frame_from_J_ana.py'
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
#import matplotlib.pyplot as plt
from fcns_io import *
from re import compile as regexcompile

sticksfolder=r'K:\users\hte\CompSustNet\2019_icdd\sticks_libraries'

lib_tups=sorted([(int(foldn.partition('_')[2]),tuple([el for el in sorted(regexcompile("[A-Z][a-z]*").findall(foldn.partition('_')[0])) if not el=='O']),foldn) for foldn in os.listdir(sticksfolder) if not foldn.startswith('sub')])[::-1]

lib_pt='substratePt_20190703161932'
lib_fto='substrateFTO_20190703161932'

serial_list='39248,39259,43760,39282,39349,35570,35873,35895,35479,32173,32061,32230,35558,35569,13891,48440,50296,22442,27829,35806,48473,48428,27818,35828,35503,35457,35794,27795,31071,31116,48473,50375,50353,50364,39361'.split(',')

#plate_list='1389,4847,5037,5035,5036'.split(',')
plate_list=[s[:-1] for s in serial_list]
#plate_list=plate_list[plate_list.index('4847'):]
#plate_list=['3557']
#plate_list=plate_list[1:]

 for el in els:
     
for pid in plate_list:
    
    d=importinfo(pid)
    els='-'.join([el for el in getelements_plateidstr(pid) if not el in ['Ar','O']])
    
    sublib=lib_pt if True in ['Pt' in pd['elements'] for pd in d['prints'].values()] else lib_fto
    
    for 
    print d['serial_no'],'\t',els