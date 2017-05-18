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
from fcns_io import *
from SaveImagesApp import *
from DBPaths import *

#batchfolder=r'K:\users\sksuram\uvis_batchtests'
#batchinput_fn='15589.txt'
expname=r'xrfs\20170518.122412'
anadestchoice=r'temp'#r'xrfs'
saveextension='run'

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


exppath=buildexppath(expname)
print exppath

    
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


calcui.importexp(exppath=exppath)



runkeys=sort_dict_keys_by_counter(calcui.expfiledict, keystartswith='run__')
#bruns=[k for k in runkeys if calcui.expfiledict[k]['run_use']=='background']
datarunkeys=[k for k in runkeys if calcui.expfiledict[k]['run_use']=='data']

ellist=getelements_plateidstr(str(calcui.expfiledict[datarunkeys[0]]['parameters']['plate_id']))

calcui.autoplotCheckBox.setChecked(False)
for count, datause in enumerate(['background', 'data']):
    i=calcui.uselist.index(datause)
    calcui.ExpRunUseComboBox.setCurrentIndex(i)
    calcui.fillruncheckboxes()

    qlist=calcui.TechTypeButtonGroup.buttons()
    typetechfound=False
    for button in qlist:
        if str(button.text()).strip()=='XRFS,batch_summary_files':
            button.setChecked(True)
            typetechfound=True
            break
    calcui.fillanalysistypes(calcui.TechTypeButtonGroup.checkedButton())
    if not typetechfound or not select_ana_fcn(calcui, 'XRFS_EDAX'):
        calcui.exec_();raiseerror
    calcuierror=calcui.analyzedata()#ana__1 and then ana__2
    if calcuierror:
        calcui.exec_();raiseerror
    if count==0:
        #no analysis performed here, just getting info
        if not select_procana_fcn(calcui, 'Process_XRFS_Stds'):
            calcui.exec_();raiseerror
        updateanalysisparams(calcui, calcui.analysisclass.dfltparams)#this includes using ana__1  which was just created above and will inlcude all transitions so we can find the transititons that match the ellist

        elcpskeylist=calcui.fomdlist[0].keys()
        trlistforquant=[]
        bckndcps=[]
        for el in ellist:
            kl=[k for k in elcpskeylist if k.startswith(el+'.') and k.endswith('.CPS') and (k.rpartition('.')[0] in calcui.analysisclass.xrfs_stds_dict.keys())]
            if len(kl)==1:#could conceivably have more than 1 transntion be quantified and in stds but not handling that now
                trlistforquant+=[kl[0].rpartition('.')[0]]
                bckndcps+=[numpy.mean([d[kl[0]] for d in calcui.fomdlist])]#average over all samples in this "background" ana
        #trlistforquant is now in order of the platemap elements but only including the elements with CPS data that are also in stds database

if not select_procana_fcn(calcui, 'Process_XRFS_Stds'):
    calcui.exec_();raiseerror

trliststr=','.join(trlistforquant)
bckndcpsstr=','.join(['%.3e' %v for v in bckndcps])
updateanalysisparams(calcui, {'select_ana': 'ana__2', 'transition_list_for_stds':trliststr, 'transition_list_for_comps':trliststr,  'bcknd_CPS_by_trans':bckndcpsstr})#nmol_CPS_list is comma-delim values, to override library, for other params user can type substrings, e.g. .csv to find any library file or Fe to find Fe.K, rations typed as comma-delim of form "Fe:La.L"
#calcui.exec_();raiseerror
calcuierror=calcui.analyzedata()#ana__3
if calcuierror:
    calcui.exec_();raiseerror

if not select_procana_fcn(calcui, 'FOM_Merge_PlatemapComps'):
    calcui.exec_();raiseerror
updateanalysisparams(calcui, {'select_ana': 'ana__3'})
calcuierror=calcui.analyzedata()#ana__4
if calcuierror:
    calcui.exec_();raiseerror

runintliststr=','.join([`ri` for ri in sorted(list(set([d['runint'] for d in calcui.fomdlist])))])

Atrliststr=','.join([s.partition('.')[0]+'.PM.AtFrac' for s in trlistforquant])
Btrliststr=','.join([s+'.AtFrac' for s in trlistforquant])

print Atrliststr, Btrliststr, runintliststr
if not select_procana_fcn(calcui, 'Process_B_vs_A_ByRun'):
    calcui.exec_();raiseerror

#updateanalysisparams(calcui, {'select_ana': 'ana__4'})    
#updateanalysisparams(calcui, calcui.analysisclass.dfltparams)
calcui.analysisclass.params.update(calcui.analysisclass.dfltparams)
#updateanalysisparams(calcui, {'select_ana': 'ana__4'})
print calcui.analysisclass.params
updateanalysisparams(calcui, {'select_ana': 'ana__4', \
'fom_keys_B':Btrliststr, 'fom_keys_A':Atrliststr, 'runints_B':runintliststr, 'runints_A':runintliststr})
print calcui.analysisclass.params
updateanalysisparams(calcui, {\
'keys_to_keep':'.CPS,.PM.AtFrac', 'method':'B_comp_dist_wrt_A', 'relative_key_append':'_CompDiff', 'AandBoffset':'0.'\
})
print calcui.analysisclass.params
calcuierror=calcui.analyzedata()#ana__5
if calcuierror:
    calcui.exec_();raiseerror
    

anasavefolder=calcui.saveana(dontclearyet=True, anatype=anadestchoice, rundone='.'+saveextension)

calcui.show()


                #calcui.viewresult(anasavefolder=anasavefolder, show=False)
                

            
#            if anabool or 'images saved' not in batchline:
#                if not anabool and 'ana_path' in batchline:#didn't calculate ana here but ened to load it
#                    anapath=getbatchlinepath(batchline, key='ana_path')
#                    visdataui.importana(p=anapath)
#                
#                if visdataui.numStdPlots==0:
#                    if skiponerror:
#                        updatelog(batchcount, 'ERROR- No standard plots in vis')
#                        continue
#                    else:
#                        calcui.exec_();raiseerror
#                    
#                comboind_strlist=[]
#                for i in range(1, visdataui.numStdPlots+1):
#                    visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
#                    comboind_strlist+=[(i, str(visdataui.stdcsvplotchoiceComboBox.currentText()))]
#            
#                for tech in ['DR_UVVIS']:
#                    batch_plotuvisrefs(visdataui, tech=tech)
#                    idialog=visdataui.savefigs(save_all_std_bool=False, batchidialog=None, lastbatchiteration=False, filenamesearchlist=[['xy']], justreturndialog=True, prependstr=tech)
#                    idialog.doneCheckBox.setChecked(False)
#                    idialog.ExitRoutine()
#                    if idialog.newanapath:
#                        visdataui.importana(p=idialog.newanapath)
#                batchidialog=saveimagesbatchDialog(None, comboind_strlist)
#                
#                fnsearchle='plate_id__'
#                if not pvdbool:#if PVD bool then don't save composition plots
#                    fnsearchle+=',code__'
#                batchidialog.filenamesearchLineEdit.setText(fnsearchle)
#                batchidialog.ExitRoutine()
#                visdataui.vminmaxLineEdit.setText('')        
#                batchidialog.plotstyleoverrideCheckBox.setChecked(False)
#                visdataui.save_all_std_plots(batchidialog=batchidialog)
#                
#                #save version of FOM plots with 1.6 to 2.6 eV range
#                visdataui.colormapLineEdit.setText('jet_r')
#                vmin=1.8;vmax=2.8
#                visdataui.vminmaxLineEdit.setText(str(vmin)+','+str(vmax))
#                visdataui.belowrangecolLineEdit.setText('(1,0.5,0.5)')
#                visdataui.aboverangecolLineEdit.setText('(0.3,0,0.5)')
#                batchidialog.plotstyleoverrideCheckBox.setChecked(True)
#                batchidialog.prependfilenameLineEdit.setText(str(vmin)+'to'+str(vmax))
#                fnsearchle='plate_id__&bg_repr'
#                if not pvdbool:#if PVD bool then don't save composition plots
#                    fnsearchle+=',code__&bg_repr'
#                batchidialog.filenamesearchLineEdit.setText(fnsearchle)
#                batchidialog.doneCheckBox.setChecked(False)
#                batchidialog.ExitRoutine()
#                visdataui.save_all_std_plots(batchidialog=batchidialog)
#                updatelog(batchcount, 'images saved')
##        except:
##            if skiponerror:
##                continue
##            else:
##                calcui.exec_();raiseerror
#        
