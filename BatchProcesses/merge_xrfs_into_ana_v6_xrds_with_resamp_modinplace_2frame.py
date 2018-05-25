import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
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
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False, modifyanainplace=True)

mainapp=QApplication(sys.argv)
form=MainMenu(None)
calcui=form.calcui
calcui.getplatemapCheckBox.setChecked(True)
folder=r'L:\processes\analysis\xrds'
#fns=[fn for fn in os.listdir(folder) if fn.endswith('.run')]#20170922.125037.run and 20170922.124034.run

if 0:
    xrdsnames=r'xrds\20180524.122602.run'.split(',')
    xrfsnames=r'xrfs\20180524.153248.done'.split(',')
elif 0:
    xrdsnames=r'xrds\20180524.130338.run'.split(',')
    xrfsnames=r'xrfs\20180524.152919.done'.split(',')
elif 1:
    xrdsnames=r'xrds\20180524.133941.run'.split(',')
    xrfsnames=r'xrfs\20180524.154943.done'.split(',')
fns=[tup for tup in zip(xrdsnames, xrfsnames)]
for fn_or_tup in fns:
    print 'starting ', fn_or_tup
    if isinstance(fn_or_tup, str):
        anafolder=os.path.join(folder, fn)
    #    if True in [s.startswith('ana__6_') for s in os.listdir(anafolder)]:
    #        print 'skipping becuase already done ', fn
        p=os.path.join(anafolder, fn.rpartition('.')[0]+'.ana')
    else:
        p=buildanapath(fn_or_tup[0])

    num_ana_for_resamp=(int(include_1st_frame_solo)+1)*(int(processed_patterns)+1)
    resamp_ana_are_processed=[False]*num_ana_for_resamp
    if processed_patterns:
        resamp_ana_are_processed[0]=True
        if include_1st_frame_solo:
            resamp_ana_are_processed[2]=True
    #ana__1 to 4 should be created by data import. then create ana__5 to 8 here
    if merge_first and processed_patterns:#should generate 5,6,7,8 or just 5,6
        append_resampled_merged_patterns_to_ana(l_anapath=[p, p], l_anak_patterns=['ana__1', 'ana__1'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame'], pattern_key='pattern_files', q_key='q.nm_processed',intensity_key='intensity.counts_processed', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
        append_resampled_merged_patterns_to_ana(l_anapath=[p, p], l_anak_patterns=['ana__2', 'ana__2'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame'], pattern_key='pattern_files', q_key='q.nm',intensity_key='intensity.counts', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
        if include_1st_frame_solo:
            append_resampled_merged_patterns_to_ana(l_anapath=[p], l_anak_patterns=['ana__1'],  l_pattern_fn_search_str=['1st_frame'], pattern_key='pattern_files', q_key='q.nm_processed',intensity_key='intensity.counts_processed', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
            append_resampled_merged_patterns_to_ana(l_anapath=[p], l_anak_patterns=['ana__2'],  l_pattern_fn_search_str=['1st_frame'], pattern_key='pattern_files', q_key='q.nm',intensity_key='intensity.counts', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
    elif merge_first and not processed_patterns: #should generate 4,5 or just 4
        append_resampled_merged_patterns_to_ana(l_anapath=[p, p], l_anak_patterns=['ana__2', 'ana__2'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame'], pattern_key='pattern_files', q_key='q.nm',intensity_key='intensity.counts', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
        if include_1st_frame_solo:
            append_resampled_merged_patterns_to_ana(l_anapath=[p], l_anak_patterns=['ana__2'],  l_pattern_fn_search_str=['1st_frame'], pattern_key='pattern_files', q_key='q.nm',intensity_key='intensity.counts', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)

    calcui.importana(p=p)
    
    anakeys_after_append=sort_dict_keys_by_counter(calcui.anadict, keystartswith='ana__')
    resamp_anakeys=anakeys_after_append[-num_ana_for_resamp:]
    print 'after merge then reimport ', calcui.anadict['experiment_name']
    pidstr=calcui.anadict['plate_ids']
    if ',' in pidstr:
        print 'skipping ', fn, pidstr
        continue
        
    if isinstance(fn_or_tup, str):
        infod=importinfo(pidstr)
        #for ank in sort_dict_keys_by_counter(infod['analyses'], keystartswith='analyses__'):#use 
        analysesd=infod['analyses']
        xrfstups=sorted([(time.strptime(v['created_at'].rpartition(' ')[0],'%Y-%m-%d %H:%M:%S'), v) for k, v in analysesd.iteritems() if v['type']=='xrfs'])
        if len(xrfstups)==0:
            print 'no xrfs data for ', fn
            continue
        relapth_xrfsana=xrfstups[-1][1]['path']#latest created_at analyses__ dict
        print 'using xrfs ', relapth_xrfsana
        xrfsp=relapth_xrfsana
    else:
        xrfsp=buildanapath(fn_or_tup[1])
    calcui.importauxexpana(xrfsp, exp=False)

    for i in range(1, int(calcui.FOMProcessNamesComboBox.count())):
        if (str(calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__FOM_Interp_Merge_Ana':
            calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            calcui.processeditedparams()
            break
    #calcui.exec_()
    c=calcui.analysisclass
    c.params['select_aux_keys']='AtFrac'
    c.params['select_aux_ints']='2'
    c.params['interp_is_comp']=1
    c.processnewparams(calcFOMDialogclass=calcui, recalc_filedlist=True)
    

    
    tempnum=len(sort_dict_keys_by_counter(calcui.anadict, keystartswith='ana__'))
    calcui.analyzedata()
    anakeys=sort_dict_keys_by_counter(calcui.anadict, keystartswith='ana__')
    if len(anakeys)==tempnum:
        print '***; %s; %s' %(relpath_xrfsana, fn)
        #continue
        calcui.exec_()
    xrfsmergedanak=anakeys[-1]
    #continue#this skips all file writing until the xrfs ana are fixed
    newanasavefolder=calcui.saveana(dontclearyet=False, anatype='xrds', rundone='.run')

    newanapath=buildanapath(newanasavefolder)
    
    for anak_patterns, isprocessed in zip(resamp_anakeys, resamp_ana_are_processed):
        q_key='q.nm_processed_resampled' if isprocessed else 'q.nm_resampled'
        intensity_key='intensity.counts_processed_resampled' if isprocessed else 'intensity.counts_resampled'
        append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=[xrfsmergedanak], l_anak_patterns=[anak_patterns], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key)
    #break#have only tested modify in place with a single .ana at a time

