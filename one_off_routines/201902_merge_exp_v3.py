# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:43:08 2019

@author: gregoire

merge the runs from 2 exp. 
. Can reassign the data_use for each run, which allows sample plate_id, technique, sample_no to exist in 2 different runs - it up to the user to ensure that such duplicates have different run_use
. Can provide a .csv with plate_id and sample_no and choose whether to keep only those (include_csv_samples_bool=True) or keep all but this (include_csv_samples_bool=False)
"""

#Needed for running line-by-line
#__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\one_off_routines\201902_merge_exp_v1.py'

import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
#import matplotlib.pyplot as plt
from fcns_io import *
from fcns_ui import *


if 0:
    #post pets intersection of samples with pre
    plate_exp_str=r'40745: 20190228.110547.copied-20190301222931021PST,50690: 20190228.110155.copied-20190301222931021PST,51545: 20190228.110440.copied-20190301222931021PST,51253: 20190228.105542.copied-20190301222931021PST,51365: 20190228.105808.copied-20190301222931021PST,51477: 20190228.104732.copied-20190301222931021PST,51433: 20190304.113409.done'
    plate_exp_tups=[s.partition(': ')[::2] for s in plate_exp_str.split(',')]
    exp_info_dlist=[dict({},run_use='data-postPETS',plate_id=pl,exp_folder_path='L:\processes\experiment\eche\%s.done' %ex) for pl,ex in plate_exp_tups]
    filter_plate_sample_fileattrd=None
elif 1:

    plate_exp_str=r'40745: 20190227.095056.copied-20190228082609825PST,50690: 20190228.095246.copied-20190301222931021PST,51545: 20190228.132533.copied-20190301222931021PST,51253: 20190228.103343.copied-20190301222931021PST,51365: 20190227.100856.copied-20190228082609825PST,51477: 20190227.101033.copied-20190228082609825PST,51433: 20190304.113120.done'

    plate_exp_tups=[s.partition(': ')[::2] for s in plate_exp_str.split(',')]

    #exp_info_dlist must have a list fo dicts, 1 for each exp to be concatenated, each with a key exp_folder_path for each entry and optional keys are plate_id (needed for csv filtering) and run_use (to overwrite the run use in the concatenated exp)
    exp_info_dlist=[dict({},run_use='data-prePETS',plate_id=pl,exp_folder_path='L:\processes\experiment\eche\%s.done' %ex) for pl,ex in plate_exp_tups]


    plate_exp_str=r'40745: 20190227.094406.copied-20190228082609825PST,50690: 20190227.093453.copied-20190228082609825PST,51545: 20190227.094332.copied-20190228082609825PST,51253: 20190228.103025.copied-20190301222931021PST,51365: 20190227.094456.copied-20190228082609825PST,51477: 20190228.103557.copied-20190301222931021PST,51433: 20190304.113329.done'
    plate_exp_tups=[s.partition(': ')[::2] for s in plate_exp_str.split(',')]

    #exp_info_dlist must have a list fo dicts, 1 for each exp to be concatenated, each with a key exp_folder_path for each entry and optional keys are plate_id (needed for csv filtering) and run_use (to overwrite the run use in the concatenated exp)
    exp_info_dlist+=[dict({},run_use='data-postPETS', plate_id=pl,exp_folder_path='L:\processes\experiment\eche\%s.done' %ex) for pl,ex in plate_exp_tups]
    
    if 0:
        filter_plate_sample_fileattrd=None
    else:
        filter_plate_sample_fileattrd={'p':r'L:\processes\analysis\eche\20190304.131739.done\ana__2__num_samples_averaged-I.A_ave.csv', \
        'keys':'sample_no,runint,plate_id,SmpRunPlate_Association,num_samples_averaged,I.A_ave'.split(','), \
        'num_header_lines':9
        }

#def combine_exps(exp_info_dlist,filter_plate_sample_fileattrd=None,include_csv_samples_bool=True,access=None,created_by=None,experiment_type=None,include_sample_0=True,rundone='.run')


include_csv_samples_bool=True
access=None
created_by=None
experiment_type=None
include_sample_0=True
rundone='.run'

dlist=[readexpasdict(buildexppath(di['exp_folder_path'])) for di in exp_info_dlist]

if filter_plate_sample_fileattrd is None:
    filter_plate_sample_list=None
else:
    filterd=readcsvdict(filter_plate_sample_fileattrd['p'], filter_plate_sample_fileattrd)
    if 'plate_id' in filterd.keys():
        filter_plate_sample_list=zip(filterd['plate_id'], filterd['sample_no'])
    else:
        filter_plate_sample_list=filterd['sample_no']

exp_names=[d['name'] for d in dlist]
newexpd={}
newexpd['description']='Combination of exp '+','.join(exp_names)+'. '+';'.join([d['description'] for d in dlist])
newexpd['exp_version']='3'
newexpd['created_by']=dlist[0]['created_by'] if created_by is None else created_by
newexpd['access']=dlist[0]['access'] if access is None else access
newexpd['experiment_type']=dlist[0]['experiment_type'] if experiment_type is None else experiment_type
newexpd['name']=timestampname()



new_run_counter=1
for d, di in zip(dlist,exp_info_dlist):
    
    
    kl=sort_dict_keys_by_counter(d, keystartswith='run__')
    for rk in kl:
        if 'run_use' in di.keys():
            d[rk]['run_use']=di['run_use']
        pid=d[rk]['parameters']['plate_id']
        if filter_plate_sample_list is None:
            keep_run=True
        else:
            keep_run=False
            files_keys=[k for k in d[rk] if k.startswith('files_technique__')]
            for fk in files_keys:
                for ftk in d[rk][fk].keys():
                    ftd=d[rk][fk][ftk]
                    for fn in ftd.keys():#don't use iterator because deleting as we go 
                        fd=ftd[fn]
                        if (not 'sample_no' in fd.keys()) or fd['sample_no']==0:
                            keepbool=include_sample_0
                        else:
                            inlist=(pid,fd['sample_no']) in filter_plate_sample_list if ('plate_id' in filterd.keys()) else fd['sample_no'] in filter_plate_sample_list
                            keepbool=inlist if include_csv_samples_bool else not inlist
                        if not keepbool:
                            del ftd[fn]
                    if len(d[rk][fk][ftk])==0:#all samples deleted so delete the whole section
                        del d[rk][fk][ftk]
                if len(d[rk][fk])==0:#all samples deleted so delete the whole section
                    del d[rk][fk]
                else:
                    keep_run=True# so any nonempty files list will trigger keeping run
        if keep_run:
            newexpd['run__%d' %new_run_counter]=d[rk]
            newexpd['run__%d' %new_run_counter]['original_exp_name']=d['name']
            new_run_counter+=1
    
saveexp_txt_dat(newexpd, erroruifcn=None, saverawdat=False, experiment_type=newexpd['experiment_type'], rundone=rundone, runtodonesavep=None, savefolder=None, file_attr_and_existence_check=False)
