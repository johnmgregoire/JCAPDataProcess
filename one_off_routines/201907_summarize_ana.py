#make  folder containing analysis the cwd
import numpy, copy, operator
import time,pickle
if __name__ == "__main__":
    import os, sys
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\AnalysisFunctions\ecms.py'
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
from fcns_io import *
from fcns_ui import *

savep=r'K:\users\gregoire\201904_database_analysis\pub-20190329083955-all\eche_subanalysis_summary.tsv'
savep=r'K:\users\gregoire\201904_database_analysis\J-20190716\eche_subanalysis_summary.tsv'
typename='eche'

fold=os.path.join(os.path.join(os.getcwd(),'analysis'),typename)
zipfns=[fn for fn in os.listdir(fold) if fn.endswith('.zip')]

pidstr_fcn=lambda d,dflt: dflt if not 'plate_ids' in d.keys() else ('%d' %d['plate_ids'] if isinstance(d['plate_ids'],int) else d['plate_ids'])

results=[]
for fn in zipfns:
    zipfn=os.path.join(fold,fn)

    anad=readana(zipfn)
    anapid=pidstr_fcn(anad,'')
    for anak in sort_dict_keys_by_counter(anad):
        if not 'files_multi_run' in anad[anak].keys() or not 'fom_files' in anad[anak]['files_multi_run'].keys():
            continue
        for csvfn,filed in anad[anak]['files_multi_run']['fom_files'].items():
            results+=[[pidstr_fcn(anad[anak],anapid),fn,anak,csvfn,anad[anak]['name'],','.join(filed['keys']),'%d' %filed['num_data_rows'],'%d' %anad[anak]['analysis_fcn_version']]] 

h='\t'.join('plate_ids,ana_zip_name,sub_analysis_key,fom_csv_fn,subanalysis_name,fom_names,num_rows,analysis_fcn_version'.split(','))
s='\n'.join([h]+['\t'.join(l) for l in results])

with open(savep,mode='w') as f: f.write(s)

import pandas as pd

df=pd.read_csv(savep,delimiter='\t')
len(df['plate_ids'][df['subanalysis_name']=='Analysis__Etaave'])
len(set(df['plate_ids'][df['subanalysis_name']=='Analysis__Etaave']))
set(df['fom_names'][df['subanalysis_name']=='Analysis__Etaave'])

len(df['plate_ids'][df['fom_names']=='sample_no,runint,plate_id,Eta.V_ave'])
len(set(df['plate_ids'][df['fom_names']=='sample_no,runint,plate_id,Eta.V_ave']))

set(df['ana_zip_name'][(df['fom_names']=='sample_no,runint,plate_id,E.V_ave') & (df['subanalysis_name']=='Analysis__Etaave')])
set(df['analysis_fcn_version'][(df['fom_names']=='sample_no,runint,plate_id,E.V_ave') & (df['subanalysis_name']=='Analysis__Etaave')])
set(df['analysis_fcn_version'][(df['fom_names']=='sample_no,runint,plate_id,Eta.V_ave') & (df['subanalysis_name']=='Analysis__Etaave')])

set(df['fom_names'][df['subanalysis_name']=='Analysis__Etaave'])