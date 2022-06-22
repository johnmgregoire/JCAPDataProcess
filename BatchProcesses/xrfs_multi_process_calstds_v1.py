import sys, os
from time import sleep
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
    def __init__(self, previousmm, execute=True):  # , TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        # self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.calcui = calcfomDialog(
            self, title='Calculate FOM from EXP', guimode=False)
        # self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data', GUIMODE=False)


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
anasaveextension = '.done'

# providing these paths will skip the generation of the exp/ana
expname = None
expdestchoice = 'xrfs'
anadestchoice = 'xrfs'

# anastr = '20161202.105650.copied-20161204222558040PST/20161202.105650.ana 20160518.174844.copied-20160812063256847PDT/20160518.174844.ana 20160512.121215.copied-20160812063256847PDT/20160512.121215.ana 20160517.162553.copied-20160812063256847PDT/20160517.162553.ana 20160520.162518.copied-20190301232320536PST/20160520.162518.ana 20160525.172107.copied-20160812063256847PDT/20160525.172107.ana 20170105.132219.copied-20170110221450943PST/20170105.132219.ana 20160309.154334.copied-20160812063256847PDT/20160309.154334.ana 20160218.152153.copied-20160812063256847PDT/20160218.152153.ana 20160308.103440.copied-20160812063256847PDT/20160308.103440.ana 20160318.171453.copied-20160812063256847PDT/20160318.171453.ana 20160321.152759.copied-20160812063256847PDT/20160321.152759.ana 20160422.104726.copied-20160812063256847PDT/20160422.104726.ana 20160309.113853.copied-20160812063256847PDT/20160309.113853.ana 20160309.135909.copied-20160812063256847PDT/20160309.135909.ana 20170530.114134.copied-20170601153808215PDT/20170530.114134.ana 20190515.150352.copied-20190516222950372PDT/20190515.150352.ana 20160318.154742.copied-20160812063256847PDT/20160318.154742.ana 20160318.142517.copied-20160812063256847PDT/20160318.142517.ana 20160218.164818.copied-20160812063256847PDT/20160218.164818.ana 20160218.161118.copied-20160812063256847PDT/20160218.161118.ana 20160308.115213.copied-20160812063256847PDT/20160308.115213.ana 20160318.133459.copied-20160812063256847PDT/20160318.133459.ana 20160317.141740.copied-20160812063256847PDT/20160317.141740.ana 20160418.160003.copied-20160812063256847PDT/20160418.160003.ana 20160321.105816.copied-20160812063256847PDT/20160321.105816.ana 20160404.104540.copied-20160812063256847PDT/20160404.104540.ana 20160404.140019.copied-20160812063256847PDT/20160404.140019.ana 20160321.124250.copied-20160812063256847PDT/20160321.124250.ana 20160404.114609.copied-20160812063256847PDT/20160404.114609.ana 20161128.153941.copied-20161128221531077PST/20161128.153941.ana 20161214.111951.copied-20161215224721049PST/20161214.111951.ana 20161202.102726.copied-20161212132802206PST/20161202.102726.ana 20190402.144034.copied-20190402221237117PDT/20190402.144034.ana 20180706.094036.copied-20190109230825492PST/20180706.094036.ana 20190329.101153.copied-20190401221721626PDT/20190329.101153.ana 20190326.082112.copied-20190328230304623PDT/20190326.082112.ana 20190325.164015.copied-20190328230304623PDT/20190325.164015.ana 20190328.124946.copied-20190328230304623PDT/20190328.124946.ana 20190402.222324.copied-20190403220958498PDT/20190402.222324.ana'
# runstr = '20161202.105650 20160518.174844 20160512.121215 20160517.162553 20160520.162518 20160525.172107 20170105.132219 20160309.154334 20160218.152153 20160308.103440 20160318.171453 20160321.152759 20160422.104726 20160309.113853 20160309.135909 20170530.114134 20190515.150352 20160318.154742 20160318.142517 20160218.164818 20160218.161118 20160308.115213 20160318.133459 20160317.141740 20160418.160003 20160321.105816 20160404.104540 20160404.140019 20160321.124250 20160404.114609 20161128.153941 20161214.111951 20161202.102726 20190402.144034 20180706.094036 20190329.101153 20190326.082112 20190325.164015 20190328.124946 20190402.222324'

# anastr = '20190821.153618.copied-20190821221442147PDT/20190821.153618.ana 20190821.133036.copied-20190821221442147PDT/20190821.133036.ana 20190821.162710.copied-20190821221442147PDT/20190821.162710.ana'
# runstr = '20190821.153618 20190821.133036 20190821.162710'

# anastr = '20151211.154550.copied-20190831003629668PDT/20151211.154550.ana xrfs/20190830.152517.copied-20190903221645644PDT/20190830.152517.ana 20190830.131725.copied-20190831003629668PDT/20190830.131725.ana'
# runstr = '20151211.154550 20190830.152517 20190830.131725'

anastr = '20150403.163811.copied-20190830113003948PDT/20150403.163811.ana'
runstr = '20150403.163811'

analst = anastr.split()
runlst = runstr.split()

anaps = ['L:/processes/analysis/xrfs/%s' %(x) for x in analst]
anaps

callibs=os.listdir('K:/experiments/xrfs/user/calibration_libraries')
callibs = [x for x in callibs if '2000-vacu-3.2' in x and 'hiTa' not in x]
tss = [int(x.split('__')[1].split('-')[0]) for x in callibs]
runtss = [float(x) for x in runlst]

len([x for x in runtss if x < min(tss)])

calinds = [0 if x < min(tss) else max([i for i,v in enumerate(tss) if x > v]) for x in runtss]
callst = [callibs[i] for i in calinds]
callst

for ana, cal in zip(anaps, callst):
    try:
        mainapp = QApplication(sys.argv)
        form = MainMenu(None)
        calcui = form.calcui
        calcui.importana(p=ana)
        select_procana_fcn(calcui, 'Process_XRFS_Stds')
        calcui.analysisclass.params['nmol_CPS_lib_file'] = cal
        calcui.analysisclass.params['nmol_CPS_list'] = ''
        calcui.analysisclass.params['select_ana'] = 'ana__1'
        calcui.analysisclass.params['transition_list_for_stds'] = 'ALL'
        calcui.analysisclass.params['transition_list_for_comps'] = 'ALL'
        calcui.analysisclass.params['transition_ratio_list'] = 'NONE'
        calcui.analysisclass.params['bcknd_CPS_sample_nos'] = 'nonpositive'
        calcui.analysisclass.params['bcknd_CPS_by_trans'] = 'None'
        calcui.processeditedparams()
        calcui.analyzedata()

        anasavefolder = calcui.saveana(
            dontclearyet=False, anatype=anadestchoice, rundone=anasaveextension)
        calcui.close()
        sleep(0.5)
        mainapp.quit()
        sleep(0.5)
        del calcui
        del mainapp
    except:
        print(('Error processing %s' %(ana)))
        calcui.close()
        sleep(0.5)
        mainapp.quit()
        sleep(0.5)
        del calcui
        del mainapp

# openwindow()
