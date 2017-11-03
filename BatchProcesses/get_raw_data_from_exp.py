import sys, os
############
projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))

from CreateExperimentApp import expDialog
from CalcFOMApp import calcfomDialog
from VisualizeDataApp import visdataDialog
from VisualizeBatchFcns import choosexyykeys
from fcns_io import *

#from get_raw_data_from_exp import get_file_dicts_containing_data

def get_file_dicts_containing_data(expname, filekeystoget, filetype):
    exppath=buildexppath(expname)
    expd, expzipclass=readexpasdict(exppath, includerawdata=False, erroruifcn=None, returnzipclass=True)
    expfolder=os.path.split(exppath)[0]

    runkeys=sort_dict_keys_by_counter(expd, keystartswith='run__')

    allfilesdict={}
    for rk in runkeys:
        rund=expd[rk]
        for fk in filekeystoget:
            if not fk in rund.keys():
                continue
            for fn, filed in rund[fk][filetype].iteritems():
                allfilesdict[fn]=filed
                filed['fn']=fn
                ans=buildrunpath_selectfile(fn, expfolder, runp=rund['run_path'], expzipclass=expzipclass, returnzipclass=True)
                
                p, zipclass=ans
                    
                filed['path']=p
                filed['zipclass']=zipclass
            
    for fn, filed in allfilesdict.items():
        filed['data_arr']=getarrs_filed(filed['fn'], filed, selcolinds=None, trydat=False, zipclass=filed['zipclass'])
    return allfilesdict
    
###Demo
#expname=r'/eche/20170504.082546.copied-20170504220706403PDT.zip'
#filekeystoget=['files_technique__CV2']
#filetype='pstat_files'
#
#allfilesdict=get_file_dicts_containing_data(expname, filekeystoget, filetype)
#print 'the first data array has shape ', allfilesdict.values()[0]['data_arr'].shape
