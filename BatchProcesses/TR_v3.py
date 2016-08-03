skiponerror=1
batchfilepath=r'.batch'

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
#from CombineFomApp import combinefomDialog
#from FileSearchApp import filesearchDialog
#from FileManagementApp import filemanDialog
from fcns_io import *
from SaveImagesApp import *
from VisualizeBatchFcns import batch_plotuvisrefs

batchfolder=r'K:\users\sksuram\uvis_batchtests'
batchinput_fn='20160705.171153_batch_paulfnew2_InnerSpace.txt'


class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False)
        self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')

mainapp=QApplication(sys.argv)
form=MainMenu(None)
#form.show()
#form.setFocus()
#mainapp.exec_()
        
expui=form.expui
calcui=form.calcui
visdataui=form.visdataui

batchfilepath=os.path.join(batchfolder,batchinput_fn)
batch_stdout_path=batchfilepath.rpartition('.')[0]+'.out'

#sys.stdout=open(batch_stdout_path,'w')

#T_path: <>; exp_path: <>; ana_path: <>
with open(batchfilepath, mode='r') as f:
    batchlines=f.readlines()

logfilepath=batchfilepath.rpartition('.')[0]+'.log'

#runsrcfolder=tryprependpath(RUNFOLDERS, r'uvis\hte-uvis-02', testfile=False, testdir=True)
runsrcfolder=tryprependpath(RUNFOLDERS, '', testfile=False, testdir=True).rstrip(os.sep)

#update these to uvis when ready to run for real
expdestchoice=r'uvis'
anadestchoice=r'uvis'

#use these to create .exp or .ana even if in batch file
forceexp=False
forceana=False

getpvdbool=True

def getbatchlinepath(linestr, key='T_path'):
    return linestr.partition(key)[2].strip(':').strip().partition(';')[0].strip()
    
loglines=[fn for fn in batchlines]

def updatelog(i, s):
    s=s.strip()
    if len(s)==0:
        return
    
    if len(loglines[i].strip())>0:
        lst=[loglines[i].strip().split('\n')[0].split('\r')[0]]
    else:
        lst=[]
    lst+=[s]
    loglines[i]=';'.join(lst)
    with open(logfilepath, mode='w') as f:
        f.write('\n'.join(loglines))
        

def batch_pvdbool(fn):
    pT=os.path.join(runsrcfolder, fn)
    serialno=pT.rpartition('_')[2]
    plateidstr=serialno[:-1]
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
    return '', ('PVD' in methods, )
    
def batch_exp(fn, expui=expui):
    expui.removeruns()
    pT=os.path.join(runsrcfolder, fn)
    pR=os.path.join(runsrcfolder, fn.replace('_T-', '_R-'))
    
    if not os.path.isdir(pT):
        if skiponerror:
            return 'ERROR - cannot find file %s' %pT, False
        else:
            raiseerror
    if not os.path.isdir(pR):
        if skiponerror:
            return 'ERROR - cannot find file %s' %pR, False
        else:
            raiseerror
    
    for p in [pT, pR]:
        for zfn in os.listdir(p):
            if not zfn.endswith('.zip'):
                continue
            expui.importruns_folder(folderp=os.path.join(p, zfn))
    expui.batchuvissingleplate_norefdata()
    
    if (not 'experiment_type' in expui.expfiledict.keys()) or len(expui.expfilestr)==0 or not 'exp_version' in expui.expfilestr:
        if skiponerror:
            return 'ERROR - betchexp failed for %s' %pT, False
        else:
            raiseerror
    saveexpfiledict, exppath=expui.saveexp(exptype=expdestchoice, rundone='.done')
    return 'exp_path: %s' %exppath, (saveexpfiledict, exppath)
    
def select_ana_fcn(calcui, analabel):
    cb=calcui.AnalysisNamesComboBox
    #print cb.count()
    for i in range(1, int(cb.count())):
        #print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if (str(cb.itemText(i)).partition('(')[0].partition('__')[2])==analabel:
            cb.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            return True
    return False
    
for batchcount, batchline in enumerate(batchlines):
    print batchline
    expbool=False
    if forceexp or not 'exp_path' in batchline:
        rawfn=getbatchlinepath(batchline, key='T_path').lstrip(os.sep)
        logstr, tupbool=batch_exp(rawfn)
        updatelog(batchcount, logstr)
        if not tupbool:#error so False passed or empty tuple
            continue
        expfiledict, exppath=tupbool
        updatelog(batchcount, 'exp_path: %s' %exppath)
        expbool=True
    elif getpvdbool:
        rawfn=getbatchlinepath(batchline, key='T_path')
        
    if getpvdbool:
        logstr, tupbool=batch_pvdbool(rawfn)
        updatelog(batchcount, logstr)
        if not tupbool:#error so False passed or empty tuple
            continue
        pvdbool=tupbool[0]
    
    anabool=False
    if forceana or not 'ana_path' in batchline:
        if expbool:
            calcui.importexp(expfiledict=expfiledict, exppath=exppath)
            for runk, rund in calcui.expfiledict.iteritems():#copy over any platemap info
                if not runk.startswith('run__'):
                    continue
                rcpfile=rund['rcp_file']
                rcpdl=[rcpd for rcpd in expui.rcpdlist if rcpd['rcp_file']==rcpfile and len(rcpd['platemapdlist'])>0]
                if len(rcpdl)>0:
                    rund['platemapdlist']=copy.copy(rcpdl[0]['platemapdlist'])
        else:
            exppath=getbatchlinepath(batchline, key='exp_path')
            calcui.importexp(exppath=exppath)#relative path ok
        calcui.autoplotCheckBox.setChecked(False)
        for analabel in ['TR_UVVIS', 'BG']:#TODO: for BG run on the ana
            if not select_ana_fcn(calcui, analabel):
                if skiponerror:
                    updatelog(batchcount, 'ERROR-Analysis %s not available' %analabel)
                    continue
                else:
                    raiseerror
            calcuierror=calcui.analyzedata()#return False if ok otherwise stringh error message
            if calcuierror:
                if skiponerror:
                    updatelog(batchcount, 'ERROR-%s' %calcuierror)
                    continue
                else:
                    raiseerror
        anasavefolder=calcui.saveana(dontclearyet=True, anatype=anadestchoice, rundone='.run')
        calcui.viewresult(anasavefolder=anasavefolder, show=False)
        updatelog(batchcount, 'ana_path: %s' %anasavefolder)
        anabool=True
    
    if anabool or 'images saved' not in batchline:
        if not anabool and 'ana_path' in batchline:#didn't calculate ana here but ened to load it
            anapath=getbatchlinepath(batchline, key='ana_path')
            visdataui.importana(p=anapath)
        
        if visdataui.numStdPlots==0:
            if skiponerror:
                updatelog(batchcount, 'ERROR- No standard plots in vis')
                continue
            else:
                raiseerror
            
        comboind_strlist=[]
        for i in range(1, visdataui.numStdPlots+1):
            visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
            comboind_strlist+=[(i, str(visdataui.stdcsvplotchoiceComboBox.currentText()))]
    
        for tech in ['T_UVVIS', 'R_UVVIS']:
            batch_plotuvisrefs(visdataui, tech=tech)
            idialog=visdataui.savefigs(save_all_std_bool=False, batchidialog=None, lastbatchiteration=False, filenamesearchlist=[['xy']], justreturndialog=True, prependstr=tech)
            idialog.doneCheckBox.setChecked(False)
            idialog.ExitRoutine()
            if idialog.newanapath:
                visdataui.importana(p=idialog.newanapath)
        batchidialog=saveimagesbatchDialog(None, comboind_strlist)
        
        fnsearchle='plate_id__'
        if not pvdbool:#if PVD bool then don't save composition plots
            fnsearchle+=',code__'
        batchidialog.filenamesearchLineEdit.setText(fnsearchle)
        batchidialog.ExitRoutine()
        visdataui.save_all_std_plots(batchidialog=batchidialog)
        
        #save version of FOM plots with 1.6 to 2.6 eV range
        visdataui.colormapLineEdit.setText('jet_r')
        visdataui.vminmaxLineEdit.setText('1.8,2.8')
        visdataui.belowrangecolLineEdit.setText('(1,0.5,0.5)')
        visdataui.aboverangecolLineEdit.setText('(0.3,0,0.5)')
        batchidialog.plotstyleoverrideCheckBox.setChecked(True)
        batchidialog.prependfilenameLineEdit.setText('1.6to2.6')
        fnsearchle='plate_id__&bg_repr'
        if not pvdbool:#if PVD bool then don't save composition plots
            fnsearchle+=',code__&bg_repr'
        batchidialog.filenamesearchLineEdit.setText(fnsearchle)
        batchidialog.doneCheckBox.setChecked(False)
        batchidialog.ExitRoutine()
        visdataui.save_all_std_plots(batchidialog=batchidialog)
        updatelog(batchcount, 'images saved')
        
