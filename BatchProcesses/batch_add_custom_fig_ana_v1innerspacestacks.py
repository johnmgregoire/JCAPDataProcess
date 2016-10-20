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


#
ananames='20160802.211016.run,20160803.030404.run,20160803.034223.run,20160902.194122.run,20160803.042224.run,20160923.153723.run,20160912.125625.run,20160803.113046.run,20160923.151003.run,20160803.124020.run,20160803.050406.run,20160902.203104.run,20160906.161617.run,20160802.180002.run,20160912.133819.run,20160712.121351.run,20160802.184102.run,20160715.174914.run,20160923.160636.run,20160902.230552.run,20160906.161617.run,20160912.141405.run,20160923.161009.run'
compinstrs='5,5,5,5,5,5,5,5,5,5,5,5,10,5,5,10,5,10,10,5,10,5,5'

#20160803.050406.run incomplete
#'20160802.211016.run,20160803.030404.run,20160803.034223.run,20160803.042224.run,20160803.113046.run,20160803.124020.run,20160803.050406.run,20160802.180002.run,20160712.121350.run,20160802.184102.run,20160715.174914.run'.split(',')

#action='COPY'
action='SAVEFIGS'

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        #self.expui=expDialog(self, title='Create/Edit an Experiment')
        #self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False)
        self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')

mainapp=QApplication(sys.argv)
form=MainMenu(None)
#form.show()
#form.setFocus()
#mainapp.exec_()
        
#expui=form.expui
#calcui=form.calcui
visdataui=form.visdataui


anadestchoice=r'temp'

for anacount, (anafold, compintstr) in enumerate(zip(ananames.split(','), compinstrs.split(','))):
    if anacount!=12:
        continue
    print anafold
    foldp=os.path.join(r'K:\processes\analysis\temp', anafold)
    if action=='COPY':
        copyfolder_1level(foldp.replace('temp', 'uvis'), foldp)
        continue
    
    if not action=='SAVEFIGS':
        continue
    fn=os.path.join(foldp, anafold.replace('.run', '.ana'))
    
        
    visdataui.importana(p=fn)
    
    plotops=[\
          'stack1.75to2.25_;DA_bg_0;jet_r;(0.,0.,0.);(0.5,0.5,0.5);1.75;2.25',  \
          'stack1.6to2.6_;DA_bg_0;jet_r;(0.,0.,0.);(0.5,0.5,0.5);1.6;2.6',  \
          'stack1.75to2.25_;DA_bg_repr;jet_r;(0.,0.,0.);(0.5,0.5,0.5);1.75;2.25',  \
          'stack1.6to2.6_;DA_bg_repr;jet_r;(0.,0.,0.);(0.5,0.5,0.5);1.6;2.6',  \
          'stack_;DA_bgslope_repr;jet_r;(0.,0.,0.);(0.5,0.5,0.5);;',  \
          'stack0to2_;DA_bgslope_repr;jet_r;(0.,0.,0.);(0.5,0.5,0.5);0;2', \
          ]
    for plotcount, optstr in enumerate(plotops):
        prependlabel, fomname, cm, bcol, acol, vmin, vmax=optstr.split(';')
        visdataui.CompPlotTypeComboBox.setCurrentIndex(6 if compintstr=='5' else 5)
        visdataui.compplotsizeLineEdit.setText('18' if compintstr=='5' else '80')
        for i in range(1, int(visdataui.fomplotchoiceComboBox.count())):              
            matchbool=str(visdataui.fomplotchoiceComboBox.itemText(i))==fomname
            if matchbool:
                visdataui.fomplotchoiceComboBox.setCurrentIndex(i)
                break
        if not matchbool:
            print 'skipping ', fomname
            continue
        visdataui.colormapLineEdit.setText(cm)
        visdataui.vminmaxLineEdit.setText((vmin+','+vmax) if (len(vmin)*len(vmax))>0 else '')
        visdataui.belowrangecolLineEdit.setText(bcol)
        visdataui.aboverangecolLineEdit.setText(acol)
        visdataui.filterandplotfomdata()
        savefigsdialog=visdataui.savefigs(save_all_std_bool=False, batchidialog=None, lastbatchiteration=False, filenamesearchlist=[['code__0']], justreturndialog=True, prependstr=prependlabel)
        savefigsdialog.doneCheckBox.setChecked(plotcount==(len(plotops)-1))
        if 0:
            visdataui.show()
            savefigsdialog.exec_()
        else:
            savefigsdialog.ExitRoutine()
