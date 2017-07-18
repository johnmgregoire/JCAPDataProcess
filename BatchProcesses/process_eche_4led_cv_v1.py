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
from SaveImagesApp import *
from DBPaths import *


#runfoldername=r'eche\hte-eche-04\20170713_VFeNiO_35749\20170713.170645.copied-20170713174121573PDT.zip'
runfoldername=r'eche\hte-eche-04\20170707_VFeCuO_35884'


#user-entered parameters for mA/cm2 calculation ond chooseing eqe plots
measurement_area_override=0.58#None to use exp value
mineqeforplot=1.e-4

expsaveextension='.done'
anasaveextension='.run'


#providing these paths will skip the generation of the exp/ana
expname=None#r'eche\20170717.155030.run'#None#r'xrfs\20170518.122412'
anarunpath=None#r'L:\processes\analysis\eche\20170717.155712.run\20170717.155712.ana'

expdestchoice='eche'
anadestchoice='eche'

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False)
        self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data', GUIMODE=False)

    def visui_exec(self, show=True):
        if self.visdataui is None:
            self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')
        if show:
            self.visdataui.show()
        
    def visexpana(self, anafiledict=None, anafolder=None, experiment_path=None, show=True):
        self.visui_exec(show=show)
        if not (anafiledict is None or anafolder is None):
            self.visdataui.importana(anafiledict=anafiledict, anafolder=anafolder)
        elif not experiment_path is None:
            self.visdataui.importexp(experiment_path=experiment_path)
            
mainapp=QApplication(sys.argv)
form=MainMenu(None)
#form.show()
#form.setFocus()
#mainapp.exec_()
        
expui=form.expui
calcui=form.calcui
visdataui=form.visdataui


    
def select_ana_fcn(calcui, analabel):
    calcui.FOMProcessNamesComboBox.setCurrentIndex(0)
    cb=calcui.AnalysisNamesComboBox
    #print cb.count()
    for i in range(1, int(cb.count())):
        #print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if (str(cb.itemText(i)).partition('(')[0].partition('__')[2])==analabel:
            
            cb.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            return True
    return False
    

def select_procana_fcn(calcui, analabel):
    cb=calcui.FOMProcessNamesComboBox
    #print cb.count()
    for i in range(1, int(cb.count())):
        #print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if (str(cb.itemText(i)).partition('(')[0].partition('__')[2])==analabel:
            cb.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            return True
    return False

def updateanalysisparams(calcui, paramd):
    calcui.analysisclass.params.update(paramd)
    calcui.processeditedparams()
    #calcui.analysisclass.processnewparams(calcFOMDialogclass=calcui)

def select_techtype(searchstr):
    qlist=calcui.TechTypeButtonGroup.buttons()
    typetechfound=False
    for button in qlist:
        if searchstr in str(button.text()).strip():
            button.setChecked(True)
            typetechfound=True
            break
    calcui.fillanalysistypes(calcui.TechTypeButtonGroup.checkedButton())
    if not typetechfound:
        calcui.exec_();raiseerror
    
    
if expname is None:
    runsrcfolder=tryprependpath(RUNFOLDERS, runfoldername)

    expui.importruns_folder(folderp=runsrcfolder)

    expui.ExpTypeLineEdit.setText('eche')
    expui.UserNameLineEdit.setText('eche')
    expui.savebinaryCheckBox.setChecked(False)

    expui.RunTypeLineEdit.setText('data')

    mainitem=expui.techtypetreefcns.typewidgetItem
    for i in range(mainitem.childCount()):
        mainitem.child(i).setCheckState(0, Qt.Checked)

    expui.editexp_addmeasurement()
            
    
    expui.exec_()
    saveexpfiledict, exppath=expui.saveexp(exptype=expdestchoice, rundone=expsaveextension)
    
else:
    saveexpfiledict=None
    exppath=buildexppath(expname)
    #exppath=tryprependpath(EXPFOLDERS_J+EXPFOLDERS_L, expname)


print exppath
if anarunpath is None:
    calcui.importexp(exppath=exppath)


    currentana=1
    for count,(techtypesearch, ana_fcn, isprocess, paramd,cm2convertbool) in enumerate([\
        ('CA1','Iphoto',False,{},True),('CA2','Iphoto',False,{},True),('CA3','Iphoto',False,{},True),('CA4','Iphoto',False,{},True),\
        ('CA1','SpectralPhoto',False,{},False),\
        ('CV5','Iphoto',False,{},False),\
        ('CV5','Pphotomax',False,{'v_extend_lower': -0.1, 'v_extend_upper': 0, 'sweep_direction': -1},True),\
        ('CV5','Pphotomax',False,{'v_extend_lower': .03, 'v_extend_upper': 0, 'sweep_direction': -1},True),\
        ('CV5','Pphotomax',False,{'v_extend_lower': -0.1, 'v_extend_upper': 0, 'sweep_direction': 1},True),\
        ('CV5','Pphotomax',False,{'v_extend_lower': .03, 'v_extend_upper': 0, 'sweep_direction': 1},True),\
        ]):
        
        select_techtype(techtypesearch)
        if isprocess:
            if not select_procana_fcn(calcui, ana_fcn):
                calcui.exec_();raiseerror
        else:
            if not select_ana_fcn(calcui, ana_fcn):
                calcui.exec_();raiseerror
        if len(paramd)>0:
            updateanalysisparams(calcui, paramd)
        calcuierror=calcui.analyzedata()
        currentana+=1
        
        if calcuierror:
            calcui.exec_();raiseerror
        if cm2convertbool:
            calcui.batch_set_params_for_photo_mAcm2_scaling(measurement_area=measurement_area_override)
            
    #        if not select_ana_fcn(calcui, 'Process_B_vs_A_ByRun'):
    #            calcui.exec_();raiseerror
    #        runintliststr=','.join([`ri` for ri in sorted(list(set([d['runint'] for d in calcui.fomdlist])))])
    #        Btrliststr='I.A_photo,I.A_photo_ill,I.A_photo_dark' if ana_fcn=='Iphoto' else 'Pmax.W,Ipmax.A,Isc.A'
    #        keys_to_keep='' if ana_fcn=='Iphoto' else 'Voc.V,Vpmax.V,Fill_factor'
    #        relative_key_append='_mcm2'
    #        Atrliststr=','.join([mpercm2_factor_str]*(Btrliststr.count(',')))
    #        calcui.analysisclass.params.update(calcui.analysisclass.dfltparams)
    #        updateanalysisparams(calcui, {'select_ana': 'ana__%d' %(currentana-1), \
    #            'fom_keys_B':Btrliststr, 'fom_keys_A':Atrliststr, 'runints_B':runintliststr, 'runints_A':runintliststr,\
    #            'keys_to_keep':keys_to_keep,'relative_key_append':relative_key_append,'method':'B_over_A'})
            calcuierror=calcui.analyzedata()
            currentana+=1
            
            if calcuierror:
                calcui.exec_();raiseerror

    calcui.exec_()
    anasavefolder=calcui.saveana(dontclearyet=True, anatype=anadestchoice, rundone='.run')

    calcui.viewresult(anasavefolder=anasavefolder, show=False)
else:
    anasavefolder=os.path.split(anarunpath)[0]
    visdataui.importana(p=anarunpath)

visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(9)
choosexyykeys(visdataui, ['E.eV_illum', 'EQE', 'None'])
for fn, filed in visdataui.anafiledict['ana__9']['files_multi_run']['sample_vector_files'].iteritems():
    p=os.path.join(anasavefolder, fn)
    vectrofiled=readcsvdict(p, filed, returnheaderdict=False, zipclass=None, includestrvals=False, delim=',')
    if numpy.all(vectrofiled['EQE']>mineqeforplot):
        filed['path']=os.path.join(anasavefolder, fn)
        filed['zipclass']=False
        visdataui.plotxy(filed=filed)
        imagesidialog=visdataui.savefigs(justreturndialog=True)
        imagesidialog.widget_plow_dlist[0]['item'].setCheckState(0, Qt.Unchecked)#plate
        imagesidialog.widget_plow_dlist[1]['item'].setCheckState(0, Qt.Unchecked)#code
        imagesidialog.widget_plow_dlist[2]['item'].setCheckState(0, Qt.Checked)#xy
        imagesidialog.prependfilenameLineEdit.setText('ana__9-sample%d-' %filed['sample_no'])
        imagesidialog.ExitRoutine()
        
stdplotinds=[2, 4, 6, 8, 12, 14, 16, 18]
for i in stdplotinds:
    visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
    visdataui.plot_preparestandardplot()
    imagesidialog=visdataui.savefigs(justreturndialog=True)
    imagesidialog.widget_plow_dlist[0]['item'].setCheckState(0, Qt.Checked)#plate
    imagesidialog.widget_plow_dlist[1]['item'].setCheckState(0, Qt.Unchecked)#code
    imagesidialog.widget_plow_dlist[2]['item'].setCheckState(0, Qt.Unchecked)#xy
    if i==stdplotinds[-1] and 'done' in anasaveextension:
        imagesidialog.doneCheckBox.setChecked(Qt.Checked)
        imagesidialog.ExitRoutine()
        visdataui.importana(p=imagesidialog.newanapath)
    else:
        imagesidialog.ExitRoutine()


visdataui.exec_()
