import sys, os
import time

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
from VisualizeBatchFcns import batch_plotuvisrefs
from DBPaths import *


if len(sys.argv) == 1:
    exec(compile(open("batch.py", "rb").read(), "batch.py", 'exec'))
else:
    exec(compile(open(sys.argv[1], "rb").read(), sys.argv[1], 'exec'))

loglines=[]
batchfilepath=os.path.join(batchfolder,batchinput_fn)
batch_stdout_path=batchfilepath.rpartition('.')[0]+'.out'
logfilepath=batchfilepath.rpartition('.')[0]+'.log'
runsrcfolder=tryprependpath(RUNFOLDERS, '', testfile=False, testdir=True).rstrip(os.sep)

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', guimode=False)
        self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data', GUIMODE=False)

    def visui_exec(self, show=True):
        if self.visdataui is None:
            self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data', GUIMODE=False)
            #use GUIMODE=True to see any messages or dialog boxes
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
expui=form.expui
calcui=form.calcui
visdataui=form.visdataui


def getbatchlinepath(linestr, key='TR_path'):
    return linestr.partition(key)[2].strip(':').strip().partition(';')[0].strip()


def updatelog(i, s, lines):
    s=s.strip()
    if len(s)==0:
        return

    if len(lines[i].strip())>0:
        lst=[lines[i].strip().split('\n')[0].split('\r')[0]]
    else:
        lst=[]
    lst+=[s]
    lines[i]=';'.join(lst)
    with open(logfilepath, mode='w') as f:
        f.write('\n'.join(lines))



def batch_getplotcompbool(fn):       
    pT=os.path.join(runsrcfolder, fn)
    serialno=pT.rpartition('_')[2]
    plateidstr=serialno[:-1]
    with open(os.path.join(projectroot,'BatchProcesses','uvis_quatcomp_maps.txt'),'r') as uv_mapfs:
         plotcompbool=1 if getscreeningmapid_plateidstr(plateidstr) in uv_mapfs.readline().split(',') else 0
    return plotcompbool

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
            raise
    with open(p, mode='r') as f:
        lines=f.readlines()
    infofiled=filedict_lines(lines)

    methods=[v3 for k, v in infofiled.items() if k.startswith('prints') for k2, v2 in v.items() if k2.startswith('prints') for k3, v3 in v2.items() if k3.startswith('method')]
    return '', ('PVD' in methods, )


def batch_exp(fn, expui=expui):
    expui.removeruns()
    pT=os.path.join(runsrcfolder, fn)
    pR=os.path.join(runsrcfolder, fn.replace('_T-', '_R-'))

    if not os.path.isdir(pT):
        if skiponerror:
            return 'ERROR - cannot find file %s' %pT, False
        else:
            raise
    if not os.path.isdir(pR):
        if skiponerror:
            return 'ERROR - cannot find file %s' %pR, False
        else:
            raise

    for p in [pT, pR]:
        for zfn in os.listdir(p):
            if not zfn.endswith('.zip'):
                continue
            expui.importruns_folder(folderp=os.path.join(p, zfn))
    expui.batchuvissingleplate_norefdata()

    if (not 'experiment_type' in list(expui.expfiledict.keys())) or len(expui.expfilestr)==0 or not 'exp_version' in expui.expfilestr:
        if skiponerror:
            return 'ERROR - betchexp failed for %s' %pT, False
        else:
            raise
    saveexpfiledict, exppath=expui.saveexp(exptype=expdestchoice, rundone='.done')
    return 'exp_path:%s' %os.path.dirname(exppath), (saveexpfiledict, exppath)


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


def run_batch():
    with open(batchfilepath, mode='r') as f:
        batchlines=f.readlines()
        loglines=[fn.rstrip('\n').rstrip('\r') for fn in batchlines]
        for batchcount, batchline in enumerate(batchlines):
            if batchline.startswith('T'):
                batchlinekey='TR_path'
                analabels=['TR_UVVIS','BG']
                techs=['T_UVVIS','R_UVVIS']
            else:
                batchlinekey='DR_path'
                analabels=['DR_UVVIS', 'BG']
                techs=['DR_UVVIS']
            if len(batchline.strip('\n').strip('\r'))!=0:
                try:
                    print('batchline:'+batchline)
                    expbool=False
                    if forceexp or not 'exp_path' in batchline:
                        rawfn=getbatchlinepath(batchline, key=batchlinekey).lstrip(os.sep)
                        logstr, tupbool=batch_exp(rawfn)
                        if not tupbool:#error so False passed or empty tuple
                            continue
                        expfiledict, exppath=tupbool
                        updatelog(batchcount, logstr, loglines)
                        expbool=True
                    
                    elif getpvdbool:
                        rawfn=getbatchlinepath(batchline, key=batchlinekey)

                    if getpvdbool:
                        logstr, tupbool=batch_pvdbool(rawfn)
                        updatelog(batchcount, logstr, loglines)
                        if not tupbool:#error so False passed or empty tuple
                            continue
                        pvdbool=tupbool[0] # not used as of now, plotcompbool is currently a superceding variable, but may use for future pvd specific plots
               
                    plotcompbool=batch_getplotcompbool(rawfn)
                    visdataui.inkjetconcentrationadjustment=True if plotcompbool else False
                    
                    
                    anabool=False
                    if forceana or not 'ana_path' in batchline:
                        if expbool:
                            calcui.importexp(expfiledict=expfiledict, exppath=exppath)
                            for runk, rund in calcui.expfiledict.items():#copy over any platemap info
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
                        for analabel in analabels:#TODO: for BG run on the ana
                            if not select_ana_fcn(calcui, analabel):
                                if skiponerror:
                                    updatelog(batchcount, 'ERROR-Analysis %s not available' %analabel, loglines)
                                    continue
                                else:
                                    raise
                            calcuierror=calcui.analyzedata()#return False if ok otherwise stringh error message
                            if calcuierror:
                                if skiponerror:
                                    updatelog(batchcount, 'ERROR-%s' %calcuierror, loglines)
                                    continue
                                else:
                                    raise
                        anasavefolder=calcui.saveana(dontclearyet=True, anatype=anadestchoice, rundone='.run')
                        calcui.viewresult(anasavefolder=anasavefolder, show=False)
                        updatelog(batchcount, 'ana_path:%s' %anasavefolder, loglines)
                        anabool=True

                    if anabool or 'images saved' not in batchline:
                        if not anabool and 'ana_path' in batchline:#didn't calculate ana here but ened to load it
                            anapath=getbatchlinepath(batchline, key='ana_path')
                            visdataui.importana(p=anapath)

                        if visdataui.numStdPlots==0:
                            if skiponerror:
                                updatelog(batchcount, 'ERROR- No standard plots in vis', loglines)
                                continue
                            else:
                                raise

                        comboind_strlist=[]
                        for i in range(1, visdataui.numStdPlots+1):
                            visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
                            comboind_strlist+=[(i, str(visdataui.stdcsvplotchoiceComboBox.currentText()))]

                        for tech in techs:
                            batch_plotuvisrefs(visdataui, tech=tech)
                            idialog=visdataui.savefigs(save_all_std_bool=False, batchidialog=None, lastbatchiteration=False, filenamesearchlist=[['xy']], justreturndialog=True, prependstr=tech)
                            idialog.doneCheckBox.setChecked(False)
                            idialog.ExitRoutine()
                            if idialog.newanapath:
                                visdataui.importana(p=idialog.newanapath)
                        batchidialog=saveimagesbatchDialog(None, comboind_strlist)

                        fnsearchle='plate_id__'
                        if plotcompbool:#if PVD bool then don't save composition plots
                            fnsearchle+=',code__'
                        batchidialog.filenamesearchLineEdit.setText(fnsearchle)
                        batchidialog.ExitRoutine()
                        visdataui.vminmaxLineEdit.setText('')
                        batchidialog.plotstyleoverrideCheckBox.setChecked(False)
                        visdataui.save_all_std_plots(batchidialog=batchidialog)

                        #save version of FOM plots with 1.6 to 2.6 eV range
                        visdataui.colormapLineEdit.setText('jet_r')
                        vmin=1.8;vmax=2.8
                        visdataui.vminmaxLineEdit.setText(str(vmin)+','+str(vmax))
                        visdataui.belowrangecolLineEdit.setText('(1,0.5,0.5)')
                        visdataui.aboverangecolLineEdit.setText('(0.3,0,0.5)')
                        batchidialog.plotstyleoverrideCheckBox.setChecked(True)
                        batchidialog.prependfilenameLineEdit.setText(str(vmin)+'to'+str(vmax))
                        fnsearchle='plate_id__&bg_repr'
                        if plotcompbool:#if PVD bool then don't save composition plots
                            fnsearchle+=',code__&bg_repr'
                        batchidialog.filenamesearchLineEdit.setText(fnsearchle)
                        batchidialog.doneCheckBox.setChecked(False)
                        batchidialog.ExitRoutine()
                        visdataui.save_all_std_plots(batchidialog=batchidialog)
                        updatelog(batchcount, 'images saved', loglines)
                except:
                    if skiponerror and not batchmode:
                        continue
                    else:
                        raise


while True:
    if batchmode:
        batchfiles = os.listdir(batchfolder)
        todofiles = [f for f in batchfiles if f.endswith(".todo")]
        if len(todofiles) > 0:
 #               todofile = os.path.join(batchfolder,todofiles[0])
            todofile = os.path.join(batchfolder,todofiles[0])
            try:
                print(("Processing " + todofile))
                runfile = os.path.join(batchfolder,todofile[0:-5] + ".run")
                os.rename(todofile,runfile)
                batchfilepath = runfile
                batch_stdout_path = batchfilepath.rpartition('.')[0]+'.out'
                logfilepath = batchfilepath.rpartition('.')[0]+'.log'
                runsrcfolder = tryprependpath(RUNFOLDERS, '', testfile=False, testdir=True).rstrip(os.sep)
                run_batch()
                donefile = os.path.join(batchfolder,todofile[0:-5] + ".done")
                os.rename(runfile,donefile)
                logfile = os.path.join(batchfolder,todofile[0:-5] + ".log")
                if os.path.isfile(logfile): os.rename(logfilepath,logfile)
                print(("Finished processing " + donefile))
                print ("Pausing for 1 minute before checking the next run")
            except:
                print(("Failed processing " + todofile))
                failedfile = os.path.join(batchfolder,todofile[0:-5] + ".failed")
                os.rename(runfile,failedfile)
                print ("Pausing for 1 minute before checking the next run")
		raise
        time.sleep(60)
    else:
        run_batch()
        break

