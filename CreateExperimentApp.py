#cd C:\Python27\Lib\site-packages\PyQt4
#pyuic4 -x C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\QtDesign\CreateExpForm.ui -o C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\CreateExpForm.py
import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pylab
import pickle
from fcns_math import *
from fcns_io import *
from fcns_ui import *
from CreateExpForm import Ui_CreateExpDialog
from SearchFolderApp import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter

matplotlib.rcParams['backend.qt4'] = 'PyQt4'


    
class expDialog(QDialog, Ui_CreateExpDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(expDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        
        self.RunTreeWidgetFcns=treeclass_dlist(self.RunTreeWidget, key_toplevel='rcp_file', key_nestedfill='rcptuplist')
        self.ExpTreeWidgetFcns=treeclass_dlist(self.ExpTreeWidget, key_toplevel='rcp_file', key_nestedfill='rcptuplist')
        QObject.connect(self.RunTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.editrunparams)
        QObject.connect(self.ExpTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.editexpparams)

        button_fcn=[\
        (self.AddMeasPushButton, self.editexp_addmeasurement), \
        (self.FilterMeasPushButton, self.editexp_filtercriteria), \
        (self.ImportRunsPushButton, self.importruns), \
        (self.SearchRunsPushButton, self.searchforruns), \
        (self.RemoveRunsPushButton, self.removeruns), \
        (self.ImportExpParamsPushButton, self.importexpparamsfile), \
        (self.ImportExpPushButton, self.importexpfile), \
        (self.ClearExpPushButton, self.clearexp), \
        (self.SaveExpPushButton, self.saveexp), \
        (self.BatchPushButton, self.runbatchprocess), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        #        (self.EditParamsPushButton, self.editrunparams), \
        #(self.EditExpParamsPushButton, self.editexpparams), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        
        
        self.batchprocesses=[self.batchuvissingleplate]
        batchdesc=['Filter uvis into data, ref_light, ref_dark']
        for i, l in enumerate(batchdesc):
            self.BatchComboBox.insertItem(i, l)
        #These are the filter criteria controls
        
        self.TechCheckBoxList=[self.TechCheckBox_0, self.TechCheckBox_1, self.TechCheckBox_2, self.TechCheckBox_3, self.TechCheckBox_4, self.TechCheckBox_5, self.TechCheckBox_6, self.TechCheckBox_7]
        self.FiletypeCheckBoxList=[self.FiletypeCheckBox_0, self.FiletypeCheckBox_1, self.FiletypeCheckBox_2, self.FiletypeCheckBox_3, self.FiletypeCheckBox_4, self.FiletypeCheckBox_5]
        
        self.platemapEqualLessMore_combobox_spinbox=[\
        (self.PlateAttrEqualComboBox, self.PlateAttrEqualSpinBox), \
        (self.PlateAttrLessComboBox, self.PlateAttrLessSpinBox), \
        (self.PlateAttrMoreComboBox, self.PlateAttrMoreSpinBox), \
        ]
        
        self.expparamsdict_le_dflt=dict([\
         ('access', [self.AccessLineEdit, 'hte']), \
         ('name', [self.ExpNameLineEdit, 'none']), \
         ('exp_type', [self.ExpTypeLineEdit, 'eche']), \
         ('created_by', [self.UserNameLineEdit, 'eche']), \
         ('description', [self.ExpDescLineEdit, 'null']), \
        ])
        
        self.defaultrcppath=os.getcwd()
        self.removeruns()
        self.clearexp()
        #self.expfilelist=[]
        #self.TechInFilesComboBox, self.FileInFilesComboBox
        #self.FileSearchLineEdit
        
    def runbatchprocess(self):
         self.batchprocesses[self.BatchComboBox.currentIndex()]()
    def batchuvissingleplate(self):
        cb=self.PlateAttrMoreComboBox
        for i in range(int(cb.count())):
            if 'Sample' in str(cb.itemText(i)):
                cb.setCurrentIndex(i)
                break
        self.RunTypeLineEdit.setText('data')
        self.editexp_addmeasurement()
        cb.setCurrentIndex(0)
        
        self.RunTypeLineEdit.setText('ref_dark')
        self.FileSearchLineEdit.setText('0_-1_')
        self.editexp_addmeasurement()
        
        self.RunTypeLineEdit.setText('ref_light')
        self.FileSearchLineEdit.setText('0_1_')
        self.editexp_addmeasurement()
        
        self.FileSearchLineEdit.setText('')
        
    
    def clearexp(self):
        for rcpd in self.rcpdlist:
            rcpd['filenamedlist']=[dict(fd, previnexp=set([]), inexp=set([])) for fd in rcpd['filenamedlist']]
        self.expdlist_use={}
        self.ExpTreeWidget.clear()
        self.ExpTextBrowser.setText('')
        self.expfiledict={}
        self.expfilestr=''
    def removeruns(self):
        self.techlist=[]
        self.typelist=[]
        self.rcpdlist=[]
        for cbl in [self.TechCheckBoxList, self.FiletypeCheckBoxList]:
            for cb in cbl:
                cb.setText('')
                cb.setToolTip('')
        self.RunTreeWidget.clear()
    
    #def undoexpfile(self):
        
    def importexpfile(self):
        p=mygetopenfile(self, markstr='open EXP for edit', filename='.exp' )
        if len(p)==0:
            return
        self.removeruns()
        self.clearexp()
        techset, typeset, self.rcpdlist, self.expparamstuplist, self.expdlist_use=readexpasrcpdlist(p)
        self.techlist=list(techset)
        self.typelist=list(typeset)
        
        self.processrunimport()
        for datause in self.expdlist_use.keys():
            self.updateexp(datause)
        #the above update for every data use is a little overkill but at least 1 reason (compared to the direct ui update below) it is necessary is that the rcpdlistind may be out of date due to rcpdlist sorting
#        self.ExpTreeWidgetFcns.filltreeexp(self.expdlist_use, self.expparamstuplist)
#        self.expfiledict=self.ExpTreeWidgetFcns.createdict()
#        self.expfilestr=self.ExpTreeWidgetFcns.createtxt()
#        self.ExpTextBrowser.setText(self.expfilestr)
        
        self.LastActionLineEdit.setText('Imported EXP including %d RUNs containing %d files' \
            %(len(self.rcpdlist), numpy.array([len(d['filenamedlist']) for d in self.rcpdlist]).sum()))

    def importexpparamsfile(self):
        p=mygetopenfile(self, markstr='open EXP to extract top level params', filename='.exp' )
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
        
    def importruns(self, pathlist=None, startfolder=None):
        if pathlist is None:
            #pathlist=mygetopenfiles()
            if startfolder is None:
                startfolder=self.defaultrcppath
            gff=getexistingFilesFolders(self, 'Open RUNs: Select Folders and .zip or .rcp Files', startfolder)
            gff.exec_()
            pathlist=gff.filesSelected()
            if not (isinstance(pathlist, list) and len(pathlist)>0 and len(pathlist[0])>0):
                idialog=messageDialog(self, 'Need to select .zip and/or folder and press "Open"')
                idialog.exec_()
                return
        
        techset, typeset, rcpdlist=readrcpfrommultipleruns(pathlist)
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
        
        sorttups=sorted([(d['rcp_file'], d) for d in self.rcpdlist], reverse=True) #rcpfn is a time stamp so this will be reverse chron order
        self.rcpdlist=map(operator.itemgetter(1), sorttups)
        for d in self.rcpdlist:
            d['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(d['plateidstr']), \
                erroruifcn=\
            lambda s:mygetopenfile(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s select platemap for plate_no %s' %(s, d['plateidstr'])))

        if True in [True for d in self.rcpdlist for tup in d['rcptuplist'] if 'computer_name' in tup[0] and 'UVIS' in tup[0]]:
            self.exp_type='uvis'
        else:
            self.exp_type='eche'
        self.expparamsdict_le_dflt['exp_type'][1]=self.exp_type
        self.expparamsdict_le_dflt['created_by'][1]=self.exp_type

        for k, (le, dfltstr) in self.expparamsdict_le_dflt.items():
            if k in ['exp_type', 'created_by']:
                le.setText(dfltstr)
        
        self.updaterunlist()
        
    def updaterunlist(self):
        self.RunTreeWidgetFcns.filltree(self.rcpdlist)
        #fill technique and file type check boxes
        for ind, (k, tl, cbl) in enumerate([('tech', self.techlist, self.TechCheckBoxList), ('type', self.typelist, self.FiletypeCheckBoxList)]):

            for t, cb in zip(tl, cbl):
                smps=[fd['smp'] for d in self.rcpdlist for fd in d['filenamedlist'] if fd[k]==t]
                cb.setText(t+('(%d)' %len(smps)))
                cb.setToolTip('Samples in [%d,%d]' %(min(smps), max(smps)))
                cb.setChecked(True)
            if len(tl)<len(cbl):
                for cb in cbl[len(tl):]:
                    cb.setText('')
                    cb.setToolTip('')
                    cb.setChecked(False)
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
        self.editexp(inexpfcndict_previnexp_filter)
        
    
    #filter:               N/A fail pass
    # previous no ->  no     no    no
    # previous yes->  yes   no   yes
    def editexp_filtercriteria(self):
        inexpfcndict_previnexp_filter={}
        inexpfcndict_previnexp_filter[0]=lambda filterresult: set.difference
        inexpfcndict_previnexp_filter[1]=lambda filterresult: abs(filterresult) and set.union or set.difference
        #inexpfcndict_previnexp_filter[2]=lambda filterresult: abs(filterresult)
        self.editexp(inexpfcndict_previnexp_filter)
    
    def editexp(self, inexpfcndict):
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
        if s==dflt or len(s)==0:
            le.setText(newdflt)
        self.expparamsdict_le_dflt['description'][1]=newdflt
        
        self.updateexp(datause)
        
        numfiles=len(expfilelist)
        delnumfiles=numfiles-prevnumfiles
        if delnumfiles>=0:
            s='%d %s files added to EXP,' %(delnumfiles, datause)
        else:
            s='%d %s files removed from EXP,' %(-delnumfiles, datause)
        s+=' now %d %s files.' %(numfiles, datause)
        self.LastActionLineEdit.setText(s)

    
    def createFilterEvalFcn(self, rcpd):
        strlist_cbl=lambda cbl:[str(cb.text()).partition('(')[0].strip() for cb in cbl if cb.isChecked()]
        techlist=strlist_cbl(self.TechCheckBoxList)
        techfcn=lambda fd:fd['tech'] in techlist
        
        typelist=strlist_cbl(self.FiletypeCheckBoxList)
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
        if len(s)==0:
            return lambda fd:True
        else:
            return lambda fd:s in fd['fn']
    
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

    def updateexp(self, datause):
        #make expdlist_use a copy of rcpdlist but update each rcptuplist so that the files sections contain on "in exp" files
        #[tup for tup in rcpd['rcptuplist'] if not tup[0].startswith('files_technique__')], \
        
        #the rcpdlistind is update here for this datause but other datause may be out of date and this can become out of date if more RUNs are imported
        self.expdlist_use[datause]=[dict(rcpd, rcpdlistind=count, \
            rcptuplist=\
            self.RunTreeWidgetFcns.createtuplist_item(self.RunTreeWidget.topLevelItem(count), filesbool=False)[1], \
            filenamedlist=\
            [fd for fd in rcpd['filenamedlist'] if datause in fd['inexp']]\
            ) for count, rcpd in enumerate(self.rcpdlist) \
            if len([fd for fd in rcpd['filenamedlist'] if datause in fd['inexp']])>0]

        for expd in self.expdlist_use[datause]:
            rcpd=self.rcpdlist[expd['rcpdlistind']]
            #tublistinds gives the 3-level indices for where a filname was in the rcp tuplist, i.e. technique index (wrt root-level rcp lines), type index, file index
            tuplistinds_inexp=[fd['tuplistinds'] for fd in rcpd['filenamedlist'] if datause in fd['inexp']]
            i0vals=sorted(list(set([i0 for i0, i1, i2 in tuplistinds_inexp])))
            filetuplist=[]
            for i0v in i0vals:
                k0, l0=rcpd['rcptuplist'][i0v]
                i1vals=sorted(list(set([i1 for i0, i1, i2 in tuplistinds_inexp if i0==i0v])))
                l0n=[]
                for i1v in i1vals:
                    k1, l1=l0[i1v]
                    l1n=[tup for i2v, tup in enumerate(l1) if (i0v, i1v, i2v) in tuplistinds_inexp]
                    if len(l1n)>0:
                        l0n+=[(k1, l1n)]
                if len(l0n)>0:
                    filetuplist+=[(k0, l0n)]
            expd['rcptuplist']+=filetuplist
        
#        #create master list of filename dicts for use in FOm anlaysis
#        self.expfilenamedlist=[dict(fd,runtype=expd['runtype'], runpath=expd['run_path'])  for expd in self.expdlist_use for fd in expd['filenamedlist']]
        
        #params
        self.expparamstuplist=[('exp_version: 3',  [])]

        for k, (le, dfltstr) in self.expparamsdict_le_dflt.items():
            s=str(le.text()).strip()
            if len(s)==0:
                s=dfltstr
            self.expparamstuplist+=[(k+': '+s , [])]
        
        self.ExpTreeWidgetFcns.filltreeexp(self.expdlist_use, self.expparamstuplist)
        self.updateexpobjects_tree()
    
    def updateexpobjects_tree(self):
        self.expfiledict=self.ExpTreeWidgetFcns.createdict()
        self.expfilestr=self.ExpTreeWidgetFcns.createtxt()
        self.ExpTextBrowser.setText(self.expfilestr)
        
    def saveexp(self):
        #self.expfilestr, self.expfiledict are read from the tree so will include edited params
        if len(self.expfilestr)==0 or not 'exp_version' in self.expfilestr:
            return
        saveexp_txt_dat(self.expfilestr, self.expfiledict, erroruifcn=\
            lambda s:mygetsavefile(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s, select file for saving EXP', filename='%s.exp' %str(self.ExpNameLineEdit.text())))

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
                runparams=['name: '+d[self.ktl],'run_use: '+k, 'run_path: '+d['run_path'], 'rcp_file: '+d['rcp_file']]
                for lab in runparams:
                    item=QTreeWidgetItem([lab],  1000)
                    mainitem.addChild(item)
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
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    
    #form.expui.exec_()
    
    mainapp.exec_()

#form.expui.expdlist_use
