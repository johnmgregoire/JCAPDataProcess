import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
    
from fcns_io import *
from fcns_ui import *
from CalcFOMApp import calcfomDialog
from Analysis_Master import Analysis_Master_nointer
from create_udi_standalone import append_udi_to_ana
analysismasterclass=Analysis_Master_nointer()


class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False)

mainapp=QApplication(sys.argv)
form=MainMenu(None)
calcui=form.calcui

folder=r'L:\processes\analysis\ssrl'
fns=[fn for fn in os.listdir(folder) if fn.endswith('.run')]#20170922.125037.run and 20170922.124034.run
for fn in fns:
    anafolder=os.path.join(folder, fn)
    if True in [s.startswith('ana__6_') for s in os.listdir(anafolder)]:
        print('skipping becuase already done ', fn)
    p=os.path.join(anafolder, fn[:-3]+'ana')
    calcui.importana(p=p)
    pidstr=calcui.anadict['plate_ids']
    if ',' in pidstr:
        print('skipping ', fn, pidstr)
        continue
    infod=importinfo(pidstr)
    #for ank in sort_dict_keys_by_counter(infod['analyses'], keystartswith='analyses__'):#use 
    analysesd=infod['analyses']
    xrfstups=sorted([(time.strptime(v['created_at'].rpartition(' ')[0],'%Y-%m-%d %H:%M:%S'), v) for k, v in analysesd.items() if v['type']=='xrfs'])
    if len(xrfstups)==0:
        print('no xrfs data for ', fn)
        continue
    relapth_xrfsana=xrfstups[-1][1]['path']#latest created_at analyses__ dict
    
    calcui.importauxexpana(relapth_xrfsana, exp=False)
            
            
    for i in range(1, int(calcui.FOMProcessNamesComboBox.count())):
        if (str(calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__FOM_Interp_Merge_Ana':
            calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            calcui.processeditedparams()
            break
    c=calcui.analysisclass
    c.params['select_aux_keys']='AtFrac'
    c.params['select_aux_ints']='2'
    c.params['interp_is_comp']=1
    c.processnewparams(calcFOMDialogclass=calcui, recalc_filedlist=True)
    #calcui.exec_()
    calcui.analyzedata()
    if not 'ana__4' in list(calcui.anadict.keys()):
        print('***; %s; %s' %(relapth_xrfsana, fn))
        continue
        calcui.exec_()
    #continue#this skips all file writing until the xrfs ana are fixed
    newanasavefolder=calcui.saveana(dontclearyet=False, anatype='ssrl', rundone='.run')
    newanapath=buildanapath(newanasavefolder)
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__4'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_processed',intensity_key='intensity.counts_processed')
    append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__4'], l_anak_patterns=['ana__1'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm',intensity_key='intensity.counts')
