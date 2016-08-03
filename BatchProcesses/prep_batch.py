# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:12:15 2016

@author: sksuram
"""
import os,sys
sys.path.append(r'E:\GitHub\JCAPDataProcess\AuxPrograms')
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
        
    def getpvdbool(self,plateidstr,skiponerror=True):
        infofn=plateidstr+'.info'
        p=tryprependpath(PLATEFOLDERS, os.path.join(plateidstr, infofn), testfile=True, testdir=False)
            
        if len(p)==0:
            if skiponerror:
                return 'ERROR - info file not found for %s' %plateidstr, False
            else:
                raiseerror
        with open(p, mode='r') as f:
            lines=f.readlines()
        infofiled=filedict_lines(lines)
        
        methods=[v3 for k, v in infofiled.iteritems() if k.startswith('prints') for k2, v2 in v.iteritems() if k2.startswith('prints') for k3, v3 in v2.iteritems() if k3.startswith('method')]
        return 'PVD' in methods
            
    def Batch_TR_getapplicable_Tfolder(self,plateidstr,combine_parentfolders=False,pvdbool=False):
        
        infofiled=self.importinfo(plateidstr)
        if pvdbool==None:
            pvdbool=self.getpvdbool(plateidstr)           
        try:
            T_runs=[infofiled['runs'][rk]['path'] for rk in infofiled['runs'].keys() if infofiled['runs'][rk]['type']=='uvis'\
        and 'T-UVVIS' in infofiled['runs'][rk]['path']]
            R_runs=[infofiled['runs'][rk]['path'] for rk in infofiled['runs'].keys() if infofiled['runs'][rk]['type']=='uvis'\
        and 'R-UVVIS' in infofiled['runs'][rk]['path']]
        except:
            T_runs=[]
            R_runs=[]
        if not combine_parentfolders:
            Trunparents=[os.path.dirname(x) for x in T_runs]
            Rrunparents=[os.path.dirname(x) for x in R_runs]
            if len(list(set(Trunparents)))!=1 or len(list(set(Rrunparents)))!=1:
                print 'Tparents: ',','.join(list(set(Trunparents)))
                print 'Rparents: ',','.join(list(set(Rrunparents)))
                print 'Expected 1 parent T folder, 1 parent R folder for plateid: %s but found %d,%d' %(plateidstr,len(list(set(Trunparents))),len(list(set(Rrunparents))))
                tp=None
                return T_runs,R_runs,tp

        if pvdbool: 
            if len(T_runs)!=2 and len(R_runs)!=1:
                print 'Expected %s T-folders, %s R-folders for plateid: %s, found %s T-folders, %s R-folders' %(2,1,plateidstr,len(T_runs),len(R_runs))
                tp=None
            else:
#                print T_runs
                tp=os.path.dirname(T_runs[0])
            return T_runs,R_runs,tp
        else:
            if len(T_runs)==0 or len(R_runs)==0:
                print 'Expected atleast %s T-folders, %s R-folders for plateid: %s, found %s T-folders, %s R-folders' %(1,1,plateidstr,len(T_runs),len(R_runs))
                tp=None
            else:
#                print T_runs
                tp=os.path.dirname(T_runs[0])
            return T_runs,R_runs,tp

        