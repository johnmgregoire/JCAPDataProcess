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
from fcns_ui import *
from SaveImagesApp import *
from DBPaths import *

#runfoldername=r'eche\hte-eche-04\20170713_VFeNiO_35749\20170713.170645.copied-20170713174121573PDT.zip'
#runfoldername=r'eche\hte-eche-04\20170707_VFeCuO_35884'
runfoldername=None#mygetdir(parent=None, xpath=tryprependpath(RUNFOLDERS, 'eche'),markstr='select folder containing runs' )


#user-entered parameters for mA/cm2 calculation ond chooseing eqe plots

expsaveextension='.done'
anasaveextension='.run'


#providing these paths will skip the generation of the exp/ana
expname=None#r'L:\processes\experiment\eche\20171128.160211.done'#None#r'eche\20171115.163552.exp'#None#r'eche\20170727.133340.exp'#None#r'eche\20170727.173030'#None#r'eche\20170717.155030.run'#None#r'xrfs\20170518.122412'
ananame=r'L:\processes\analysis\temp\20190403.133916.run\20190403.133916.ana'#r'L:\processes\analysis\temp\20190402.124053.run\20190402.124053.ana'#None
eche_techniques='CV9'
lossfcns=['L2_3x_first_half_3x_positive','L2_5x_positive','L2', 'L1', 'LogCosh_1E9', 'L2_5x_first_half', 'L2_inv_prop_to_time']


expdestchoice='temp'
anadestchoice='temp'

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        #self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False)
        #self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data', GUIMODE=False)

#    def visui_exec(self, show=True):
#        if self.visdataui is None:
#            self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')
#        if show:
#            self.visdataui.show()
#        
#    def visexpana(self, anafiledict=None, anafolder=None, experiment_path=None, show=True):
#        self.visui_exec(show=show)
#        if not (anafiledict is None or anafolder is None):
#            self.visdataui.importana(anafiledict=anafiledict, anafolder=anafolder)
#        elif not experiment_path is None:
#            self.visdataui.importexp(experiment_path=experiment_path)
            
mainapp=QApplication(sys.argv)
form=MainMenu(None)

def openwindow():
    form.show()
    form.setFocus()
    form.calcui.show()
    mainapp.exec_()
    
#expui=form.expui
calcui=form.calcui
#visdataui=form.visdataui



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

def plot_new_fom(visdataui, fom_name):
    cb=visdataui.fomplotchoiceComboBox
    #print cb.count()
    for i in range(0, int(cb.count())):
        #print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if str(cb.itemText(i))==fom_name:
            cb.setCurrentIndex(i)
            visdataui.filterandplotfomdata()
            return True
        
    return False


calcui.importana(p=ananame)
for lossfcn in lossfcns:
    select_procana_fcn(calcui, 'ECMS_Fit_MS')
    calcui.analysisclass.params['eche_techniques']=eche_techniques
    calcui.analysisclass.params['loss_fcn']=lossfcn
    calcui.processeditedparams()
#    openwindow()
#    break
    calcui.analyzedata()
    
anasavefolder=calcui.saveana(dontclearyet=True, anatype=anadestchoice, rundone=anasaveextension)
openwindow()

#if expname is None:
#    if os.path.isdir(runfoldername):
#        runsrcfolder=runfoldername
#    else:
#        runsrcfolder=tryprependpath(RUNFOLDERS, runfoldername)
#
#    expui.importruns_folder(folderp=runsrcfolder)
#
#    expui.ExpTypeLineEdit.setText('eche')
#    expui.UserNameLineEdit.setText('eche')
#    expui.savebinaryCheckBox.setChecked(False)
#
#    expui.RunTypeLineEdit.setText('data')
#
#    mainitem=expui.techtypetreefcns.typewidgetItem
#    for i in range(mainitem.childCount()):
#        mainitem.child(i).setCheckState(0, Qt.Checked)
#
#    expui.editexp_addmeasurement()
#            
#    
#    expui.exec_()
#    saveexpfiledict, exppath=expui.saveexp(exptype=expdestchoice, rundone=expsaveextension)
#    
#else:
#    saveexpfiledict=None
#    exppath=buildexppath(expname)
#    #exppath=tryprependpath(EXPFOLDERS_J+EXPFOLDERS_L, expname)
#print exppath

#
#analysis_to_do_tups=[\
#        ('CA1','Iphoto',False,{'illum_key':illum_key},True),('CA2','Iphoto',False,{'illum_key':illum_key},True),('CA3','Iphoto',False,{'illum_key':illum_key},True),('CA4','Iphoto',False,{'illum_key':illum_key},True),\
#        ('CA1','SpectralPhoto',False,{},False),\
#        ('CV5','Iphoto',False,{'illum_key':illum_key},False),\
#        ('CV5','Pphotomax',False,{'v_extend_lower': -0.1, 'v_extend_upper': 0, 'sweep_direction': 'anodic'},True),\
#        ('CV5','Pphotomax',False,{'v_extend_lower': .03, 'v_extend_upper': 0, 'sweep_direction': 'anodic'},True),\
#        ('CV5','Pphotomax',False,{'v_extend_lower': -0.1, 'v_extend_upper': 0, 'sweep_direction': 'cathodic'},True),\
#        ('CV5','Pphotomax',False,{'v_extend_lower': .03, 'v_extend_upper': 0, 'sweep_direction': 'cathodic'},True),\
#        ]
#if ananame is None:
#    calcui.importexp(exppath=exppath)
#
#
#    currentana=1
#    for count,(techtypesearch, ana_fcn, isprocess, paramd,cm2convertbool) in enumerate(analysis_to_do_tups):
#        print 'calculating ana__%s, %s' %(currentana, ana_fcn)
#        #calcui.exec_()
#        select_techtype(techtypesearch)
#        if isprocess:
#            if not select_procana_fcn(calcui, ana_fcn):
#                calcui.exec_();raiseerror
#        else:
#            if not select_ana_fcn(calcui, ana_fcn):
#                calcui.exec_();raiseerror
#        if len(paramd)>0:
#            updateanalysisparams(calcui, paramd)
#        print 'parameters updated, performing calculation'
#        
#        calcuierror=calcui.analyzedata()
#        currentana+=1
#        
#        if calcuierror:
#            calcui.exec_();raiseerror
#        if cm2convertbool:
#            print 'converting to m*/cm2'
#            calcui.batch_set_params_for_photo_mAcm2_scaling(measurement_area=measurement_area_override)
#            
#            calcuierror=calcui.analyzedata()
#            currentana+=1
#            
#            if calcuierror:
#                calcui.exec_();raiseerror
#
#    #calcui.exec_()
#    pidstr=`calcui.expfiledict['run__1']['parameters']['plate_id']`
#    merge_interp_xrfs_single_plate_id(calcui, ananame=None, pidstr=pidstr, l_anak_to_merge=['ana__2', 'ana__4', 'ana__6', 'ana__8', 'ana__12'], save_extension=None)
#    anasavefolder=calcui.saveana(dontclearyet=True, anatype=anadestchoice, rundone='.run')
#
#    calcui.viewresult(anasavefolder=anasavefolder, show=False)
#else:
#    anapath=buildanapath(ananame)
#    anasavefolder=os.path.split(anapath)[0]
#    visdataui.importana(p=anapath)
#
#visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(9)
#visdataui.plot_preparestandardplot()
#choosexyykeys(visdataui, ['E.eV_illum', 'EQE', 'None'])
#for fn, filed in visdataui.anafiledict['ana__9']['files_multi_run']['sample_vector_files'].iteritems():
#    p=os.path.join(anasavefolder, fn)
#    vectrofiled=readcsvdict(p, filed, returnheaderdict=False, zipclass=None, includestrvals=False, delim=',')
#    if numpy.all(vectrofiled['EQE']>mineqeforplot):
#        filed['path']=os.path.join(anasavefolder, fn)
#        filed['zipclass']=False
#        visdataui.plotxy(filed=filed)
#        imagesidialog=visdataui.savefigs(justreturndialog=True)
#        imagesidialog.widget_plow_dlist[0]['item'].setCheckState(0, Qt.Unchecked)#plate
#        imagesidialog.widget_plow_dlist[1]['item'].setCheckState(0, Qt.Unchecked)#code
#        imagesidialog.widget_plow_dlist[2]['item'].setCheckState(0, Qt.Checked)#xy
#        imagesidialog.prependfilenameLineEdit.setText('ana__9-sample%d-' %filed['sample_no'])
#        imagesidialog.ExitRoutine()
#        
#stdplotinds=[2, 4, 6, 8,12, 14, 16, 18]# 
#for i in stdplotinds:
#    visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
#    visdataui.plot_preparestandardplot()
#    inds=numpy.where(numpy.logical_not(numpy.isnan(visdataui.fomplotd['fom'])))[0]
#    if len(inds)>0:
#        samplestoplot=list(visdataui.fomplotd['sample_no'][inds])
#        filterinds=[ind for ind, smp in enumerate(visdataui.fomplotd['sample_no']) if smp in samplestoplot]
#        for k in visdataui.fomplotd.keys():
#            if isinstance(visdataui.fomplotd[k], numpy.ndarray):
#                visdataui.fomplotd[k]=visdataui.fomplotd[k][filterinds]
#            else:
#                print k
#        vmin=max(0, visdataui.fomplotd['fom'].min())*0.99
#        vmax=numpy.percentile(visdataui.fomplotd['fom'], 95.)
#        if visdataui.fomplotd['fom'].max()<1.1*vmax:
#            vmax=visdataui.fomplotd['fom'].max()
#        if not numpy.all((visdataui.fomplotd['fom']<vmin)|(visdataui.fomplotd['fom']>vmax)):                
#            visdataui.vminmaxLineEdit.setText('%.3f,%.3f' %(vmin, vmax))
#            visdataui.plotfom()
#            visdataui.vminmaxLineEdit.setText('')
#            imagesidialog=visdataui.savefigs(justreturndialog=True)
#            imagesidialog.widget_plow_dlist[0]['item'].setCheckState(0, Qt.Checked)#plate
#            imagesidialog.widget_plow_dlist[1]['item'].setCheckState(0, Qt.Unchecked)#code
#            imagesidialog.widget_plow_dlist[2]['item'].setCheckState(0, Qt.Unchecked)#xy
#            imagesidialog.ExitRoutine()
#    if i>=12:
#        inds=numpy.where(numpy.logical_not(numpy.isnan(visdataui.fomplotd['fom'])) & (visdataui.fomplotd['fom']>=crit_pmax_mwcm2_for_fillfactor))[0]
#        if len(inds)>0:
#            samplestoplot=list(visdataui.fomplotd['sample_no'][inds])
#            plot_new_fom(visdataui, 'Fill_factor')
#            filterinds=[ind for ind, smp in enumerate(visdataui.fomplotd['sample_no']) if smp in samplestoplot]
#            for k in visdataui.fomplotd.keys():
#                if isinstance(visdataui.fomplotd[k], numpy.ndarray):
#                    visdataui.fomplotd[k]=visdataui.fomplotd[k][filterinds]
#                else:
#                    print k
#            vmin=max(0, visdataui.fomplotd['fom'].min())*0.99
#            vmax=min(0.8, visdataui.fomplotd['fom'].max())*1.01
#            if not numpy.all((visdataui.fomplotd['fom']<vmin)|(visdataui.fomplotd['fom']>vmax)):                
#                visdataui.vminmaxLineEdit.setText('%.3f,%.3f' %(vmin, vmax))
#                visdataui.plotfom()
#                visdataui.vminmaxLineEdit.setText('')
#                imagesidialog=visdataui.savefigs(justreturndialog=True)
#                imagesidialog.widget_plow_dlist[0]['item'].setCheckState(0, Qt.Checked)#plate
#                imagesidialog.widget_plow_dlist[1]['item'].setCheckState(0, Qt.Unchecked)#code
#                imagesidialog.widget_plow_dlist[2]['item'].setCheckState(0, Qt.Unchecked)#xy
#                if i==stdplotinds[-1] and 'done' in anasaveextension:#if need to convert to .done and skipped the fill factor plot, try this - not tested
#                    imagesidialog.doneCheckBox.setChecked(Qt.Checked)
#                    imagesidialog.ExitRoutine()
#                    visdataui.importana(p=imagesidialog.newanapath)
#                else:
#                    imagesidialog.ExitRoutine()
#        elif i==stdplotinds[-1] and 'done' in anasaveextension:#if need to convert to .done and skipped the fill factor plot, try this resave of last image- not tested
#            imagesidialog=visdataui.savefigs(justreturndialog=True)
#            imagesidialog.doneCheckBox.setChecked(Qt.Checked)
#            imagesidialog.ExitRoutine()
#            visdataui.importana(p=imagesidialog.newanapath)
#
#visdataui.exec_()
