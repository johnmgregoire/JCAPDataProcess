# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 09:22:10 2018

@author: gregoire
"""

#srcfolder=r'L:\processes\analysis\rams\temp_to_add_to_4076'
#anafolder=r'L:\processes\analysis\rams\20181130.142222.run'
#srcfolder=r'L:\processes\analysis\rams\temp_to_add_to_4832'
#anafolder=r'L:\processes\analysis\rams\20181130.141414.run'

#fom_segment_min_index_spacing=4



import os,shutil
import pandas as pd
import numpy as np

def import_CU_Multi_Bcknd_as_ana_block(srcfolder,anafolder,fom_segment_min_index_spacing=6,anak='ana__2'):
    def get_num_segments(arr):
        indsarr=np.where((arr[:-1]<=0.5)&(arr[1:]>0.5))[0]
        if len(indsarr)==0:
            return 0
        return ((indsarr[1:]-indsarr[:-1])>fom_segment_min_index_spacing).sum()+int(indsarr[0]>fom_segment_min_index_spacing)
    
    
    pid=int(srcfolder.rpartition('_')[2])
    keystr='sample_no,runint,plate_id,num_pts_above_bcknd,smooth_num_pts_above_bcknd,num_segments_above_bcknd,smooth_num_segments_above_bcknd,max_signal_prob,max_smooth_signal_prob'
    numk=keystr.count(',')+1
    
    indent='    '
    paramsfromfile=''
    
    tups=[]
    filelists=[[],[],[]]
    for fn in os.listdir(srcfolder):
        pr=os.path.join(srcfolder,fn)
        nfn=anak+'_'+fn
        pn=os.path.join(anafolder,nfn)
        if fn=='Bcknd_Summary.csv':
            with open(pr,mode='r') as f: lines=f.readlines()
            orig_summ_keys=lines[0].strip().split(',')
            inds=[count for count,k in enumerate(orig_summ_keys) if 'bcknd_weight__' in k]
            i0=inds[0]
            i1=inds[-1]
            if inds!=range(i0,i1+1):
                print 'WARNING NON CONSEC KEYS: ',inds,orig_summ_keys
            keep_summ_keys=orig_summ_keys[i0:i1+1]
            new_key_str=','.join([keystr]+keep_summ_keys)
            filelists[0].append('%s: csv_fom_file;%s;19;%d' %(nfn,new_key_str,len(lines)-1))
            csvstartstr=('1\t%d\t%d\t17\ncsv_version: 1\nplot_parameters:' %(numk+len(keep_summ_keys),len(lines)-1))+\
             '\n    plot__1:\n        colormap: jet\n        colormap_over_color: (0.5,0.,0.)\n        colormap_under_color: (0.,0.,0.)\n        fom_name: max_smooth_signal_prob' +\
             '\n    plot__2:\n        colormap: jet\n        colormap_over_color: (0.5,0.,0.)\n        colormap_under_color: (0.,0.,0.)\n        fom_name: smooth_num_pts_above_bcknd' +\
             '\n    plot__3:\n        colormap: jet\n        colormap_over_color: (0.5,0.,0.)\n        colormap_under_color: (0.,0.,0.)\n        fom_name: smooth_num_segments_above_bcknd' 
            summ_smps=[int(s.partition(',')[0]) for s in lines[1:]]
            summ_keepstrs=[','.join(s.split(',')[i0:i1+1]) for s in lines[1:]]
            p_summ=pn
        elif 'Bcknd_Factors' in fn:
            shutil.copy(pr,pn)
            with open(pn,mode='r') as f: lines=f.readlines()
            filelists[1].append('%s: rams_misc_file;%s;1;%d' %(nfn,lines[0].strip(),len(lines)-1))
        elif 'Bcknd_Sample_' in fn:
            shutil.copy(pr,pn)
            d=pd.read_csv(pn)
            x=np.array(d.as_matrix())
            smp=int(fn.rpartition('_')[2].partition('.')[0])
        
            tups.append((smp,1,pid,(x[:,2]>0.5).sum(),(x[:,3]>0.5).sum(),get_num_segments(x[:,2]),get_num_segments(x[:,3]),x[:,2].max(),x[:,3].max()))
            
            filelists[2].append('%s: rams_inter_rawlen_file;%s;1;%d;%d' %(nfn,','.join(d.keys()),len(x),smp))
        elif fn=='Bcknd_Init.txt':
            with open(pr,mode='r') as f: lines=f.readlines()
            lines=[indent*2+l.strip() for l in lines]
            paramsfromfile='\n'.join(lines)
    new_summ_lines=[csvstartstr,new_key_str]
    
    for t in sorted(tups):#this will only keep lines of summary for sample_no with individual sample files, and if there is an individual file not in the summary there will be an error
        i=summ_smps.index(t[0])
        new_summ_lines.append(','.join(['%d,%d,%d,%d,%d,%d,%d,%.5f,%.5f' %t]+[summ_keepstrs[i]]))
        
    
    filestr='\n'.join(new_summ_lines)
    with open(p_summ,mode='w') as f: f.write(filestr)
    
    s=anak
    s+=':\n    plate_ids: %d\n    analysis_fcn_version: 1\n    technique: rams\n    analysis_general_type: analysis_of_ana\n    description: multi-rank background identification and subtraction\n    name: Analysis__CU_Multi_Bcknd\n    parameters:\n        select_ana: ana__1\n%s\n        fom_segment_min_index_spacing: %d\n    plot_parameters:\n        plot__1:\n            x_axis: wavenumber._cm\n            series__1: smooth_signal_probability_pattern' \
           %(pid,paramsfromfile,fom_segment_min_index_spacing)
    analines=[s]
    analines.append('    files_multi_run:\n        fom_files:\n'+'\n'.join([indent*3+filedesc for filedesc in filelists[0]]))
    analines.append('        misc_files:\n'+'\n'.join([indent*3+filedesc for filedesc in filelists[1]]))
    analines.append('    files_run__1:\n        inter_rawlen_files:\n'+'\n'.join([indent*3+filedesc for filedesc in filelists[2]]))
    
    pana=os.path.join(anafolder,[fn for fn in os.listdir(anafolder) if fn.endswith('.ana')][0])
    with open(pana,mode='r') as f: fs=f.read()
    anafilestr='\n'.join([fs.strip()]+analines)
    with open(pana,mode='w') as f: f.write(anafilestr)
    with open(os.path.join(srcfolder,'anablock.txt'),mode='w') as f: f.write('\n'.join(analines))

#anafolder=r'L:\processes\analysis\rams\20181205.140000.run'
#
#for anaint,rank in [(2,1),(3,2),(4,4),(5,8)]:
#    foldname='rank%d_4832' %rank
#    anak='ana__%d' %(anaint)
#    srcfolder=os.path.join(r'D:\data\201812_MultiBcknd_4832',foldname)
#    import_CU_Multi_Bcknd_as_ana_block(srcfolder,anafolder,fom_segment_min_index_spacing=6,anak=anak)
    
