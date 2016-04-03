skiponerror=False
batchfilepath=r'.batch'

import sys, os
############
sys.path.append(os.path.join(os.getcwd(),'QtForms'))
sys.path.append(os.path.join(os.getcwd(),'AuxPrograms'))
sys.path.append(os.path.join(os.getcwd(),'OtherApps'))

from CreateExperimentApp import expDialog
from CalcFOMApp import calcfomDialog
from VisualizeDataApp import visdataDialog
from CombineFomApp import combinefomDialog
from FileSearchApp import filesearchDialog
from FileManagementApp import filemanDialog
from file_io import *

expui=expDialog(self, title='Create/Edit an Experiment')
calcui=calcfomDialog(self, title='Calculate FOM from EXP')
visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')


with open(batchfilepath, mode='r') as f:
    batchfns=f.readlines()

logfilepath=batchfilepath.rpartition('.')[0]+'.log'

runsrcfolder=tryprependpath(RUNFOLDERS, r'uvis\hte-uvis-02', testfile=False, testdir=True)
expdestchoice=r'temp'
anadestchoice=r'temp'

loglines=[]
def writelogline(s, loglines=loglines):
    loglines+=[s]
    with open(logfilepath, mode='w') as f:
        f.write('\n'.join(loglines))
        
    
for fn in batchfns:
    pT=os.path.join(runsrcfolder, fn)
    pR=os.path.join(runsrcfolder, fn.replace('_T-', '_R-'))
    
    if not os.path.isfile(pT):
        writelogline('ERROR: cannot find file %s' %pT)
        if skiponerror:
            continue
        else:
            raiseerror
    if not os.path.isfile(pR):
        writelogline('ERROR: cannot find file %s' %pR)
        if skiponerror:
            continue
        else:
            raiseerror
            
    plateidstr=pT.rpartition('_')[2]
    
    infofn=plateidstr+'.info'
    p=tryprependpath(PLATEFOLDERS, os.path.join(plateidstr, infofn), testfile=True, testdir=False)
        
    if len(p)==0:
        writelogline('ERROR: info file not found for %s' %plateidstr)
        if skiponerror:
            continue
        else:
            raiseerror
    with open(p, mode='r') as f:
        lines=f.readlines()
    infofiled=filedict_lines(lines)
    
    methods=[v3 for k, v in infofiled.iteritems() if k.startswith('prints') for k2, v2 in v.iteritems() if k2.startswith('prints') for k3, v3 in infofiled.iteritems() if k3.startswith('method')]
    pvdbool='PVD' in methods
    
    
    expui.importruns_folder(folderp=pT)
    expui.importruns_folder(folderp=pR)
    expui.batchuvissingleplate_norefdata()
    
    if (not 'experiment_type' in expui.expfiledict.keys()) or len(expui.expfilestr)==0 or not 'exp_version' in expui.expfilestr:
        writelogline('ERROR: betchexp failed for %s' %pT)
        if skiponerror:
            continue
        else:
            raiseerror
    
    expui.saveexp()
    
    
    
    
    
    
