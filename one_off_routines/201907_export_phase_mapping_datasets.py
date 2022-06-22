# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 16:10:27 2019

@author: gregoire
"""
import numpy, copy, operator
import shutil
if __name__ == "__main__":
    import os, sys
    #Needed for running line-by-line
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\BatchProcesses\merge_xrfs_into_ana_v7_2frame_from_J_ana.py'
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
#import matplotlib.pyplot as plt
from fcns_io import *



ananames=r'xrds\20190628.132713.run\20190628.132713.ana,xrds\20190628.133758.run\20190628.133758.ana,xrds\20190628.140658.run\20190628.140658.ana,xrds\20190701.093129.run\20190701.093129.ana,xrds\20190628.141853.run\20190628.141853.ana,xrds\20190701.111746.run\20190701.111746.ana,xrds\20190701.103712.run\20190701.103712.ana,xrds\20190703.091317.run\20190703.091317.ana,xrds\20190701.110930.run\20190701.110930.ana,xrds\20190701.112426.run\20190701.112426.ana,xrds\20190701.113340.run\20190701.113340.ana,xrds\20190701.142646.run\20190701.142646.ana,xrds\20190701.143351.run\20190701.143351.ana,xrds\20190703.092000.run\20190703.092000.ana,xrds\20190703.092327.run\20190703.092327.ana,xrds\20190703.092736.run\20190703.092736.ana,xrds\20190703.092821.run\20190703.092821.ana,xrds\20190701.143941.run\20190701.143941.ana'.split(',')
savefolder=r'K:\users\hte\CompSustNet\201907_phase_mapping_datasets'

sumtablelines=[]
for s in ananames:
    anap=buildanapath(s)
    anafold=os.path.split(anap)[0]
    ad=readana(anap)
    pid=repr(ad['plate_ids'])
    d=importinfo(pid)
    els='-'.join([el for el in getelements_plateidstr(pid) if not el in ['Ar']])
    foldname='_'.join([pid,els,ad['name'][:8]])
    sf=os.path.join(savefolder,foldname)
    if not os.path.exists(sf): os.mkdir(sf)
    for fn in os.listdir(anafold):
        if fn.endswith('.udi') or fn.endswith('.ana'):
            shutil.copy(os.path.join(anafold,fn),os.path.join(sf,fn))
    sumtablelines+=['\t'.join([pid,d['serial_no'],foldname])]
print('\n'.join(sumtablelines))