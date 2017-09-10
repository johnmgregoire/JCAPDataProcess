
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




#XRFS ANA: L:\processes\analysis\xrfs\20170907.125058.done (turns .copied overnight) (use ana__2)

extimportui.ProfileComboBox.setCurrentIndex(2)

#p=r'K:\experiments\xrds\user\SSRLFeb2015\2015Feb\24297_NbMnVO'
#pp=r'K:\experiments\xrds\user\SSRLFeb2015\Processed\24297_NbMnVO'

saveoption=2# use 3 for .done in ssrl folder
extimportui.ExpSaveComboBox.setCurrentIndex(saveoption)#.done in ssrl folder
extimportui.AnaSaveComboBox.setCurrentIndex(saveoption)#.done in ssrl folder

pp_parentdir=r'K:\experiments\xrds\SSRL2017May\27830_CuBiVO\processed'
pp_parentfn=lambda x: os.path.join(pp_parentdir,x)

p_parentdir=r'K:\experiments\xrds\SSRL2017May\27830_CuBiVO\data'
p_parentfn=lambda x: os.path.join(p_parentdir,x)

dirl = [x for x in os.listdir(pp_parentdir) if os.path.isdir(pp_parentfn(x))]
for dirn in dirl:
    print dirn
    p=p_parentfn(dirn)
    pp=pp_parentfn(dirn)
    if os.path.exists(p) and os.path.exists(pp):
        extimportui.importfolder(p=p, p_processed=pp)
        extimportui.createfiles_runprofilefcn(rundoneext='.run')
        extimportui.create_udi(opttionsearchstr_xrd='Process', opttionsearchstr_comps='')#use the qcounts_subbcknd xrd data and the only comps data
        extimportui.savefiles(overwrite=True, rundoneext='.run')
        print 'done with ', dirn
        extimportui.exec_()
#    break

#TODO. read in .run ana and perform merge analysis using standard calcfomapp.
mockcalcfom=calcfom_mock_class()
mockcalcfom.aux_ana_dlist=[]
mockcalcfom.anadict=extimportui.anadict#by reference
mockcalcfom.paramsdict_le_dflt['description']='composition interpolation for ssrl import'
aux_ana_path=r'L:\processes\analysis\xrfs\20170907.125058.copied-20170907221545763PDT\20170907.125058.ana'

auxexpanadict=readana(auxexpanapath, stringvalues=False, erroruifcn=None)
        rp=os.path.split(auxexpanapath)[0]
        dbpath_folds=(ANAFOLDERS_J+ANAFOLDERS_L)
        rp=compareprependpath(dbpath_folds, rp)
        auxexpanadict['auxexpanapath_relative']=rp.replace(chr(92),chr(47))
        auxexpanadict['auxexpanapath']=auxexpanapath
        mockcalcfom.aux_ana_dlist+=[auxexpanadict]
#analysisclass.perform(self.tempanafolder, expdatfolder=expdatfolder, anak=anak, zipclass=self.expzipclass, expfiledict=self.expfiledict, anauserfomd=self.userfomd)
analysisclass=Analysis__FOM_Interp_Merge_Ana()
analysisclass.params={'select_ana': 'ana__1', 'select_fom_keys':'ALL', 'select_aux_keys':'V.K.AtFrac,Cu.K.AtFrac,Bi.L.AtFrac', 'aux_ana_path':aux_ana_path, 'aux_ana_ints':2, 'interp_keys':'platemap_xy', 'fill_value':'extrapolate', 'kind':'linear', 'interp_is_comp':1}
analysisclass.processnewparams(calcFOMDialogclass=mockcalcfom)
analysisclass.perform(self.tempanafolder, anak='ana__4')
