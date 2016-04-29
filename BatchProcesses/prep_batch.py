# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:12:15 2016

@author: sksuram
"""
import os
from fcns_io import *
from DBPaths import *

class Prepare_Batch_UVIS():
    def __init__(self):
        pass

    def importinfo(self,plateidstr):
        fn=plateidstr+'.info'
        p=tryprependpath(PLATEFOLDERS, os.path.join(plateidstr, fn), testfile=True, testdir=False)
        with open(p, mode='r') as f:
            lines=f.readlines()
        infofiled=filedict_lines(lines)
        return infofiled
        
    def getpvdbool(self,plateid):
        pass
        
    def Batch_TR_getapplicable_Tfolder(self,plateidstr,pvdbool=None):
        
        infofiled=self.importinfo(plateidstr)
        if pvdbool==None:
            pvdbool=self.getpvdbool(plateidstr)
        if pvdbool:            
            try:
                T_runs=[infofiled['runs'][rk]['path'] for rk in infofiled['runs'].keys() if infofiled['runs'][rk]['type']=='uvis'\
            and 'T-UVVIS' in infofiled['runs'][rk]['path']]
                R_runs=[infofiled['runs'][rk]['path'] for rk in infofiled['runs'].keys() if infofiled['runs'][rk]['type']=='uvis'\
            and 'R-UVVIS' in infofiled['runs'][rk]['path']]
            except:
                T_runs=[]
                R_runs=[]
            if len(T_runs)!=2 and len(R_runs)!=1:
                print 'Expected %s T-folders, %s R-folders for plateid: %s, found %s T-folders, %s R-folders' %(2,1,plateidstr,len(T_runs),len(R_runs))
                tp=None
            else:
                print T_runs
                tp=os.path.dirname(T_runs[0])
            return len(T_runs),len(R_runs),tp
        