
import sys, os
############
projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))

from ExternalDataImportApp import extimportDialog

from fcns_io import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *



class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.extimportui=extimportDialog(self, title='Create RCP/EXP/ANA for non-HTE instruments')

mainapp=QApplication(sys.argv)
form=MainMenu(None)
#form.show()
#form.setFocus()
#mainapp.exec_()
        
extimportui=form.extimportui



extimportui.ProfileComboBox.setCurrentIndex(2)

#p=r'K:\experiments\xrds\user\SSRLFeb2015\2015Feb\24297_NbMnVO'
#pp=r'K:\experiments\xrds\user\SSRLFeb2015\Processed\24297_NbMnVO'

saveoption=3# use 3 for .done in ssrl folder
extimportui.ExpSaveComboBox.setCurrentIndex(saveoption)#.done in ssrl folder
extimportui.AnaSaveComboBox.setCurrentIndex(saveoption)#.done in ssrl folder

pp_parentdir=r'F:\2017May\Processed_pvd'
pp_parentfn=lambda x: os.path.join(pp_parentdir,x)

p_parentdir=r'F:\2017May\data_pvd'
p_parentfn=lambda x: os.path.join(p_parentdir,x)

dirl = [x for x in os.listdir(pp_parentdir) if os.path.isdir(pp_parentfn(x))]
for dirn in dirl:
    print(dirn)
    p=p_parentfn(dirn)
    pp=pp_parentfn(dirn)
    if os.path.exists(p) and os.path.exists(pp):
        extimportui.importfolder(p=p, p_processed=pp)
        extimportui.createfiles_runprofilefcn()
        extimportui.create_udi(opttionsearchstr_xrd='Process', opttionsearchstr_comps='')#use the qcounts_subbcknd xrd data and the only comps data
        extimportui.savefiles()
#        extimportui.exec_()
#    break
