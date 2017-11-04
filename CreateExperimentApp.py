#cd C:\Python27\Lib\site-packages\PyQt4
#pyuic4 -x C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\QtDesign\CreateExpForm.ui -o C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\CreateExpForm.py
#import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#try:
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#except ImportError:
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure
#import numpy.ma as ma
#import matplotlib.colors as colors
#import matplotlib.cm as cm
#import matplotlib.mlab as mlab
#import pylab
#import pickle
projectpath=os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath,'QtForms'))
sys.path.append(os.path.join(projectpath,'AuxPrograms'))
sys.path.append(os.path.join(projectpath,'OtherApps'))

from fcns_math import *
from fcns_io import *
from fcns_ui import *
from CreateExpForm import Ui_CreateExpDialog
from SaveButtonForm import Ui_SaveOptionsDialog
from RunsFromInfoApp import runsfrominfoDialog
from SearchFolderApp import *
from DBPaths import *


#from matplotlib.ticker import FuncFormatter
#from matplotlib.ticker import ScalarFormatter

matplotlib.rcParams['backend.qt4'] = 'PyQt4'


class SaveOptionsDialog(QDialog, Ui_SaveOptionsDialog):
    def __init__(self, parent, dflt):
        super(SaveOptionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.dfltButton.setText(dflt)
        button_fcn=[\
        (self.dfltButton, self.dflt), \
        (self.tempButton, self.temp), \
        (self.browseButton, self.browse), \
        (self.cancelButton, self.cancel), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        self.choice=dflt
    def dflt(self):
        self.close()
    def temp(self):
        self.choice='temp'
        self.close()
    def browse(self):
        self.choice='browse'
        self.close()
    def cancel(self):
        self.choice=''
        self.close()
        
class expDialog(QDialog, Ui_CreateExpDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(expDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        
        self.RunTreeWidgetFcns=treeclass_dlist(self.RunTreeWidget, key_toplevel='rcp_file', key_nestedfill='rcptuplist')
        self.ExpTreeWidgetFcns=treeclass_dlist(self.ExpTreeWidget, key_toplevel='rcp_file', key_nestedfill='rcptuplist')
        QObject.connect(self.RunTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.editrunparams)
        QObject.connect(self.ExpTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.editexpparams)
        QObject.connect(self.UserFOMLineEdit,SIGNAL("editingFinished()"),self.updateuserfomd)
        
        button_fcn=[\
        (self.AddMeasPushButton, self.editexp_addmeasurement), \
        (self.FilterMeasPushButton, self.editexp_filtercriteria), \
        (self.ImportRunFolderPushButton, self.importruns_folder), \
        (self.ImportRunsPushButton, self.importruns), \
        (self.ImportRunInfoPushButton, self.importruns_info), \
        (self.SearchRunsPushButton, self.searchforruns), \
        (self.RemoveRunsPushButton, self.removeruns), \
        (self.ImportExpParamsPushButton, self.importexpparamsfile), \
        (self.ImportExpPushButton, self.importexpfile), \
        (self.ClearExpPushButton, self.clearexp), \
        (self.SaveExpPushButton, self.saveexp), \
        (self.SaveExpGoAnaPushButton, self.saveexpgoana), \
        (self.SaveExpGoVisPushButton, self.saveexpgovis), \
        (self.BatchPushButton, self.runbatchprocess), \
        (self.RaiseErrorPushButton, self.raiseerror), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        #        (self.EditParamsPushButton, self.editrunparams), \
        #(self.EditExpParamsPushButton, self.editexpparams), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        
        
        self.batchprocesses=[self.batchuvissingleplate_norefdata, self.batchuvissingleplate, self.batchechedark, self.batchechewavelengths, self.batchxrfs]
        batchdesc=['Filter uvis into data, ref_light, ref_dark', 'Filter uvis into data including refs, ref_light, ref_dark', 'Filter _DARK eche spectra as ref_dark', \
         'Add eche runs by wavelength label', 'Process xrfs']
        for i, l in enumerate(batchdesc):
            self.BatchComboBox.insertItem(i, l)
        #These are the filter criteria controls
        
        self.techtypetreefcns=treeclass_techtype(self.TechTypeTreeWidget)
        
        self.platemapEqualLessMore_combobox_spinbox=[\
        (self.PlateAttrEqualComboBox, self.PlateAttrEqualSpinBox), \
        (self.PlateAttrLessComboBox, self.PlateAttrLessSpinBox), \
        (self.PlateAttrMoreComboBox, self.PlateAttrMoreSpinBox), \
        ]
        
        self.expparamsdict_le_dflt=dict([\
         ('access', [self.AccessLineEdit, 'hte']), \
         ('name', [self.ExpNameLineEdit, 'temp_eche_name']), \
         ('experiment_type', [self.ExpTypeLineEdit, 'eche']), \
         ('created_by', [self.UserNameLineEdit, 'eche']), \
         ('description', [self.ExpDescLineEdit, 'null']), \
        ])
        
        self.defaultrcppath=tryprependpath(RUNFOLDERS, '')
        self.removeruns()
        self.clearexp()
        #self.expfilelist=[]
        #self.TechInFilesComboBox, self.FileInFilesComboBox
        #self.FileSearchLineEdit
        self.savebinaryCheckBox.setChecked(False)
        self.batchmode=False
        self.updateuserfomd(clear=True)
        self.run_foms_fcn=None#framework setup but not tested and 20160608 not used. run_foms_fcn(rcpdict_temp) takes the rcpdict from a run block and returns a dictionsary ofr run_fom keys with string values that will be included as a run_foms block in each run__ block in the exp
        
    def raiseerror(self):
        raiseerror
        
    def updateuserfomd(self, clear=False, batchkeys=None):
        if clear:
            self.userfomd={}
            self.UserFOMLineEdit.setText('')
            self.text_UserFOMLineEdit=''
            self.RunTypeLineEdit.setText(str(self.RunTypeLineEdit.text()).partition('__')[0])
            return
        if self.batchmode and batchkeys is None:
            return    
        s=str(self.UserFOMLineEdit.text())
        if self.text_UserFOMLineEdit==s:#"duplicate" signals being emitted so ignore them 
            return
        self.text_UserFOMLineEdit=s

        vals=s.split(',')
        if batchkeys is None:
            keys=['user_fom_run__%d' %i for i, v in enumerate(vals)]
            ans=[]
            count=0
            while ans!=keys:
                inputs=[('key for %s' %v, str, k) for k, v in zip(keys, vals)]
                ans=userinputcaller(self, inputs=inputs, title='Enter user FOM keys',  cancelallowed=True)
                if ans is None:
                    return
                keys=[filterchars(k) for k in ans]

                count+=1
        else:
            keys=batchkeys
        vals=[v.strip() for v in vals]#no numericalconversion here
        self.userfomd=dict([(k, v) for k, v in zip(keys, vals)])
        if len(vals)>0:
            self.RunTypeLineEdit.setText(str(self.RunTypeLineEdit.text()).partition('__')[0]+'__'+','.join(vals))

    def runbatchprocess(self):
        self.batchprocesses[self.BatchComboBox.currentIndex()]()
    def batchuvissingleplate(self):#uses cb filter for sample_no>0 but the only difference from other batch is to note use ref data, which has sample_no 0 so this is obselte until we see how to add sample_no that are not 0
        
        self.ExpTypeLineEdit.setText('uvis')
        self.UserNameLineEdit.setText('uvis')
        self.savebinaryCheckBox.setChecked(False)
#        cb=self.PlateAttrMoreComboBox
#        for i in range(int(cb.count())):
#            if 'Sample' in str(cb.itemText(i)):
#                cb.setCurrentIndex(i)
#                break
        self.RunTypeLineEdit.setText('data')
        
        self.FileNotStartLineEdit.setText('')
        
        self.FileStartLineEdit.setText('')
        self.editexp_addmeasurement()
        #cb.setCurrentIndex(0)
        
        self.RunTypeLineEdit.setText('ref_dark')
        self.FileStartLineEdit.setText('0_-1_')
        self.editexp_addmeasurement()
        
        self.RunTypeLineEdit.setText('ref_light')
        self.FileStartLineEdit.setText('0_1_')
        self.editexp_addmeasurement()
        
        self.FileStartLineEdit.setText('')
    
    def batchxrfs(self):
        self.ExpTypeLineEdit.setText('xrfs')
        self.UserNameLineEdit.setText('xrfs')
        self.savebinaryCheckBox.setChecked(False)

        self.RunTypeLineEdit.setText('data')
        
        mainitem=self.techtypetreefcns.typewidgetItem
        for i in range(mainitem.childCount()):
            mainitem.child(i).setCheckState(0, Qt.Unchecked if 'binary' in str(mainitem.child(i).text(0)) else Qt.Checked)
    
        self.editexp_addmeasurement()
#    def batchrunfoms_multitoggle_leds(self):
#        ans=userinputcaller(self, inputs=[('optimal power (mW)\nfor each toggle channel\n<leave blank to use rcp values>', str, ''), \
#                                                    ('rcp key with the optical\npower values in mW\n<if this is also blank then no calibration>', str, 'illumination_intensity')\
#                                                         ], title='enter the LED calibration info (mW of optical pwoer)',  cancelallowed=True)
#        if ans is None:
#            return
#        if len(ans[0].strip())>0:
#            mWvals=ans[0].strip().split(',')
#            mWvals_rcpd=lambda rcpd:mWvals
#        elif len(ans[1].strip())>0:
#            mWrcpk=ans[1].strip()
#            mWvals_rcpd=lambda rcpd:rcpd[mWrcpk].strip().split(',')
#        else:
#            mWvals_rcpd=lambda rcpd:None
#        
#        def run_foms_fcn(rcpd):
#            
#        
#        
#        self.run_foms_fcn=
#        self.editexp_addmeasurement()
        
    def batchuvissingleplate_norefdata(self):
        
        self.ExpTypeLineEdit.setText('uvis')
        self.UserNameLineEdit.setText('uvis')
        self.savebinaryCheckBox.setChecked(False)
        cb=self.PlateAttrMoreComboBox
        for i in range(int(cb.count())):
            if 'Sample' in str(cb.itemText(i)):
                cb.setCurrentIndex(i)
                break
        self.RunTypeLineEdit.setText('data')
        self.FileStartLineEdit.setText('')
        self.FileNotStartLineEdit.setText('0_')
        self.editexp_addmeasurement()
        cb.setCurrentIndex(0)
        
        self.FileNotStartLineEdit.setText('')
        
        self.RunTypeLineEdit.setText('ref_dark')
        self.FileStartLineEdit.setText('0_-1_')
        self.editexp_addmeasurement()
        
        self.RunTypeLineEdit.setText('ref_light')
        self.FileStartLineEdit.setText('0_1_')
        self.editexp_addmeasurement()
        
        self.FileStartLineEdit.setText('')
        
    def batchechedark(self):

        self.techtypetreefcns.checkbysearchstr('spectrum', self.techtypetreefcns.typewidgetItem)

        self.RunTypeLineEdit.setText('ref_dark')
        self.FileSearchLineEdit.setText('_DARK')
        self.editexp_addmeasurement()
        
        self.RunTypeLineEdit.setText('data')
        self.FileSearchLineEdit.setText('')
        self.techtypetreefcns.checkbysearchstr('', self.techtypetreefcns.typewidgetItem)
    
    def batchechewavelengths(self):
        self.batchmode=True
        for wl in ['385', '455', '530', '617']:
            self.FileSearchLineEdit.setText('-'+wl)
            self.UserFOMLineEdit.setText(wl)
            self.updateuserfomd(batchkeys=['user_fom_led_wavelength'])
            self.editexp_addmeasurement()
        self.FileSearchLineEdit.setText('')
        self.batchmode=False
        
    def clearexp(self):
        for rcpd in self.rcpdlist:
            rcpd['filenamedlist']=[dict(fd, previnexp=set([]), inexp=set([])) for fd in rcpd['filenamedlist']]
        self.expdlist_use={}
        self.ExpTreeWidget.clear()
        self.ExpTextBrowser.setText('')
        self.expfiledict={}
        self.expfilestr=''
        self.prevsaveexppath=None
    def removeruns(self):
        self.techlist=[]
        self.typelist=[]
        self.rcpdlist=[]
        
        self.techtypetreefcns.cleartree()
        self.RunTreeWidget.clear()
    
    #def undoexpfile(self):
        
    def importexpfile(self):
        p=selectexpanafile(self, exp=True, markstr='Select .exp/.pck EXP file, or .zip file')
        if len(p)==0:
            return
        self.removeruns()
        self.clearexp()
        techset, typeset, self.rcpdlist, self.expparamstuplist, self.expdlist_use=readexpasrcpdlist(p)
        self.techlist=list(techset)
        self.typelist=list(typeset)
        
        self.processrunimport()
#        for datause in self.expdlist_use.keys():
#            self.updateexp(datause)
#        #the above update for every data use is a little overkill but at least 1 reason (compared to the direct ui update below) it is necessary is that the rcpdlistind may be out of date due to rcpdlist sorting
#        
##the above re-creation of the .exp from import doesn't catch important keys so for now just import the runs
        self.clearexp()
        
        self.LastActionLineEdit.setText('Imported EXP including %d RUNs containing %d files' \
            %(len(self.rcpdlist), numpy.array([len(d['filenamedlist']) for d in self.rcpdlist]).sum()))

    def importexpparamsfile(self):
        p=selectexpanafile(self, exp=True, markstr='Select .exp/.pck EXP file, or .zip file')
        if len(p)==0:
            return

        importedexpparamstuplist=readexpasrcpdlist(p, only_expparamstuplist=True)
        self.expparamstuplist=[('exp_version:3',  [])]+[tup for tup in importedexpparamstuplist if not 'exp_version' in tup[0]]
        
        #if params were manually changed in the tree, those changes will be ignored here
        self.ExpTreeWidgetFcns.filltreeexp(self.expdlist_use, self.expparamstuplist)
        self.updateexpobjects_tree()
        
        self.LastActionLineEdit.setText('Imported EXP params')
    
    def searchforruns(self):
        idialog=SearchFolderDialog(parent=self, folderpath=self.defaultrcppath, title='Search for RUN folders')
        idialog.exec_()
        if not idialog.openfolder is None:
            self.importruns(startfolder=idialog.openfolder)
        elif not idialog.openpathlist is None:
            self.importruns(pathlist=idialog.openpathlist)
    
    def importruns_info(self):
        idialog=runsfrominfoDialog(parent=self, runtype=str(self.ExpTypeLineEdit.text()))
        if not idialog.exec_():
            return
        pathlist=[buildrunpath(p) for p in idialog.runpaths]
        if '' in pathlist:
            idialog=messageDialog(self, 'Some or all run paths not found')
            if not idialog.exec_():
                return
        
        rcpdictadditions=[tupl for tupl, p in zip(idialog.rcpdictadditions, pathlist) if len(p)>0]
        pathlist=[p for p in pathlist if len(p)>0]
        
        if len(pathlist)>0:
            self.importruns(pathlist=pathlist, rcpdictadditions=rcpdictadditions)
    
    def importruns_folder(self, folderp=None):
        if folderp is None:
            folderp=str(mygetdir(parent=self, xpath=self.defaultrcppath,markstr='Folder containing .rcp or set of .zip' ))
            if len(folderp)==0:
                return
        if folderp.endswith('.zip'):
            pathlist=[folderp]
        else:
            fns=os.listdir(folderp)
            rcpfns=[fn for fn in fns if fn.endswith('.rcp')]
            if len(rcpfns)==1:
                pathlist=[folderp]
            else:
                pathlist=[os.path.join(folderp, fn) for fn in fns if fn.endswith('.zip')]
                if len(pathlist)==0:
                    idialog=messageDialog(self, 'No .rcp or .zip found')
                    idialog.exec_()
                    return
        self.importruns(pathlist=pathlist)
        
        
    def importruns(self, pathlist=None, startfolder=None, rcpdictadditions=None):
        if pathlist is None:
            if startfolder is None:
                startfolder=self.defaultrcppath
            
            pathlist=mygetopenfiles(parent=self, xpath=startfolder,markstr='.zip runs', filename='' )
            if not (isinstance(pathlist, list) and len(pathlist)>0 and not (False in [p.endswith('.zip') for p in pathlist])):
                idialog=messageDialog(self, 'Need to select only .zip')
                idialog.exec_()
                return

        techset, typeset, rcpdlist=readrcpfrommultipleruns(pathlist, rcpdictadditions=rcpdictadditions)

        self.techlist=list(set(self.techlist).union(techset))
        self.typelist=list(set(self.typelist).union(typeset))
        self.rcpdlist+=rcpdlist
        self.processrunimport()
        self.LastActionLineEdit.setText('Imported %d RUNs containing %d files' \
            %(len(rcpdlist), numpy.array([len(d['filenamedlist']) for d in rcpdlist]).sum()))
    
    def processrunimport(self):
        if 'pstat_files' in self.typelist:
            temp=self.typelist.pop(self.typelist.index('pstat_files'))
            self.typelist=[temp]+self.typelist
        
        sorttups=sorted([(d['rcp_file']+str(count), d) for count, d in enumerate(self.rcpdlist)], reverse=True) #rcpfn is a time stamp so this will be reverse chron order
        self.rcpdlist=map(operator.itemgetter(1), sorttups)
        for d in self.rcpdlist:
            d['name']=d['rcp_file'].strip().rstrip('.rcp')
            if self.getplatemapCheckBox.isChecked():
                d['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(d['plateidstr']), \
                    erroruifcn=\
                lambda s:mygetopenfile(parent=self, xpath=PLATEMAPFOLDERS[0], markstr='Error: %s select platemap for plate_no %s' %(s, d['plateidstr'])))
            else:
                d['platemapdlist']=[]
        exp_type_list=[tup[0].partition(':')[2].strip() for d in self.rcpdlist for tup in d['rcptuplist'] if 'experiment_type' in tup[0]]
        if len(exp_type_list)>0:
            self.experiment_type=exp_type_list[0].lower()
        else:
            self.experiment_type='eche'
        self.expparamsdict_le_dflt['experiment_type'][1]=self.experiment_type
        self.expparamsdict_le_dflt['created_by'][1]=self.experiment_type

        for k, (le, dfltstr) in self.expparamsdict_le_dflt.items():
            if k in ['experiment_type', 'created_by']:
                le.setText(dfltstr)
        
        self.updaterunlist()


    def updaterunlist(self):
        self.RunTreeWidgetFcns.filltree(self.rcpdlist)
        #fill technique and file type check boxes
        
        self.techtypetreefcns.cleartree()
        for ind, (k, tl, treeitem) in enumerate([('tech', self.techlist, self.techtypetreefcns.techwidgetItem), ('type', self.typelist, self.techtypetreefcns.typewidgetItem)]):
            k_comments_tuplist=[]
            for t in tl:
                try:
                    smps=[fd['smp'] for d in self.rcpdlist for fd in d['filenamedlist'] if fd[k]==t]
                    k_comments_tuplist+=[(t, ['%d files' %len(smps),'Samples in\n[%d,%d]' %(min(smps), max(smps)), ])]
                except:
                    k_comments_tuplist+=[(t, ['%d files' %len(smps)])]
            self.techtypetreefcns.fillmainitem(k_comments_tuplist, treeitem)
            
        #fill run select comboboxs
        self.FilterRunComboBox.clear()
        self.FilterRunComboBox.insertItem(0, 'All RUNs')
        for i, d in enumerate(self.rcpdlist):
            self.FilterRunComboBox.insertItem(i+1, '(%d)' %(i+1)+d['rcp_file'])
        self.FilterRunComboBox.setCurrentIndex(0)
        self.RunPriorityLineEdit.setText(','.join(['%d' %(i+1) for i in range(len(self.rcpdlist))]))
    
        #fill platemap fields
        pmkeys=set([])
        for d in self.rcpdlist:
           if len(d['platemapdlist'])>0:
               pmkeys=pmkeys.union(set(d['platemapdlist'][0].keys()))
        pmkeys=list(pmkeys)
        if 'Sample' in pmkeys:
            temp=pmkeys.pop(pmkeys.index('Sample'))
            pmkeys=[temp]+pmkeys
        for cb, sb in self.platemapEqualLessMore_combobox_spinbox:
            cb.clear()
            cb.insertItem(0, '')
            for i, k in enumerate(pmkeys):
                cb.insertItem(i+1, k)
            cb.setCurrentIndex(0)
    
    def getpriorityorderinds(self):
        dfltorder=['%d' %(i+1) for i in range(len(self.rcpdlist))]
        lestrlist=self.RunPriorityLineEdit.text().split(',')
        lestrlist=[str(s).strip() for s in lestrlist]
        order=[]
        for s in lestrlist:
            if s in dfltorder:
                spop=dfltorder.pop(dfltorder.index(s))
                order+=[spop]
        order+=dfltorder
        self.RunPriorityLineEdit.setText(','.join(order))
        orderinds=[eval(s)-1 for s in order]
        return orderinds
    #for inexp and previnexp no,yes,duplicate are 0,1,2. For filter criteria, N/A, fail and pass are -1,0,1. combine 0,1,2 possiblities from previous and -1,0,1 from current filtering na d provide 0,1,2
    #filter:               N/A fail pass
    # previous no ->  no    no   yes
    # previous yes->  yes    yes   yes
    def editexp_addmeasurement(self):
        inexpfcndict_previnexp_filter={};
        inexpfcndict_previnexp_filter[0]=lambda filterresult: (filterresult==1) and set.union or set.difference
        inexpfcndict_previnexp_filter[1]=lambda filterresult: set.union
        #inexpfcndict_previnexp_filter[2]=lambda filterresult: 1
        #rundesc=filterchars(str(self.RunDescLineEdit.text()).strip(), valid_chars = "-_.; ()%s%s" % (string.ascii_letters, string.digits))
        self.editexp(inexpfcndict_previnexp_filter, user_run_foms=self.userfomd, run_foms_fcn=self.run_foms_fcn)#, rundesc=rundesc)
        self.updateuserfomd(clear=True)
        #self.RunDescLineEdit.setText('')
    #filter:               N/A fail pass
    # previous no ->  no     no    no
    # previous yes->  yes   no   yes
    def editexp_filtercriteria(self):
        inexpfcndict_previnexp_filter={}
        inexpfcndict_previnexp_filter[0]=lambda filterresult: set.difference
        inexpfcndict_previnexp_filter[1]=lambda filterresult: abs(filterresult) and set.union or set.difference
        #inexpfcndict_previnexp_filter[2]=lambda filterresult: abs(filterresult)
        self.editexp(inexpfcndict_previnexp_filter)
    
    def editexp(self, inexpfcndict, user_run_foms={}, run_foms_fcn=None):#, rundesc=''):#for the user-specified data use, uses inexpfcndict to add or remove a file from the exp based on whether the fiel was not or was in the exp already. uses orderinds to define priority of evaluating the rcpdlist, the inexp and previnexp keys of the rcpd are the notable items being set here
        selrun=self.FilterRunComboBox.currentIndex()
        datause=str(self.RunTypeLineEdit.text()).strip()
        dus=set([datause])
        orderinds=self.getpriorityorderinds()
        prevnumfiles=len([fd['fn'] for rcpd in self.rcpdlist for fd in rcpd['filenamedlist'] if datause in fd['inexp']])
        expfilelist=[]
        for ind in orderinds:
            rcpd=self.rcpdlist[ind]
            rcpd['filenamedlist']=[dict(fd, previnexp=fd['inexp']) for fd in rcpd['filenamedlist']]
            if selrun==0 or (selrun-1)==ind:# if considering all or this is the 1 we are considering then build an evaluation function
                evalfilters=self.createFilterEvalFcn(rcpd)
                #print [evalfilters(fd) for fd in rcpd['filenamedlist']]
            else:#otherwise we are not considering this one so result is -1, i.e. "N/A"
                evalfilters=lambda fd:-1
                print ind, orderinds
            rcpd['filenamedlist']=[dict(fd, inexp=\
                inexpfcndict[datause in fd['previnexp']](evalfiltresult * int(not fd['fn'] in expfilelist))(fd['previnexp'], dus)\
                                                         ) \
                for fd, evalfiltresult in zip(rcpd['filenamedlist'], map(evalfilters, rcpd['filenamedlist']))]
            #rcpd['fns_inexp']=
            fns_inexp=[fd['fn'] for fd in rcpd['filenamedlist'] if datause in fd['inexp']]
            expfilelist+=fns_inexp#rcpd['fns_inexp']
            #print rcpd['fns_inexp']

        #create a default description from list of techniques and types after filtering done and if the description line edit equals the previous default, update the line edit
        techs=list(set([fd['tech'] for rcpd in self.rcpdlist for fd in rcpd['filenamedlist'] if fd['inexp']]))
        types=list(set([fd['type'] for rcpd in self.rcpdlist for fd in rcpd['filenamedlist'] if fd['inexp']]))
        
        newdflt='Technique %s with file type %s.' %(','.join(techs), ','.join(types))
        
        le, dflt=self.expparamsdict_le_dflt['description']
        s=str(le.text()).strip()
        s=filterchars(s, valid_chars = "-_.; ()%s%s" % (string.ascii_letters, string.digits))
        if s==dflt or len(s)==0:
            le.setText(newdflt)
        self.expparamsdict_le_dflt['description'][1]=newdflt
        

        self.updateexp(datause, user_run_foms=user_run_foms, run_foms_fcn=run_foms_fcn)#, rundesc=rundesc)
        
        numfiles=len(expfilelist)
        delnumfiles=numfiles-prevnumfiles
        if delnumfiles>=0:
            s='%d %s files added to EXP,' %(delnumfiles, datause)
        else:
            s='%d %s files removed from EXP,' %(-delnumfiles, datause)
        s+=' now %d %s files.' %(numfiles, datause)
        self.LastActionLineEdit.setText(s)

    
    def createFilterEvalFcn(self, rcpd):

        techlist=self.techtypetreefcns.strlist_checked(self.techtypetreefcns.techwidgetItem)
        techfcn=lambda fd:fd['tech'] in techlist
        
        typelist=self.techtypetreefcns.strlist_checked(self.techtypetreefcns.typewidgetItem)
        typefcn=lambda fd:fd['type'] in typelist
        
        filesearchfcn=self.createFileSearchfilterfcn()
        platemapfcn=self.createPlatemapfilterfcn(rcpd)
        fcn=lambda fd:techfcn(fd) and typefcn(fd) and filesearchfcn(fd) and platemapfcn(fd)
        return fcn

    def createPlatemapfilterfcn(self, rcpd):
        smpliststr=str(self.SampleListLineEdit.text()).strip()
        selsmplist=smpliststr.split(',')
        selsmplist=[int(s.strip()) for s in selsmplist if s.strip().isdigit()]
        if not ((True in [cb.currentIndex()>0 for cb, sb in self.platemapEqualLessMore_combobox_spinbox]) or len(selsmplist)>0):
            return lambda fd:True
        if len(selsmplist)>0:
            smplist=selsmplist
        else:
            smplist=[d['Sample'] for d in rcpd['platemapdlist']]
        
        for count, (cb, sb) in enumerate(self.platemapEqualLessMore_combobox_spinbox):
            if cb.currentIndex()==0:
                continue
            k=str(cb.currentText()).strip()
            
            compareval=float(sb.value())
            if count==0:
                comparefcn=lambda v: v==compareval
            elif count==1:
                comparefcn=lambda v: v<compareval
            else:
                comparefcn=lambda v: v>compareval
            smplist=[d['Sample'] for d in rcpd['platemapdlist'] if d['Sample'] in smplist and k in d.keys() and comparefcn(d[k])]
        return lambda fd:fd['smp'] in smplist
    def createFileSearchfilterfcn(self):
        s=str(self.FileSearchLineEdit.text()).strip()
        ns=str(self.FileNotSearchLineEdit.text()).strip()
        ss=str(self.FileStartLineEdit.text()).strip()
        nss=str(self.FileNotStartLineEdit.text()).strip()
        if len(s)==0 and len(ss)==0 and len(ns)==0 and len(nss)==0:
            return lambda fd:True
        elif  len(ns)==0 and len(nss)==0:
            return lambda fd:s in fd['fn'] and fd['fn'].startswith(ss)
        else:#ns or nss not zero so checking is more complicated becauase these are onyl valid if their length is >0
            return lambda fd:(s in fd['fn']) and \
                                      fd['fn'].startswith(ss) and \
                                      (len(ns)==0 or not ns in fd['fn']) and\
                                      (len(nss)==0 or not fd['fn'].startswith(nss))
    
    def editexpparams(self, item, column):
        self.editparams(self.ExpTreeWidget, item=item, column=column)
    def editrunparams(self, item, column):
        self.editparams(self.RunTreeWidget, item=item, column=column)
    def editparams(self, widget, item=None, column=0):
        if item is None:
            item=widget.currentItem()
        s=str(item.text(column))
        st=s.partition(': ')
        k=''.join(st[:2])
        v=st[2].strip()
        if len(v)==0:
            print 'Error editing param,  no value detected: ', s
            return
        ans=userinputcaller(self, inputs=[(k, str, v)], title='Enter new param value',  cancelallowed=True)
        if ans is None or ans[0].strip()==v:
            return
        ans=ans[0].strip()
        
        warningkeys=['rcp_version', 'plate_id', 'computer_name', 'experiment_type', 'file_format_version', 'exp_version', 'run_use', 'run__']
        echewarningkeys=['electrolyte', 'concentration', 'solution_ph', 'redox_couple_type', 'ref_electrode_type','measurement_area']
        echeactionkeys=['reference_vrhe', 'reference_e0']
        
        if True in [kv in k for kv in warningkeys]:
            idialog=messageDialog(self, 'THIS IS CONSIDERED A READ-ONLY PARAMETER.\nYOU SHOULD PROBABLY "Cancel"')
            if not idialog.exec_():
                return
        if True in [kv in k for kv in echewarningkeys]:
            idialog=messageDialog(self, 'THIS PARAM EFFECTS reference_vrhe and reference_e0\nBUT THEY WILL NOT BE AUTOMATICALY UPDATED.\nYOU SHOULD PROBABLY "Cancel"')
            if not idialog.exec_():
                return
        for kv in echeactionkeys:
            if kv in k:
                idialog=messageDialog(self, echeparamactiondict[kv]['message'])
                if idialog.exec_():
                    echeparamactiondict[kv]['changefcn'](item, v, ans)
        item.setText(column,''.join([k, ans]))

    def updateexp(self, datause, user_run_foms={}, run_foms_fcn=None):#, rundesc=''):
        #make expdlist_use a copy of rcpdlist but update each rcptuplist so that the files sections contain on "in exp" files
        #[tup for tup in rcpd['rcptuplist'] if not tup[0].startswith('files_technique__')], \
        
        #the rcpdlistind is update here for this datause but other datause may be out of date and this can become out of date if more RUNs are imported
        self.expdlist_use[datause]=[dict(rcpd, rcpdlistind=count, \
            rcptuplist=\
            self.RunTreeWidgetFcns.createtuplist_item(self.RunTreeWidget.topLevelItem(count), filesbool=False)[1], \
            filenamedlist=\
            [fd for fd in rcpd['filenamedlist'] if datause in fd['inexp']], \
            user_run_foms=user_run_foms, \
            ) for count, rcpd in enumerate(self.rcpdlist) \
            if len([fd for fd in rcpd['filenamedlist'] if datause in fd['inexp']])>0]

        for expd in self.expdlist_use[datause]:
            rcpd=self.rcpdlist[expd['rcpdlistind']]
            #tublistinds gives the 3-level indices for where a filname was in the rcp tuplist, i.e. technique index (wrt root-level rcp lines), type index, file index
            tuplistinds_inexp=[fd['tuplistinds'] for fd in rcpd['filenamedlist'] if datause in fd['inexp']]
            i0vals=sorted(list(set([i0 for i0, i1, i2 in tuplistinds_inexp])))
            filetuplist=[]
            filecount=0
            techlist=[]
            for i0v in i0vals:
                k0, l0=rcpd['rcptuplist'][i0v]
                i1vals=sorted(list(set([i1 for i0, i1, i2 in tuplistinds_inexp if i0==i0v])))
                l0n=[]
                for i1v in i1vals:
                    k1, l1=l0[i1v]
                    l1n=[tup for i2v, tup in enumerate(l1) if (i0v, i1v, i2v) in tuplistinds_inexp]
                    if len(l1n)>0:
                        l0n+=[(k1, l1n)]
                        filecount+=len(l1n)
                if len(l0n)>0:
                    filetuplist+=[(k0, l0n)]
                    techlist+=[k0.partition('__')[2].strip().strip(':')]
                    
            expd['rcptuplist']+=filetuplist
            if not run_foms_fcn is None:
                rcpdict_temp=dict([createdict_tup(tup) for tup in expd['rcptuplist']])
                expd['run_foms']=run_foms_fcn(rcpdict_temp)
            

        #params
        self.expparamstuplist=[('exp_version: 3',  [])]

        for k, (le, dfltstr) in self.expparamsdict_le_dflt.items():
            s=str(le.text()).strip()
            if len(s)==0:
                s=dfltstr
            self.expparamstuplist+=[(k+': '+s , [])]
        plateidstemp=[d['plateidstr'] if 'plateidstr' in d.keys() else None for dlist in self.expdlist_use.itervalues() for d in dlist]
        if None in plateidstemp:
            idialog=messageDialog(self, 'WARNING: plate_id missing for at least 1 run')
            idialog.exec_()
#        plateids=sorted(list(set([id for id in plateidstemp if not id is None])))
#        if len(plateids)>0:
#            plateidsstr=','.join(plateids)
#            self.expparamstuplist+=[('plate_ids: '+plateidsstr, [])]
        self.ExpTreeWidgetFcns.filltreeexp(self.expdlist_use, self.expparamstuplist)
        self.updateexpobjects_tree()
    
    def updateexpobjects_tree(self):
        self.expfiledict=self.ExpTreeWidgetFcns.createdict()
        self.expfilestr=self.ExpTreeWidgetFcns.createtxt()
        self.ExpTextBrowser.setText(self.expfilestr)
    
    def saveexpgoana(self):
        self.hide()
        saveexpfiledict, exppath=self.saveexp()
        self.parent.calcexp(expfiledict=copy.deepcopy(saveexpfiledict), exppath=exppath)
        for runk, rund in self.parent.calcui.expfiledict.iteritems():#copy over any platemap info
            if not runk.startswith('run__'):
                continue
            rcpfile=rund['rcp_file']
            rcpdl=[rcpd for rcpd in self.rcpdlist if rcpd['rcp_file']==rcpfile and len(rcpd['platemapdlist'])>0]
            if len(rcpdl)>0:
                rund['platemapdlist']=copy.copy(rcpdl[0]['platemapdlist'])
        

    def saveexpgovis(self):
        self.hide()
        saveexpfiledict, exppath=self.saveexp()
        self.parent.visexpana(experiment_path=os.path.split(exppath)[0])
        
    def saveexp(self, exptype=None, rundone=None):
        #self.expfilestr, self.expfiledict are read from the tree so will include edited params
        if not 'experiment_type' in self.expfiledict.keys():
            idialog=messageDialog(self, 'Aborting SAVE because no data in EXP')
            idialog.exec_()
            return
        if exptype is None:
            savefolder=None
            idialog=SaveOptionsDialog(self, self.expfiledict['experiment_type'])
            idialog.exec_()
            if not idialog.choice:
                return
            exptype=idialog.choice
            if idialog.choice=='browse':
                savefolder=mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Select folder for saving EXP')
                if savefolder is None or len(savefolder)==0:
                    return
        else:
            savefolder=None
            
        if len(self.expfilestr)==0 or not 'exp_version' in self.expfilestr:
            return
        runtodonesavep=None
        if rundone is None:
            if savefolder is None and not self.prevsaveexppath is None and os.path.split(self.prevsaveexppath)[0].endswith('run'):
                idialog=messageDialog(self, 'convert the .run to a .done?')
                if idialog.exec_():
                    rundone='.done'
                    runtodonesavep=self.prevsaveexppath
                else:
                    rundone='.run'#will get a new timestamp
            else:
                idialog=messageDialog(self, 'save as .done ?')
                if idialog.exec_():
                    rundone='.done'
                else:
                    rundone='.run'
        saverawdat=self.savebinaryCheckBox.isChecked()
        saveexpfiledict, exppath = saveexp_txt_dat(self.expfiledict, rundone=rundone, experiment_type=exptype, runtodonesavep=runtodonesavep, savefolder=savefolder, saverawdat=saverawdat, erroruifcn=\
            lambda s:mygetsavefile(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s, select file for saving EXP', filename='%s.exp' %str(self.ExpNameLineEdit.text())))
        
        self.prevsaveexppath=exppath
        return saveexpfiledict, exppath




class treeclass_techtype():
    def __init__(self, tree):
        self.treeWidget=tree
        self.cleartree()
    def cleartree(self):#, tech_comments_tuplist, type_comments_tuplist):
        self.treeWidget.clear()
        
        self.techwidgetItem=QTreeWidgetItem(['techniques'], 0)
        #self.fillmainitem(tech_comments_tuplist, self.techwidgetItem)
        self.treeWidget.addTopLevelItem(self.techwidgetItem)
        self.techwidgetItem.setExpanded(True)
        
        self.typewidgetItem=QTreeWidgetItem(['file types'], 0)
        #self.fillmainitem(type_comments_tuplist, self.typewidgetItem)
        self.treeWidget.addTopLevelItem(self.typewidgetItem)
        self.typewidgetItem.setExpanded(True)
        
    def fillmainitem(self, k_comments_tuplist, mainitem):
        for k, comments in k_comments_tuplist:
            item=QTreeWidgetItem([k], 0)
            item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
            mainitem.addChild(item)
            for s in comments:
                item2=QTreeWidgetItem([s], 0)
                item.addChild(item2)
            item.setExpanded(False)
    
    def checkbysearchstr(self, searchstr, mainitem):
        for i in range(mainitem.childCount()):
            mainitem.child(i).setCheckState(0, Qt.Checked if searchstr in str(mainitem.child(i).text(0)) else Qt.Unchecked)
    
    def strlist_checked(self, mainitem):
        return [str(mainitem.child(i).text(0)) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]

class treeclass_dlist():
    def __init__(self, tree, key_toplevel='rcp_file', key_nestedfill='rcptuplist'):
        self.treeWidget=tree
        self.treeWidget.clear()
        self.ktl=key_toplevel
        self.knf=key_nestedfill

    def createtuplist_item(self, item, filesbool=True):
        tuplist=[]
        for i in range(item.childCount()):
            if filesbool or not str(item.child(i).text(0)).startswith('files_technique__'):
                tuplist+=[self.createtuplist_item(item.child(i), filesbool=filesbool)]
        return (str(item.text(0)), tuplist)
        
    def filltree(self, dlist, addcountstr=True):
        self.treeWidget.clear()
        if len(dlist)==0:
            return
        for i, d in enumerate(dlist):
            if addcountstr:
                s='(%d)' %(i+1)+d[self.ktl]
            else:
                s=d[self.ktl]
            mainitem=QTreeWidgetItem([s], 0)
            if i==0:
                item0=mainitem
            self.treeWidget.addTopLevelItem(mainitem)
            self.nestedfill(d[self.knf], mainitem)
            mainitem.setExpanded(False)
            
        self.treeWidget.setCurrentItem(item0)

    def filltreeexp(self, expdlist_use, expparamstuplist):
        self.treeWidget.clear()
        #add all exp-level params as parent items
        for (lab, l) in expparamstuplist:
            if len(l)==0:
                inttype=1000
            else:
                inttype=2000
            mainitem=QTreeWidgetItem([lab],  inttype)
            if len(l)>0:
                self.nestedfill(l, mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
        #add rcps with run__1 as label
        count=0
        for k, dlist in expdlist_use.iteritems():
            for d in dlist:
                count+=1
                s='run__%d:' %(count)
                mainitem=QTreeWidgetItem([s],  0)
                self.treeWidget.addTopLevelItem(mainitem)
                
                rp=d['run_path']
                
                runparams=['name: '+d['name'],'run_use: '+k, 'run_path: '+rp, 'rcp_file: '+d['rcp_file']]
                
                filecount=numpy.array([len(tup2[1]) for tup in d[self.knf] for tup2 in tup[1] if tup[0].startswith('files_technique__')]).sum()
                techlist=list(set([tup[0].partition('files_technique__')[2].strip().strip(':') for tup in d[self.knf] if tup[0].startswith('files_technique__')]))
                plateid=[tup[0].partition('plate_id: ')[2].strip() for tup in d[self.knf] if tup[0].startswith('plate_id: ')][0]
                rundesc='; '.join(['%d files' %filecount, ','.join(techlist), 'plate_id '+plateid, k])
                runparams+=['description: '+rundesc]
                
                for lab in runparams:
                    item=QTreeWidgetItem([lab],  1000)
                    mainitem.addChild(item)
                if 'user_run_foms' in d.keys() and len(d['user_run_foms'])>0:
                    self.nestedfill([('user_run_foms:', [(': '.join(kv), []) for kv in d['user_run_foms'].iteritems()])], mainitem)
                if 'run_foms' in d.keys() and len(d['run_foms'])>0:
                    self.nestedfill([('run_foms:', [(': '.join(kv), []) for kv in d['run_foms'].iteritems()])], mainitem)#assumes run_foms values are strings
                    
                self.nestedfill([('parameters:', [tup for tup in d[self.knf] if not tup[0].startswith('files_technique__')])], mainitem)
                self.nestedfill([tup for tup in d[self.knf] if tup[0].startswith('files_technique__')], mainitem)
                mainitem.setExpanded(False)
            

    def nestedfill(self, nestedtuplist, parentitem):
        for (lab, l) in nestedtuplist:
            if len(l)==0:
                inttype=1000
            else:
                inttype=2000
            item=QTreeWidgetItem([lab],  inttype)
            if len(l)>0:
                self.nestedfill(l, item)
            parentitem.addChild(item)
            
    def createtxt(self, indent='    '):
        self.indent=indent
        return '\n'.join([self.createtxt_item(self.treeWidget.topLevelItem(count)) for count in range(int(self.treeWidget.topLevelItemCount()))])
        
    def createtxt_item(self, item, indentlevel=0):
        str(item.text(0))
        itemstr=self.indent*indentlevel+str(item.text(0)).strip()
        if item.childCount()==0:
            return itemstr
        childstr='\n'.join([self.createtxt_item(item.child(i), indentlevel=indentlevel+1) for i in range(item.childCount())])
        return '\n'.join([itemstr, childstr])
    
    def partitionlineitem(self, item):
        s=str(item.text(0)).strip()
        a, b, c=s.partition(':')
        return (a.strip(), c.strip())
    def createdict(self):
        return dict(\
        [self.createdict_item(self.treeWidget.topLevelItem(count))\
            for count in range(int(self.treeWidget.topLevelItemCount()))])
        
    def createdict_item(self, item):
        tup=self.partitionlineitem(item)
        if item.childCount()==0:
            return tup
        d=dict([self.createdict_item(item.child(i)) for i in range(item.childCount())])
        return (tup[0], d)
        
# this section automically shifts echem potentials by the same amount when 1 is changed *******
def updateecheparamsfcn(item, oldstr, newstr, keystoalter=[]):
    delta=float(newstr)-float(oldstr)
    for alterk in keystoalter:
        par=item.parent()
        for i in range(par.childCount()):
            if str(par.child(i).text(0)).startswith(alterk):
                alteritem=par.child(i)
                s=str(alteritem.text(0))
                st=s.partition(': ')
                k=''.join(st[:2])
                v=st[2].strip()
                newstr='%.3f' %(float(v)+delta)
                alteritem.setText(0,''.join([k, newstr]))
                break
                
echeparamactiondict={}

echeparamactiondict['reference_vrhe']={}
echeparamactiondict['reference_vrhe']['message']='Press "OK" to also update reference_e0 \n "Cancel" will still update reference_vrhe'
echeparamactiondict['reference_vrhe']['changefcn']=lambda item, oldstr, newstr:updateecheparamsfcn(item, oldstr, newstr, keystoalter=['reference_e0'])

echeparamactiondict['reference_e0']={}
echeparamactiondict['reference_e0']['message']='Press "OK" to alos update reference_vrhe \n "Cancel" will still update reference_e0'
echeparamactiondict['reference_e0']['changefcn']=lambda item, oldstr, newstr:updateecheparamsfcn(item, oldstr, newstr, keystoalter=['reference_vrhe'])
#*********************************************************************************************


if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
            super(MainMenu, self).__init__(None)
            #self.setupUi(self)
            self.expui=expDialog(self, title='Create/Edit an Experiment', **kwargs)
            #self.expui.importruns(pathlist=['20150422.145113.donex.zip'])
            #self.expui.importruns(pathlist=['uvis'])
            if execute:
                self.expui.exec_()
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    
    #form.expui.exec_()
    
    mainapp.exec_()

#form.expui.expdlist_use
