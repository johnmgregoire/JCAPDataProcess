import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    #Needed for running line-by-line
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\BatchProcesses\merge_xrfs_into_ana_v7_2frame_from_J_ana.py'
    try:
        p=os.path.split(os.path.realpath(__file__))[0]
    except:
        p=os.getcwd()
    sys.path.append(os.path.split(p)[0])
    sys.path.append(os.path.join(os.path.split(p)[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(p)[0], 'AnalysisFunctions'))
#import matplotlib.pyplot as plt
from fcns_io import *
from fcns_ui import *
from CalcFOMApp import calcfomDialog
from Analysis_Master import Analysis_Master_nointer
from create_udi_standalone import append_udi_to_ana, append_resampled_merged_patterns_to_ana, smoothfcn
analysismasterclass=Analysis_Master_nointer()

processed_patterns=True
include_1st_frame_solo=False
merge_first=True
class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False, modifyanainplace=False)

mainapp=QApplication(sys.argv)
form=MainMenu(None)
calcui=form.calcui
calcui.getplatemapCheckBox.setChecked(True)


#serial_list=''.split(',')


#plate_list='1389,4847,5037,5035,5036'.split(',')
#plate_list=[s[:-1] for s in serial_list]
#plate_list=plate_list[plate_list.index('4847'):]
#plate_list=['3557']
#plate_list=plate_list[1:]

plate_list='3581,3591,3593'.split(',')

for pid in plate_list:
    print('STARTING ',pid)
    d=importinfo(pid)
    if 0:
        els='-'.join([el for el in getelements_plateidstr(pid) if not el in ['Ar']])
        els+='/Pt' if True in ['Pt' in pd['elements'] for pd in list(d['prints'].values())] else ('/'+d['substrate'])
        print(d['serial_no'],'\t',els)
    if not 'analyses' in d:
        continue
    l=[]
    for k,ad in list(d['analyses'].items()):
        if ad['type']=='xrds':
            l+=[(float(os.path.split(ad['path'])[1][:15]),ad['path'])]
    if len(l)==0: continue
#    if pid=='3587':
#        most_recent_xrds=sorted(l)[-2][1]
#    else:
    most_recent_xrds=sorted(l)[-1][1]#If phase mapping or othr analysis done for this plate then most recent probably isn't the desired one so TODO could be to check for the 
    
    l=[]
    for k,ad in list(d['analyses'].items()):
        if ad['type']=='xrfs':
            l+=[(float(os.path.split(ad['path'])[1][:15]),ad['path'])]
    if len(l)==0: continue
    most_recent_xrfs=sorted(l)[-1][1]
    print(most_recent_xrfs)
    p=buildanapath(most_recent_xrds)
    
    #break#TEMP

    #import to create tmep folder and delete anything past ana__4, which are the 4 ana created during external import    
    calcui.importana(p=p)
    anakeys=sort_dict_keys_by_counter(calcui.anadict, keystartswith='ana__')
    for anak in anakeys[4:][::-1]:
        calcui.clearsingleanalysis(anak=anak)
    
    #if ana__2 has no fom csv, make one
    anak='ana__2'
    if not ('files_multi_run' in list(calcui.anadict[anak].keys()) and 'fom_files' in list(calcui.anadict[anak]['files_multi_run'].keys())):
        calcui.create_default_fom_csv_from_runfiles(anak)
    
    #import xrfs and merge with ana__2 to create ana__5
    calcui.importauxexpana(buildanapath(most_recent_xrfs), exp=False)
    
    for i in range(1, int(calcui.FOMProcessNamesComboBox.count())):
        if (str(calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__FOM_Interp_Merge_Ana':
            calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            calcui.processeditedparams()
            break
    #calcui.exec_()
    c=calcui.analysisclass
    c.params['select_ana']='ana__2'
    c.params['select_aux_keys']='AtFrac'
    c.params['aux_ana_ints']='2'
    c.params['interp_is_comp']=1
    c.processnewparams(calcFOMDialogclass=calcui, recalc_filedlist=True)
    

    
    tempnum=len(sort_dict_keys_by_counter(calcui.anadict, keystartswith='ana__'))
    calcui.analyzedata()
    anakeys=sort_dict_keys_by_counter(calcui.anadict, keystartswith='ana__')
    if len(anakeys)==tempnum:
        print('***; %s; %s' %(buildanapath(most_recent_xrfs), pid))
        continue
        #calcui.exec_()#WILL STOP HERE IF ERROR IN XRFS MERGE
    xrfsmergedanak=anakeys[-1]
    #continue#this skips all file writing until the xrfs ana are fixed
    newanasavefolder=calcui.saveana(dontclearyet=False, anatype='xrds', rundone='.run')

    newanapath=buildanapath(newanasavefolder)
    #now have core ana saved as .run and modify in place
    num_ana_blocks=len(anakeys)
    

    #first create separate udi for the RAW 1st and 2nd frame - ana__6 and 7
    q_key='q.nm'
    intensity_key='intensity.counts'
    anak_patterns='ana__2'
    pattern_fn_search_str='1st_frame'
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_fn_search_str=pattern_fn_search_str, pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)    
    num_ana_blocks+=1
    pattern_fn_search_str='2nd_frame'    
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_fn_search_str=pattern_fn_search_str, pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)    
    num_ana_blocks+=1
    pattern_fn_search_str='3rd_frame'    
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_fn_search_str=pattern_fn_search_str, pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)    
    num_ana_blocks+=1

    #lin resam merge ana__1, which is bcknd-sub data, and then append udi - ana__8 and 9
    q_key='q.nm_processed'
    intensity_key='intensity.counts_processed'
    append_resampled_merged_patterns_to_ana(l_anapath=[newanapath,newanapath,newanapath], l_anak_patterns=['ana__1', 'ana__1', 'ana__1'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame','3rd_frame'], pattern_key='pattern_files', q_key=q_key,intensity_key=intensity_key, dq=None, q_log_space_coef=None, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
    num_ana_blocks+=1
    
    q_key='q.nm_processed_resampled'
    intensity_key='intensity.counts_processed_resampled'
    anak_patterns='ana__%d' %(num_ana_blocks)
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)
    num_ana_blocks+=1
    
    
    #log resam merge ana__1, which is bcknd-sub data, and then append udi - ana__10 and 11
    q_key='q.nm_processed'
    intensity_key='intensity.counts_processed'
    append_resampled_merged_patterns_to_ana(l_anapath=[newanapath,newanapath,newanapath], l_anak_patterns=['ana__1', 'ana__1', 'ana__1'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame','3rd_frame'], pattern_key='pattern_files', q_key=q_key,intensity_key=intensity_key, dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
    num_ana_blocks+=1
    
    q_key='q.nm_processed_resampled'
    intensity_key='intensity.counts_processed_resampled'
    anak_patterns='ana__%d' %(num_ana_blocks)
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)
    num_ana_blocks+=1

    #lin resam merge ana__2, which is raw, and then append udi - ana__12 and 13
    q_key='q.nm'
    intensity_key='intensity.counts'
    append_resampled_merged_patterns_to_ana(l_anapath=[newanapath,newanapath,newanapath], l_anak_patterns=['ana__2', 'ana__2', 'ana__2'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame','3rd_frame'], pattern_key='pattern_files', q_key=q_key,intensity_key=intensity_key, dq=None, q_log_space_coef=None, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
    num_ana_blocks+=1
    
    q_key='q.nm_resampled'
    intensity_key='intensity.counts_resampled'
    anak_patterns='ana__%d' %(num_ana_blocks)
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)
    num_ana_blocks+=1
    
    #log resam merge ana__2, which is raw, and then append udi - ana__14 and 15
    q_key='q.nm'
    intensity_key='intensity.counts'
    append_resampled_merged_patterns_to_ana(l_anapath=[newanapath,newanapath,newanapath], l_anak_patterns=['ana__2', 'ana__2', 'ana__2'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame','3rd_frame'], pattern_key='pattern_files', q_key=q_key,intensity_key=intensity_key, dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
    num_ana_blocks+=1
    
    q_key='q.nm_resampled'
    intensity_key='intensity.counts_resampled'
    anak_patterns='ana__%d' %(num_ana_blocks)
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)
    num_ana_blocks+=1


    print(pid,',',num_ana_blocks,',',newanapath)
    
    
    
    
    
    
    