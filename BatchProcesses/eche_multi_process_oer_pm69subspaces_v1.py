import sys, os
from time import sleep
import numpy
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

# def openwindow():
#     form.show()
#     form.setFocus()
#     form.calcui.show()
#     mainapp.exec_()


# expui=form.expui
# visdataui=form.visdataui


def select_ana_fcn(calcui, analabel):
    calcui.FOMProcessNamesComboBox.setCurrentIndex(0)
    cb = calcui.AnalysisNamesComboBox
    # print cb.count()
    for i in range(1, int(cb.count())):
        # print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if (str(cb.itemText(i)).partition('(')[0].partition('__')[2]) == analabel:

            cb.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            return True
    return False


def select_procana_fcn(calcui, analabel):
    cb = calcui.FOMProcessNamesComboBox
    # print cb.count()
    for i in range(1, int(cb.count())):
        # print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if (str(cb.itemText(i)).partition('(')[0].partition('__')[2]) == analabel:
            cb.setCurrentIndex(i)
            calcui.getactiveanalysisclass()
            return True
    return False


def updateanalysisparams(calcui, paramd):
    calcui.analysisclass.params.update(paramd)
    calcui.processeditedparams()
    # calcui.analysisclass.processnewparams(calcFOMDialogclass=calcui)


def select_techtype(searchstr):
    qlist = calcui.TechTypeButtonGroup.buttons()
    typetechfound = False
    for button in qlist:
        if searchstr in str(button.text()).strip():
            button.setChecked(True)
            typetechfound = True
            break
    calcui.fillanalysistypes(calcui.TechTypeButtonGroup.checkedButton())
    if not typetechfound:
        calcui.exec_()
        raiseerror


def plot_new_fom(visdataui, fom_name):
    cb = visdataui.fomplotchoiceComboBox
    # print cb.count()
    for i in range(0, int(cb.count())):
        # print(str(cb.itemText(i)).partition('(')[0].partition('__')[2])
        if str(cb.itemText(i)) == fom_name:
            cb.setCurrentIndex(i)
            visdataui.filterandplotfomdata()
            return True

    return False




runfoldername = None
expsaveextension = '.done'
anasaveextension = '.run'

# providing these paths will skip the generation of the exp/ana
expname = None
expdestchoice = 'eche'
anadestchoice = 'eche'

# explst = [
#     ('L:/processes/experiment/eche/20190501.125714.copied-20190501221215867PDT/20190501.125714.exp', (0.48, 1.0), (0.5, 1.0)), # 7
#     ('L:/processes/experiment/eche/20190416.140535.copied-20190416220707052PDT/20190416.140535.exp', (0.48, 1.0), (0.5, 1.0)), # 7
#     ('L:/processes/experiment/eche/20190415.115538.copied-20190415220556175PDT/20190415.115538.exp', (0.48, 1.0), (0.5, 1.0)), # 7
#     ('L:/processes/experiment/eche/20180411.141724.copied-20180411220901744PDT/20180411.141724.exp', (0.48, 1.0), (0.5, 1.0)), # 3
#     ('L:/processes/experiment/eche/20180411.152214.copied-20180411220901744PDT/20180411.152214.exp', (0.48, 1.0), (0.5, 1.0)), # 3
#     ('L:/processes/experiment/eche/20180411.154249.copied-20180411220901744PDT/20180411.154249.exp', (0.48, 1.0), (0.5, 1.0)), # 3
#     ('L:/processes/experiment/eche/20170828.170010.copied-20170828220902243PDT/20170828.170010.exp', (0.48, 0.9), (0.5, 0.9)), # 9
#     ('L:/processes/experiment/eche/20170828.165552.copied-20170828220902243PDT/20170828.165552.exp', (0.48, 0.9), (0.5, 0.9)), # 9
#     ('L:/processes/experiment/eche/20170828.165831.copied-20170828220902243PDT/20170828.165831.exp', (0.48, 0.9), (0.5, 0.9)), # 9
#     ('L:/processes/experiment/eche/20170823.145121.copied-20170823194838230PDT/20170823.145121.exp', (0.32, 0.6), (0.35, 0.65)), # 13
#     ('L:/processes/experiment/eche/20170823.143138.copied-20170823194838230PDT/20170823.143138.exp', (0.32, 0.6), (0.35, 0.65)), # 13
#     ('L:/processes/experiment/eche/20170823.151056.copied-20170823194838230PDT/20170823.151056.exp', (0.32, 0.6), (0.35, 0.65)) # 13
#     ]

# explst = [
#     ('L:/processes/experiment/eche/20190814.210551.done/20190814.210551.exp', (0.32, 0.6), (0.35, 0.65)), # 13
#     ]

# explst = [
#     ('L:/processes/experiment/eche/20190819.120802.done/20190819.120802.exp', (0.48, 1.0), (0.5, 1.0)),
#     ('L:/processes/experiment/eche/20190819.120931.done/20190819.120931.exp', (0.48, 1.0), (0.5, 1.0))
# ]

# 9/20 update TRI dataset
# explst = [
#     ('L:/processes/experiment/eche/20161208.093513.copied-20161208221238642PST/20161208.093513.exp',
#      (0.32, 0.6), (0.35, 0.65)),
#     ('L:/processes/experiment/eche/20160705.085609.copied-20160705220726116PDT/20160705.085609.exp',
#      (0.32, 0.6), (0.35, 0.65)),
#     ('L:/processes/experiment/eche/20170301.101901.copied-20170308132955800PST/20170301.101901.exp',
#      (0.32, 0.6), (0.35, 0.65)),
#     ('L:/processes/experiment/eche/20190520.161947.copied-20190520221254058PDT/20190520.161947.exp',
#      (0.32, 0.6), (0.35, 0.65)),
#     ('L:/processes/experiment/eche/20170823.145121.copied-20170823194838230PDT/20170823.145121.exp',
#      (0.32, 0.6), (0.35, 0.65)),
# ]
# 9/20 reprocess 4098
# explst = [
#     ('L:/processes/experiment/eche/20190920.110322.done/20190920.110322.exp',
#      (0.32, 0.6), (0.35, 0.65)),
# ]
# 9/20 reprocess pH < 13
# explst = [
    # ('L:/processes/experiment/eche/20160314.112931.copied-20160314220326441PDT/20160314.112931.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20160721.085158.copied-20160727063023665PDT/20160721.085158.exp', (0.48, 1), (0.5, 1)),
    # ('L:/processes/experiment/eche/20190520.162751.copied-20190520221254058PDT/20190520.162751.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190304.154816.copied-20190304221211247PST/20190304.154816.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20180411.141724.copied-20180411220901744PDT/20180411.141724.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20170301.110115.copied-20170308132955800PST/20170301.110115.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20180411.154249.copied-20180411220901744PDT/20180411.154249.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20180411.152214.copied-20180411220901744PDT/20180411.152214.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190819.120802.copied-20190821054206716PDT/20190819.120802.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190913.110534.copied-20190913220646905PDT/20190913.110534.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190819.120931.copied-20190821054206716PDT/20190819.120931.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20161114.153016.copied-20161114220507745PST/20161114.153016.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20160314.151855.copied-20160314220326441PDT/20160314.151855.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190304.151422.copied-20190304221211247PST/20190304.151422.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20160720.163219.copied-20160727063023665PDT/20160720.163219.exp', (0.48, 1), (0.5, 1)),
    # ('L:/processes/experiment/eche/20170228.142848.copied-20170301220342337PST/20170228.142848.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20170328.101615.copied-20170328220334394PDT/20170328.101615.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190920.225000.done/20190920.225000.exp', (0.48, 1), (0.5, 1)),
    # ('L:/processes/experiment/eche/20190430.140031.copied-20190430220754109PDT/20190430.140031.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190812.142046.copied-20190814002507232PDT/20190812.142046.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190812.140146.copied-20190814002507232PDT/20190812.140146.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20190920.163109.done/20190920.163109.exp', (0.48, 1), (0.5, 1)), 
    # ('L:/processes/experiment/eche/20160308.105918.copied-20160308220226709PST/20160308.105918.exp', (0.48, 0.9), (0.5, 0.9)), 
    # ('L:/processes/experiment/eche/20161114.133636.copied-20161114220507745PST/20161114.133636.exp', (0.48, 0.9), (0.5, 0.9)), 
    # ('L:/processes/experiment/eche/20190520.161823.copied-20190520221254058PDT/20190520.161823.exp', (0.48, 0.9), (0.5, 0.9)), 
    # ('L:/processes/experiment/eche/20170828.165831.copied-20170828220902243PDT/20170828.165831.exp', (0.48, 0.9), (0.5, 0.9)), 
    # ('L:/processes/experiment/eche/20190920.162750.done/20190920.162750.exp', (0.48, 0.9), (0.5, 0.9)), 
    # ('L:/processes/experiment/eche/20160418.172947.copied-20160418220703150PDT/20160418.172947.exp', (0.32, 0.6), (0.35, 0.65)), 
    # ('L:/processes/experiment/eche/20170823.143138.copied-20170823194838230PDT/20170823.143138.exp', (0.32, 0.6), (0.35, 0.65)), 
    # ('L:/processes/experiment/eche/20190814.210551.copied-20190816111512496PDT/20190814.210551.exp', (0.32, 0.6), (0.35, 0.65)), 
    # ('L:/processes/experiment/eche/20190920.163245.done/20190920.163245.exp', (0.32, 0.6), (0.35, 0.65))
    # ]
explst = [
    ('L:/processes/experiment/eche/20190920.234643.done/20190920.234643.exp', (0.48, 0.9), (0.5, 0.9)),
    ('L:/processes/experiment/eche/20190920.235421.done/20190920.235421.exp', (0.48, 1.0), (0.5, 1.0))
]


for exp, lim1, lim2 in explst:
    mainapp = QApplication(sys.argv)
    form = MainMenu(None)
    calcui = form.calcui
    visdataui=form.visdataui
    try:
        calcui.importexp(exppath=exp)
        select_techtype('CP3')
        select_procana_fcn(calcui, '')
        select_ana_fcn(calcui, 'Etaave')
        calcui.analysisclass.params['num_std_dev_outlier'] = 1.5
        calcui.processeditedparams()
        calcui.analyzedata()
        
        select_techtype('CP3')
        select_procana_fcn(calcui, 'FOM_Merge_PlatemapComps')
        calcui.analysisclass.params['select_ana'] = 'ana__1'
        calcui.processeditedparams()
        calcui.analyzedata()
        
        select_techtype('CP3')
        select_procana_fcn(calcui, 'CDEF')
        calcui.analysisclass.params['select_ana'] = 'ana__2'
        calcui.processeditedparams()
        calcui.batch_process_allsubspace()
        
        select_techtype('CP4')
        select_procana_fcn(calcui, '')
        select_ana_fcn(calcui, 'Etaave')
        calcui.analysisclass.params['num_std_dev_outlier'] = 1.5
        calcui.processeditedparams()
        calcui.analyzedata()

        select_techtype('CP4')
        select_procana_fcn(calcui, 'FOM_Merge_PlatemapComps')
        calcui.analysisclass.params['select_ana'] = 'ana__18'
        calcui.processeditedparams()
        calcui.analyzedata()
        
        select_techtype('CP4')
        select_procana_fcn(calcui, 'CDEF')
        calcui.analysisclass.params['select_ana'] = 'ana__19'
        calcui.processeditedparams()
        calcui.batch_process_allsubspace()
        
        anasavefolder = calcui.saveana(
            dontclearyet=True, anatype=anadestchoice, rundone=anasaveextension)
        calcui.viewresult(anasavefolder=anasavefolder, show=False)
        comboind_strlist=[]
        for i in range(1, visdataui.numStdPlots+1):
            visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
            comboind_strlist+=[(i, str(visdataui.stdcsvplotchoiceComboBox.currentText()))]

        batchidialog=saveimagesbatchDialog(visdataui, comboind_strlist)
        batchidialog.plotstyleoverrideCheckBox.setChecked(1)
        inds=numpy.where(numpy.logical_not(numpy.isnan(visdataui.fomplotd['fom'])))[0]
        if len(inds)>0:
            samplestoplot=list(visdataui.fomplotd['sample_no'][inds])
            filterinds=[ind for ind, smp in enumerate(visdataui.fomplotd['sample_no']) if smp in samplestoplot]
            for k in visdataui.fomplotd.keys():
                if isinstance(visdataui.fomplotd[k], numpy.ndarray):
                    visdataui.fomplotd[k]=visdataui.fomplotd[k][filterinds]

        for i in range(1, 35):
            visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
            visdataui.numcompintervalsSpinBox.setValue(10)
            if i<18:
                vmin, vmax = lim1
            else:
                vmin, vmax = lim2
            visdataui.vminmaxLineEdit.setText('%.3f,%.3f' %(vmin, vmax))
            if i == 2 or i == 19:
                continue
            if i==1 or i==18:
                filenamesearchlist=['plate_id']
            else:
                filenamesearchlist=['code__-1']
            filenamesearchlist=[s.strip() for s in filenamesearchlist if (len(s.strip())>0) and s!='&']
            if len(filenamesearchlist)==0:
                filenamesearchlist=None
            else:
                filenamesearchlist=[[sv.strip() for sv in s.split('&') if len(sv.strip())>0] for s in filenamesearchlist if len(s.strip())>0]
            visdataui.plot_preparestandardplot(loadstyleoptions=True)# or logic for ,-delim and and logic within each or block with &-delim
            visdataui.savefigs(save_all_std_bool=True, batchidialog=batchidialog, filenamesearchlist=filenamesearchlist, lastbatchiteration=(i==32))#for std plots all foms will be from same ana__  and prepend str will be filled in automatically
        visdataui.close()
        sleep(0.5)
        calcui.close()
        sleep(0.5)
        mainapp.quit()
        sleep(0.5)
        del visdataui
        del calcui
        del mainapp
    except:
        visdataui.close()
        sleep(0.5)
        calcui.close()
        sleep(0.5)
        mainapp.quit()
        sleep(0.5)
        del visdataui
        del calcui
        del mainapp
