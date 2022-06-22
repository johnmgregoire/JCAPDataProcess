import sys, os
############
projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))
import operator
from fcns_io import *
#fix error of too many open files
#import win32file
#if win32file._getmaxstdio()<1000:
#    win32file._setmaxstdio(2048)

#from get_raw_data_from_exp import get_file_dicts_containing_data


def get_file_dicts_containing_data(expname, filekeystoget, filetype, sample_list=None, fn_must_contain='', return_list_ordered_by_sample=False):
    exppath=buildexppath(expname)
    expd, expzipclass=readexpasdict(exppath, includerawdata=False, erroruifcn=None, returnzipclass=True)
    expfolder=os.path.split(exppath)[0]

    runkeys=sort_dict_keys_by_counter(expd, keystartswith='run__')

    allfilesdict={}
    for rk in runkeys:
        rund=expd[rk]
        runp_fullpath=buildrunpath(rund['run_path'])
        rund['zipclass']=gen_zipclass(runp_fullpath)
        for fk in filekeystoget:
            if not fk in list(rund.keys()):
                continue
            for fn, filed in rund[fk][filetype].items():
                if not fn_must_contain in fn:
                    continue
                if (not sample_list is None) and (not filed['sample_no'] in sample_list):
                    continue
                allfilesdict[fn]=filed
                filed['fn']=fn

                filed['zipclass']=rund['zipclass']
            
    for fn, filed in list(allfilesdict.items()):
        filed['data_arr']=getarrs_filed(filed['fn'], filed, selcolinds=None, trydat=False, zipclass=filed['zipclass'])
    
    if return_list_ordered_by_sample and not sample_list is None:
        tups=sorted([(sample_list.index(v['sample_no']), v) for v in list(allfilesdict.values())])
        dlist=list(map(operator.itemgetter(1), tups))
        return dlist
    elif return_list_ordered_by_sample:#ordered by sample_no but user doesn't yet know the sample_no list (get it as [d['sample_no'] for d in dlist])
        tups=sorted([(v['sample_no'], v) for v in list(allfilesdict.values())])
        dlist=list(map(operator.itemgetter(1), tups))
        return dlist
    else:
        return allfilesdict
    


####Demo
#expname=r'/eche/20170504.082546.copied-20170504220706403PDT.zip'
#filekeystoget=['files_technique__CV2']
#filetype='pstat_files'
#
#allfilesdict=get_file_dicts_containing_data(expname, filekeystoget, filetype, sample_list=[646, 941])
#print 'the first data array has shape ', allfilesdict.values()[0]['data_arr'].shape
