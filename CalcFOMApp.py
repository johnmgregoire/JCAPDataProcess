import string
#import time
import os, os.path#, shutil
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
import matplotlib.colors as colors
import matplotlib.cm as cm
#import matplotlib.mlab as mlab
#import pylab
#import pickle

projectpath=os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath,'QtForms'))
sys.path.append(os.path.join(projectpath,'AuxPrograms'))
sys.path.append(os.path.join(projectpath,'OtherApps'))
sys.path.append(os.path.join(projectpath,'AnalysisFunctions'))


from fcns_math import *
from fcns_io import *
from fcns_ui import *
from CalcFOMForm import Ui_CalcFOMDialog
from SaveButtonForm import Ui_SaveOptionsDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'



from CA_CP_basics import *
from CV_photo import *
from OpenFromInfoApp import openfrominfoDialog
from FOM_process_basics import *
from import_scipy_foruvis import *
from eche_spectral import Analysis__SpectralPhoto
AnalysisClasses=[Analysis__Imax(), Analysis__Imin(), Analysis__Ifin(), Analysis__Efin(), Analysis__Etafin(), Analysis__Iave(), Analysis__Eave(), Analysis__Etaave(), Analysis__Iphoto(), Analysis__Ephoto(), Analysis__Etaphoto(), \
   Analysis__E_Ithresh(), Analysis__Eta_Ithresh(), \
   Analysis__Pphotomax(), Analysis__SpectralPhoto(), \
   Analysis__TR_UVVIS(), Analysis__BG(),Analysis__T_UVVIS(),Analysis__DR_UVVIS()\
    ]

FOMProcessClasses=[Analysis__AveCompDuplicates(), Analysis__Process_XRFS_Stds(), Analysis__FilterSmoothFromFile()]#Analysis__FilterSmoothFromFile must always be last because it is referred to with index -1 in the code
#NumNonPckBasedFilterSmooth=len(FOMProcessClasses)

DEBUGMODE=False

for ac in AnalysisClasses+FOMProcessClasses:
    ac.debugmode=DEBUGMODE

GUIMODE=True #when running this program all the classes will default to True and then if writing a batch script, need to turn gui_mode_bool to False
for ac in AnalysisClasses+FOMProcessClasses:
    ac.gui_mode_bool=GUIMODE
    
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
        
class calcfomDialog(QDialog, Ui_CalcFOMDialog):
    def __init__(self, parent=None, title='', folderpath=None, guimode=GUIMODE):
        super(calcfomDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
        self.guimode=guimode
        if guimode!=GUIMODE:
            for ac in AnalysisClasses+FOMProcessClasses:
                ac.gui_mode_bool=guimode
#        self.echem30=echem30axesWidget()
#        self.echem30.show()
        self.plotillumkey=None

        self.dbdatasource=0

        self.techniquedictlist=[]

        self.plotwsetup()
        button_fcn=[\
        (self.BatchPushButton, self.runbatchprocess), \
        (self.ImportExpPushButton, self.importexp), \
        (self.ImportAnaPushButton, self.importana), \
        (self.OpenInfoPushButton, self.importfrominfo), \
        (self.EditAnalysisParamsPushButton, self.editanalysisparams), \
        (self.AnalyzeDataPushButton, self.analyzedata), \
        (self.ViewResultPushButton, self.viewresult), \
        (self.SaveViewPushButton, self.saveview), \
        (self.EditDfltVisPushButton, self.editvisparams), \
        (self.SaveAnaPushButton, self.saveana), \
        (self.ClearAnalysisPushButton, self.clearanalysis), \
        (self.ClearSingleAnalysisPushButton, self.clearsingleanalysis), \
        (self.ImportAnalysisParamsPushButton, self.importanalysisparams), \
        (self.UpdatePlotPushButton, self.plotwithcaution), \
        (self.RaiseErrorPushButton, self.raiseerror), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        QObject.connect(self.UserFOMLineEdit,SIGNAL("editingFinished()"),self.updateuserfomd)


        QObject.connect(self.RunSelectTreeWidget, SIGNAL('itemChanged(QTreeWidgetItem*, int)'), self.runselectionchanged)
        self.runtreeclass=treeclass_anadict(self.RunSelectTreeWidget)
        
        QObject.connect(self.ExpRunUseComboBox,SIGNAL("activated(QString)"),self.fillruncheckboxes)
        
        #QObject.connect(self.TechTypeButtonGroup,SIGNAL("buttonClicked(QAbstractButton)"),self.fillanalysistypes)
        self.TechTypeButtonGroup.buttonClicked[QAbstractButton].connect(self.fillanalysistypes)
        
        QObject.connect(self.AnalysisNamesComboBox,SIGNAL("activated(QString)"),self.getactiveanalysisclass)
        QObject.connect(self.FOMProcessNamesComboBox,SIGNAL("activated(QString)"),self.getactiveanalysisclass)
        
        
        QObject.connect(self.fomplotchoiceComboBox,SIGNAL("activated(QString)"),self.plot_generatedata)
        QObject.connect(self.CompPlotTypeComboBox,SIGNAL("activated(QString)"),self.plot_generatedata)
        QObject.connect(self.stdcsvplotchoiceComboBox,SIGNAL("activated(QString)"),self.plot_preparestandardplot)
        QObject.connect(self.usedaqtimeCheckBox,SIGNAL("stateChanged()"),self.plot_generatedata)
        
        QObject.connect(self.AnaTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem)
        
        self.paramsdict_le_dflt=dict([\
         ('access', [self.AccessLineEdit, 'hte']), \
         ('name', [self.AnaNameLineEdit, 'temp_eche_name']), \
         ('analysis_type', [self.AnaTypeLineEdit, 'eche']), \
         ('created_by', [self.UserNameLineEdit, 'eche']), \
         ('description', [self.AnaDescLineEdit, 'null']), \
        ])
        
        self.batchprocesses=[self.batch_processallana, self.batch_analyzethenprocess, self.batch_process_allsubspace, \
                                      self.batch_analyzethenprocess_allsubspace, self.batch_analyze_fcn_same_techclass]
        batchdesc=['Run Prcoess FOM on all present ana__x', 'Run select Analysis and then Process', 'FOM Process: all Sub-Space w/ same root name',\
                         'Run Analysis + Process all w/ same root name', 'Run select Analysis on all similar techniques']
        for i, l in enumerate(batchdesc):
            self.BatchComboBox.insertItem(i, l)
            
        self.getplatemapCheckBox.setChecked(True)
        
        self.AnaTreeWidgetFcns=treeclass_anadict(self.AnaTreeWidget)
        self.exppath='null'
        self.tempanafolder=''
        self.expzipclass=None
        self.clearanalysis()
        self.updateuserfomd(clear=True)
        
    def raiseerror(self):
        raiseerror
    def updateuserfomd(self, clear=False):
        if clear:
            self.userfomd={}
            self.UserFOMLineEdit.setText('')
            self.text_UserFOMLineEdit=''
            return
            
        s=str(self.UserFOMLineEdit.text())
        if self.text_UserFOMLineEdit==s:#"duplicate" signals being emitted so ignore them 
            return
        self.text_UserFOMLineEdit=s

        vals=s.split(',')
        keys=['user_ana_fom__%d' %i for i, v in enumerate(vals)]
        ans=[]
        count=0
        while ans!=keys:
            inputs=[('key for %s' %v, str, k) for k, v in zip(keys, vals)]
            ans=userinputcaller(self, inputs=inputs, title='Enter user FOM keys',  cancelallowed=True)
            if ans is None:
                return
            keys=[filterchars(k) for k in ans]

            count+=1
        vals=[attemptnumericconversion(v.strip()) for v in vals]
        self.userfomd=dict([(k, v) for k, v in zip(keys, vals)])


    def edittreeitem(self, item, column):
        self.editparams(self.AnaTreeWidget, item=item, column=column)
        
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
        
        warningbool = (True in [ws in k for ws in ['version']])
        parent=item.parent()
        if parent is None:
            parentstr=''
        else:
            parentstr=parent.text(0)
        warningbool = warningbool or True in [ws in parentstr or ws in k for ws in ['ana__', 'parameters', 'files_']]
        
        
        if warningbool:
            idialog=messageDialog(self, 'THIS IS CONSIDERED A READ-ONLY PARAMETER.\nYOU SHOULD PROBABLY "Cancel"')
            if not idialog.exec_():
                return
        item.setText(column,''.join([k, ans]))
        kl=[k.partition(':')[0].strip()]
        while not item.parent() is None:
            item=item.parent()
            kl=[str(item.text(0)).partition(':')[0].strip()]+kl

        d=self.anadict
        while len(kl)>1:
            d=d[kl.pop(0)]
        d[kl[0]]=ans
        
    def importexp(self, expfiledict=None, exppath=None, expzipclass=None, anadict=None):
        if expfiledict is None:
            if exppath is None:
                exppath=selectexpanafile(self, exp=True, markstr='Select .exp/.pck EXP file, or containing .zip')
            if len(exppath)==0:
                return
            if not (exppath.endswith('.exp') or exppath.endswith('.pck') or not os.path.isabs(exppath)):
                exppath=buildexppath(exppath)
            expfiledict, expzipclass=readexpasdict(exppath, includerawdata=False, erroruifcn=None, returnzipclass=True)
            if expfiledict is None:
                print 'Problem opening EXP'
                return
        self.clearexp()
        self.exppath=exppath
        self.expfolder=os.path.split(exppath)[0]
        self.expfiledict=expfiledict
        if self.expzipclass:
            self.expzipclass.close()
        self.expzipclass=expzipclass
        self.FilterSmoothMapDict={}
        if self.getplatemapCheckBox.isChecked():
            for runk, rund in self.expfiledict.iteritems():
                if runk.startswith('run__') and not 'platemapdlist' in rund.keys()\
                         and 'parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
                         and 'plate_id' in rund['parameters'].keys():
                    rund['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(str(rund['parameters']['plate_id'])), \
                        erroruifcn=\
                    lambda s:mygetopenfile(parent=self, xpath=PLATEMAPBACKUP, markstr='Error: %s select platemap for plate_no %s' %(s, rund['parameters']['plate_id'])))
                if runk.startswith('run__') and not 'platemap_id' in rund.keys():
                    rund['platemap_id']=getplatemapid_plateidstr(str(rund['parameters']['plate_id']), erroruifcn=\
                    lambda s:userinputcaller(self, inputs=[('platemap id: ', str, '')], title=s,  cancelallowed=False)[0])
            platemapids=[rund['platemap_id'] for runk, rund in self.expfiledict.iteritems() if runk.startswith('run__') and 'platemap_id' in rund]
            self.FilterSmoothMapDict=generate_filtersmoothmapdict_mapids(platemapids)
            
        self.paramsdict_le_dflt['analysis_type'][1]=self.expfiledict['experiment_type']
        self.paramsdict_le_dflt['created_by'][1]=self.expfiledict['experiment_type']

        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            if k in ['analysis_type', 'created_by']:
                le.setText(dfltstr)
        self.clearanalysis(anadict=anadict)
        #rp=self.exppath.replace('.pck', '.exp')
        rp=os.path.split(self.exppath)[0]
        rp=compareprependpath(EXPFOLDERS_J+EXPFOLDERS_K, rp)
        self.anadict['experiment_path']=rp.replace(chr(92),chr(47))
        print 'active experiment_path is %s' %(self.anadict['experiment_path'])
        self.anadict['experiment_name']=self.expfiledict['name']
        self.fillexpoptions()
        self.expfilenameLineEdit.setText(self.exppath)
    def fillexpoptions(self):
        self.clearexp()
        
        self.runk_use=[(k, v['run_use'].partition('__')[0]) for k, v in self.expfiledict.iteritems() if k.startswith('run__')]
        self.uselist=list(set(map(operator.itemgetter(1), self.runk_use)))
        if 'data' in self.uselist:
            temp=self.uselist.pop(self.uselist.index('data'))
            self.uselist=[temp]+self.uselist
        
        for i, k in enumerate(self.uselist):
            self.ExpRunUseComboBox.insertItem(i, k)

        self.ExpRunUseComboBox.setCurrentIndex(0)
        
        self.fillruncheckboxes()
    
    def fillruncheckboxes(self):
        self.runselectionaction=False
        self.usek=str(self.ExpRunUseComboBox.currentText())
        runklist=[runk for runk, usek in self.runk_use if usek==self.usek]
        d=dict([('-'.join([runk, self.expfiledict[runk]['description'] if 'description' in self.expfiledict[runk].keys() else '']), dict([(k, v) for k, v in self.expfiledict[runk].iteritems() if not k.startswith('platemap')])) for runk in runklist])
        self.runtreeclass.filltree(d, startkey='')
        self.runtreeclass.maketoplevelchecked()
        self.filltechtyperadiobuttons()
        self.runselectionaction=True
    def runselectionchanged(self, item, column):
        if not self.runselectionaction:
            return

        if item.parent() is None:#top level run
            self.filltechtyperadiobuttons()
    
    def filltechtyperadiobuttons(self, startind=0):
        qlist=self.TechTypeButtonGroup.buttons()
        numbuttons=len(qlist)
        for button in qlist:
            button.setText('')
            button.setToolTip('')
            button.setVisible(False)
        self.selectrunklist=self.runtreeclass.getlistofchecktoplevelitems()
        self.selectrunklist=[s.partition('-')[0] for s in self.selectrunklist if len(s.partition('-')[0])>0]
        runk_techk=[(runk, techk)
           for runk in self.selectrunklist \
           for techk in self.expfiledict[runk].keys() \
              if techk.startswith('files_technique__')]
        
        self.techk_typek=list(set([(techk.partition('files_technique__')[2], typek) \
        for runk, techk in runk_techk \
        for typek in self.expfiledict[runk][techk].keys()]))
        
        numfiles=[\
            numpy.array([len(self.expfiledict[runk]['files_technique__'+techk][typek].keys()) \
                for runk in self.selectrunklist \
                if 'files_technique__'+techk in self.expfiledict[runk].keys() and typek in self.expfiledict[runk]['files_technique__'+techk].keys()]).sum(dtype='int32')
            for techk, typek in self.techk_typek]
        
        temp_t_t=self.techk_typek
        numcanlist=numbuttons
        displaystrs=[]
        if startind>0:
            numcanlist-=1
            temp_t_t=temp_t_t[startind:]
            numfiles=numfiles[startind:]
            displaystrs+=['Display 0-9']
        if len(temp_t_t)>numcanlist:
            numcanlist-=1
            temp_t_t=temp_t_t[:numcanlist]
            numfiles=numfiles[:numcanlist]
            displaystrs+=['Display %d-?' %(startind+numcanlist)]
        count=0
        for nfiles, techk_typek in zip(numfiles, self.techk_typek):
            button=qlist[count]
            s=','.join(techk_typek)
            button.setText(s)
            button.setToolTip('%d files' %(nfiles))
            button.setVisible(True)
            if count==0:
                button.setChecked(True)
                self.fillanalysistypes(button)
            count+=1
        for s in displaystrs:
            button=qlist[count]
            button.setText(s)
            button.setVisible(True)
            count+=1
            
    def fillanalysistypes(self, button):
        if button is None:
            button=self.TechTypeButtonGroup.buttons()[0]
            button.setChecked(True)
        s=str(button.text())
        if s.startswith('Display '):
            i=int(s.partition('Display ')[2].partition('-')[0])
            filltechtyperadiobuttons(startind=i)
            return
        self.techk, garb, self.typek=s.partition(',')
        nfiles_classes=[len(c.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist, anadict=self.anadict)) for i, c in enumerate(AnalysisClasses)]
        self.AnalysisClassInds=[i for i, nf in enumerate(nfiles_classes) if nf>0]
        self.AnalysisNamesComboBox.clear()
        self.AnalysisNamesComboBox.insertItem(0, '')
        for count, i in enumerate(self.AnalysisClassInds):
            self.AnalysisNamesComboBox.insertItem(count+1, AnalysisClasses[i].analysis_name+('(%d)' %nfiles_classes[i]))
            self.AnalysisNamesComboBox.setCurrentIndex(1)
            
        
        filternames=list(set([k for d in self.FilterSmoothMapDict.values() for k in d.keys()]))
        
        nfiles_classes=[len(c.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist, anadict=self.anadict)) for i, c in enumerate(FOMProcessClasses[:-1])]
        self.FOMProcessClassInds=[i for i, nf in enumerate(nfiles_classes) if nf>0]
        self.FOMProcessNamesComboBox.clear()
        self.FOMProcessNamesComboBox.insertItem(0, 'use analysis function')
        for count, i in enumerate(self.FOMProcessClassInds):
            self.FOMProcessNamesComboBox.insertItem(count+1, '%s(%s)' %(FOMProcessClasses[i].analysis_name, FOMProcessClasses[i].params['select_ana']))
        if len(FOMProcessClasses[-1].getapplicablefomfiles(self.anadict))>0 and len(filternames)>0:
            for filtername in filternames:
                self.FOMProcessClassInds+=[-1]#each filtername from a .pck file uses the same analysis class
                count+=1
                self.FOMProcessNamesComboBox.insertItem(count+1, '%s(%s)' %(filtername, FOMProcessClasses[-1].params['select_ana']))
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
            
        self.getactiveanalysisclass()
    
    def getactiveanalysisclass(self):
        procselind=int(self.FOMProcessNamesComboBox.currentIndex())
        if procselind>0:
            procclassind=self.FOMProcessClassInds[procselind-1]
            self.analysisclass=FOMProcessClasses[procclassind]
            if procclassind==-1:#filter from pck
                filtername=str(self.FOMProcessNamesComboBox.currentText()).partition('(')[0]#write the filter_path__runint while handy here to use later
                self.analysisclass.filter_path__runint=dict([(int(runk.partition('__')[2]), self.FilterSmoothMapDict[str(rund['platemap_id'])][filtername]) for runk, rund in self.expfiledict.iteritems() if runk.startswith('run__')])
                
                if '__' in filtername:
                    self.analysisclass.params['platemap_comp4plot_keylist']=','.join(list(filtername.partition('__')[2]))
                else:
                    self.analysisclass.params['platemap_comp4plot_keylist']=self.analysisclass.dfltparams['platemap_comp4plot_keylist']
        else:
            selind=int(self.AnalysisNamesComboBox.currentIndex())
            if selind==0:
                self.analysisclass=None
                return
            self.analysisclass=AnalysisClasses[self.AnalysisClassInds[selind-1]]
        #self.activeana=None
        
        le, dflt=self.paramsdict_le_dflt['description']
        s=filterchars(str(le.text()), valid_chars = "-_.; ()%s%s" % (string.ascii_letters, string.digits))
        if ';' in s:
            s=s.partition(';')[0]
            newdflt='; '.join([s, self.analysisclass.description])
        else:
            newdflt=self.analysisclass.description
        le.setText(newdflt)
        self.paramsdict_le_dflt['description'][1]=newdflt
        
    def clearexp(self):
        self.ExpRunUseComboBox.clear()
        self.RunSelectTreeWidget.clear()
        self.plotd={}
        self.expfilenameLineEdit.setText('')
    def runbatchprocess(self):
        self.batchprocesses[self.BatchComboBox.currentIndex()]()

    def importfrominfo(self):
        idialog=openfrominfoDialog(self, runtype='', exp=True, ana=False, run=False)
        idialog.exec_()
        if idialog.selecttype=='ana':
            self.importana(p=idialog.selectpath)
        if idialog.selecttype=='exp':
            self.importexp(exppath=idialog.selectpath)
    def importana(self, p=None):
        if p is None:
            p=selectexpanafile(self, exp=False, markstr='Select .ana/.pck to import, or .zip file')
        if len(p)==0:
            return
        anadict=readana(p, stringvalues=True, erroruifcn=None)#don't allow erroruifcn because dont' want to clear temp ana folder until exp successfully opened and then clearanalysis and then copy to temp folder, so need the path defintion to be exclusively in previous line
        print anadict.keys()
        if not 'experiment_path' in anadict.keys():
            return
#        if anadict['ana_version']!='3':
#            idialog=messageDialog(self, '.ana version %s is different from present. continue?' %anadict['ana_version'])
#            if not idialog.exec_():
#                return
        exppath=buildexppath(anadict['experiment_path'])#this is the place an experiment folder is turned into an exp fiel path so for the rest of this App exppath is the path of the .exp file
        expfiledict, expzipclass=readexpasdict(exppath, includerawdata=False, returnzipclass=True)
        if len(expfiledict)==0:
            idialog=messageDialog(self, 'abort .ana import because fail to open .exp')
            idialog.exec_()
            return
        self.importexp(expfiledict=expfiledict, exppath=exppath, expzipclass=expzipclass, anadict=anadict)#clearanalysis happens here and anadcit is ported into self.anadict in the clearanalysis
        #self.anadict=anadict
        if p.endswith('.ana') or p.endswith('.pck'):
            anafolder=os.path.split(p)[0]
        else:
            anafolder=p
    
        copyanafiles(anafolder, self.tempanafolder)
        self.updateana()
        print self.anadict.keys()

    def editanalysisparams(self):
        if self.analysisclass is None or len(self.analysisclass.params)==0:
            return
        keys_paramsd=[k for k, v in self.analysisclass.params.iteritems() if isinstance(v, dict)]
        if len(keys_paramsd)==0:
            self.editanalysisparams_paramsd(self.analysisclass.params)
            return
        else:
            keys_paramsd=['<non-nested params>']+keys_paramsd
        i=userselectcaller(self, options=keys_paramsd, title='Select type of parameter to edit')
        if i==0:
            self.editanalysisparams_paramsd(self.analysisclass.params)
        else:
            self.editanalysisparams_paramsd(self.analysisclass.params[keys_paramsd[i]])

    def editanalysisparams_paramsd(self, paramsd):
        inputs=[(k, type(v), (isinstance(v, str) and (v,) or (str(v),))[0]) for k, v in paramsd.iteritems() if not isinstance(v, dict)]
        if len(inputs)==0:
            return
        ans, changedbool=userinputcaller(self, inputs=inputs, title='Enter Calculation Parameters', returnchangedbool=True)
        somethingchanged=False
        for (k, tp, v), newv, chb in zip(inputs, ans, changedbool):
            if chb:
                paramsd[k]=newv
                somethingchanged=True
        if somethingchanged:#soem analysis classes have different files applicable depending on user-enter parameters so update here but don't bother deleting if numfiles goes to 0
            self.processeditedparams()
    def processeditedparams(self):
        self.analysisclass.processnewparams()
        nfiles=len(self.analysisclass.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist, anadict=self.anadict))
        if 'process_fom' in self.analysisclass.getgeneraltype():
            selind=int(self.FOMProcessNamesComboBox.currentIndex())
            self.FOMProcessNamesComboBox.setItemText(selind, '%s(%s)' %(str(self.FOMProcessNamesComboBox.currentText()).partition('(')[0], self.analysisclass.params['select_ana']))
        else:
            selind=int(self.AnalysisNamesComboBox.currentIndex())
            self.AnalysisNamesComboBox.setItemText(selind, self.analysisclass.analysis_name+('(%d)' %nfiles))
        self.getactiveanalysisclass()#this is only to update the description if necessary
        
    def gethighestanak(self, getnextone=False):
        kfcn=lambda i:'ana__%d' %i
        i=1
        while kfcn(i) in self.anadict.keys():
            i+=1
        if getnextone:
            anak=kfcn(i)
        else:
            anak=kfcn(i-1)
            if not anak in self.anadict.keys():
                return None
        return anak
    def analyzedata(self):
        if self.analysisclass is None:
            return
        
        checkbool, checkmsg=self.analysisclass.check_input()
        if not checkbool:
            if self.guimode:
                idialog=messageDialog(self, 'Continue analysis? '+checkmsg)
                if not idialog.exec_():
                    return
            else:
                return checkmsg
        #rawd=readbinaryarrasdict(keys)
        #expdatfolder=os.path.join(self.expfolder, 'raw_binary')
        expdatfolder=self.expfolder
        
        anak=self.gethighestanak(getnextone=True)
        #try:
        if 1:
            self.analysisclass.perform(self.tempanafolder, expdatfolder=expdatfolder, anak=anak, zipclass=self.expzipclass, expfiledict=self.expfiledict, anauserfomd=self.userfomd)
#        except:
#            idialog=messageDialog(self, 'Analysis Crashed. Nothing saved')
#            if not idialog.exec_():
#                removefiles(self.tempanafolder, [k for rund in \
#                   ([self.analysisclass.multirunfiledict]+self.analysisclass.runfiledict.items()) for typed in rund.items() for k in typed.keys()])
#                return
        runk_typek_b=self.analysisclass.prepareanafilestuples__runk_typek_multirunbool()
        killana=False
        if len(runk_typek_b)==0:
            killana=True
            checkmsg='no analysis output'
        else:
            checkbool, checkmsg=self.analysisclass.check_output()
            if not checkbool:
                if self.guimode:
                    idialog=messageDialog(self, 'Keep analysis? '+checkmsg)
                    if not idialog.exec_():
                        killana=True
                else:
                    killana=True
                if killana:
                    removefiles(self.tempanafolder, [k for d in \
                            ([self.analysisclass.multirunfiledict]+self.analysisclass.runfiledict.items()) for typed in d.values() for k in typed.keys()])
                
        if killana:
            return checkmsg#anadict not been modified yet
        
        self.updateuserfomd(clear=True)
        self.anadict[anak]={}
        
        self.activeana=self.anadict[anak]
        if not checkbool:
            self.activeana['check_output_message']=checkmsg
        for runk, typek, b in runk_typek_b:
            frunk='files_'+runk
            if not frunk in self.activeana.keys():
                self.activeana[frunk]={}
            if b:
                self.activeana[frunk][typek]=copy.deepcopy(self.analysisclass.multirunfiledict[typek])
            else:
                self.activeana[frunk][typek]=copy.deepcopy(self.analysisclass.runfiledict[runk][typek])
                
        self.activeana['name']=self.analysisclass.analysis_name
        self.activeana['analysis_fcn_version']=self.analysisclass.analysis_fcn_version
        
        self.activeana['plot_parameters']=self.analysisclass.plotparams
        plateidsliststr=','.join('%d' %i for i in sorted(list(set([d['plate_id'] for d in self.analysisclass.fomdlist]))))
        self.activeana['plate_ids']=plateidsliststr
        le, desc=self.paramsdict_le_dflt['description']
        s=str(le.text()).strip()
        if not (len(s)==0 or 'null' in s):
            desc=s
        desc+='; run '+','.join('%d' %i for i in sorted(list(set([d['runint'] for d in self.analysisclass.fomdlist]))))
        desc+='; plate_id '+plateidsliststr
        self.activeana['description']=desc
        le.setText('')#clear description to clear any user-entered comment
        if len(self.analysisclass.params)>0:
            self.activeana['parameters']={}
        for k, v in self.analysisclass.params.iteritems():
            if isinstance(v, dict):
                self.activeana['parameters'][k]={}
                for k2, v2 in v.iteritems():
                    self.activeana['parameters'][k][v2]=str(v2)
            else:
                self.activeana['parameters'][k]=str(v)
        
        #the A,B,C,D order is editable as a analysisclass paramete and if it is not the nontrivial case, bump it up to an ana__ key for ease in finding in visualization
        if 'parameters' in self.activeana.keys() and 'platemap_comp4plot_keylist' in self.activeana['parameters'].keys() and self.activeana['parameters']['platemap_comp4plot_keylist']!='A,B,C,D':
            self.activeana['platemap_comp4plot_keylist']=self.activeana['parameters']['platemap_comp4plot_keylist']

        gentype=self.analysisclass.getgeneraltype()
        if 'process_fom' in gentype:
            if 'from_file' in gentype:
                self.activeana['process_fom_from_file_paths']=','.join(sorted(list(set([compareprependpath(FOMPROCESSFOLDERS, p) for p in self.analysisclass.filter_path__runint.values()]))))
        else:
            self.activeana['technique']=self.techk
        self.activeana['analysis_general_type']=gentype


        self.fomdlist=self.analysisclass.fomdlist
        self.filedlist=self.analysisclass.filedlist
        self.fomnames=self.analysisclass.fomnames
        self.csvheaderdict=self.analysisclass.csvheaderdict
        self.primarycsvpath=self.analysisclass.primarycsvpath
        self.fomplotchoiceComboBox.clear()
        for count, s in enumerate(self.fomnames):
            self.fomplotchoiceComboBox.insertItem(count, s)
        self.fomplotchoiceComboBox.setCurrentIndex(0)
        
        self.stdcsvplotchoiceComboBox.clear()
        if 'plot_parameters' in self.csvheaderdict.keys() and 'plot__1' in self.csvheaderdict['plot_parameters'].keys():
            keys=sorted([k for k in self.csvheaderdict['plot_parameters'].keys() if k.startswith('plot__')])
            for count, s in enumerate(keys):
                self.stdcsvplotchoiceComboBox.insertItem(count, s)
            if len(keys)==0:
                count=-1
                newk='new plot__1'
            else:
                newk='new plot__%d' %(int(keys[-1].partition('__')[2])+1)
            self.stdcsvplotchoiceComboBox.insertItem(count+1, newk)
        self.stdcsvplotchoiceComboBox.setCurrentIndex(0)
        
        self.updateana()
        self.plot_preparestandardplot(plotbool=False)
        if self.autoplotCheckBox.isChecked():
            self.plot_generatedata(plotbool=True)
        return False#false means no error

        
    def updateana(self):
        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            s=str(le.text()).strip()
            if len(s)==0:
                s=dfltstr
            self.anadict[k]=s#this makes description just the last ana__ description
        
        
        #plateids=sorted(list(set(['%d' %rund['parameters']['plate_id'] for rund in [v for k, v in self.expfiledict.iteritems() if k.startswith('run__')]]))) #this old way of getting plate_ids will include plates for which analysis was not done
        
        ananames=sorted(list(set([anad['name'] for anad in [v for k, v in self.anadict.iteritems() if k.startswith('ana__')]])))
        plateidsstrlist_list=[anad['plate_ids'] for anad in [v for k, v in self.anadict.iteritems() if k.startswith('ana__')] if 'plate_ids' in anad.keys()]
        plateidsstrlist=sorted(list(set([idstr for liststr in plateidsstrlist_list for idstr in liststr.split(',')])))
        plateidsstr=','.join(plateidsstrlist)
        #self.anadict['plate_ids']=plateidsstr
        
        self.anadict['description']='%s on plate_id %s' %(', '.join(ananames), plateidsstr)
        self.AnaTreeWidgetFcns.filltree(self.anadict)
        
        self.fillanalysistypes(self.TechTypeButtonGroup.checkedButton())
        
    def viewresult(self, anasavefolder=None, show=True):
        if anasavefolder is None:
            anasavefolder=self.tempanafolder
        d=copy.deepcopy(self.anadict)
        convertfilekeystofiled(d)
        #importfomintoanadict(d)
        self.parent.visdataui.importana(anafiledict=d, anafolder=anasavefolder)
        if show:
            self.hide()
            self.parent.visdataui.show()
    def saveview(self):
        anasavefolder=self.saveana(dontclearyet=True)
        self.viewresult(anasavefolder=anasavefolder)#just hide+show so shouldn't get hung here
        self.importexp(expfiledict=self.expfiledict, exppath=self.exppath)

    def clearsingleanalysis(self):
        keys=sorted([k for k in self.anadict.keys() if k.startswith('ana__')])
        if len(keys)==0:
            return
        i=userselectcaller(self, options=keys, title='select ana__ to delete')
        if i is None:
            return
        if len(keys)==1:
            self.clearanalysis()
            return
        anad=self.anadict[keys[i]]
        fnlist=[fn for d in [v for k, v in anad.iteritems() if k.startswith('files_') and isinstance(v, dict)] for d2 in d.itervalues() for fn in d2.keys()]
        removefiles(self.tempanafolder, fnlist)
        
        if i<(len(keys)-1):
            for ki, knext in zip(keys[i:-1], keys[i+1:]):
                self.anadict[ki]=self.anadict[knext]
        del self.anadict[keys[-1]]
        self.activeana=None
        self.updateana()
        
    def clearanalysis(self, anadict=None):
        self.analysisclass=None
        self.activeana=None
        self.anadict={}
        
        self.paramsdict_le_dflt['description'][1]='null'
        
        if not anadict is None:
            for k, v in anadict.iteritems():
                self.anadict[k]=v
            if 'description' in anadict.keys():
                self.paramsdict_le_dflt['description'][1]=anadict['description']
                
        self.anadict['ana_version']='3'
        
        

        self.AnaTreeWidget.clear()
        
        
        if os.path.isdir(self.tempanafolder):
            for fn in os.listdir(self.tempanafolder):
                os.remove(os.path.join(self.tempanafolder, fn))
        else:
            self.tempanafolder=getanadefaultfolder(erroruifcn=lambda s:mygetdir(parent=self, markstr='select ANA default folder - to meet compliance this should be format %Y%m%d.%H%M%S.incomplete'))
            #this is meant to result in rund['name']=%Y%m%d.%H%M%S but doesn't guarantee it
            timestr=(os.path.split(self.tempanafolder)[1]).rstrip('.incomplete')
            self.AnaNameLineEdit.setText(timestr)
            self.paramsdict_le_dflt['name'][1]=timestr
    def importanalysisparams(self):
        return


 
    def saveana(self, dontclearyet=False, anatype=None, rundone=None):
        self.anafilestr=self.AnaTreeWidgetFcns.createtxt()
        if not 'ana_version' in self.anafilestr:
            idialog=messageDialog(self, 'Aborting SAVE because no data in ANA')
            idialog.exec_()
            return
        if anatype is None:
            savefolder=None
            idialog=SaveOptionsDialog(self, self.anadict['analysis_type'])
            idialog.exec_()
            if not idialog.choice:
                return
            anatype=idialog.choice
            if idialog.choice=='browse':
                savefolder=mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Select folder for saving ANA')
                if savefolder is None or len(savefolder)==0:
                    return
                rundone=''#rundone not used if user browses for folder
        else:
            savefolder=None
            
        if len(self.anafilestr)==0 or not 'ana_version' in self.anafilestr:
            return

        if rundone is None:
            idialog=messageDialog(self, 'save as .done ?')
            if idialog.exec_():
                rundone='.done'
            else:
                rundone='.run'

        anasavefolder=saveana_tempfolder(self.anafilestr, self.tempanafolder, analysis_type=anatype, anadict=self.anadict, savefolder=savefolder, rundone=rundone, erroruifcn=\
            lambda s:mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s, select folder for saving ANA'))
        
        if not dontclearyet:
            self.importexp(expfiledict=self.expfiledict, exppath=self.exppath)#clear analysis happens here but exp_path wont' be lost
        #self.clearanalysis()
        return anasavefolder
    def editvisparams(self):
        if self.activeana is None:
            print 'active ana__ has been lost so nothing done.'
            return
        k=str(self.stdcsvplotchoiceComboBox.currentText())
        if not k in self.csvheaderdict['plot_parameters'].keys():
           k=k.partition('new ')[2]
           self.csvheaderdict['plot_parameters'][k]={}
        d=self.csvheaderdict['plot_parameters'][k]
        d['fom_name']=str(self.fomplotchoiceComboBox.currentText())
        for k, le in [('colormap', self.colormapLineEdit), ('colormap_over_color', self.aboverangecolLineEdit), ('colormap_under_color', self.belowrangecolLineEdit)]:
            if len(str(le.text()).strip())==0:
                continue
            v=str(le.text()).strip()
            if '_color' in k and v in colors.ColorConverter.colors.keys():
                v=str(colors.ColorConverter.colors[v])
            elif '_color' in k and not '(' in v:#kinda require the color values to be (r,g,b)
                continue
            d[k]=v.replace(' ', '')
        s=str(self.vminmaxLineEdit.text())
        if ',' in s:
            a, temp, b=s.partition(',')
            if len(a.strip())>0:
                d['colormap_min_value']=a.strip()
            if len(b.strip())>0:
                d['colormap_max_value']=b.strip()
        totnumheadlines=writecsv_smpfomd(self.primarycsvpath, '', headerdict=self.csvheaderdict, replaceheader=True)
        fnf=os.path.split(self.primarycsvpath)[1]
        files_techd=self.activeana['files_multi_run']
        files_fomd=files_techd['fom_files']
        s=files_fomd[fnf]
        l=s.split(';')
        l[2]='%d' %(totnumheadlines)
        files_fomd[fnf]=';'.join(l)
        self.updateana()
        
    def plot_preparestandardplot(self, plotbool=True):
        k=str(self.stdcsvplotchoiceComboBox.currentText())
        if not k in self.csvheaderdict['plot_parameters'].keys():
           return
        d=self.csvheaderdict['plot_parameters'][k]
        if not 'fom_name' in d.keys() or not d['fom_name'] in self.fomnames:
            return
        self.fomplotchoiceComboBox.setCurrentIndex(self.fomnames.index(d['fom_name']))
        for k, le in [('colormap', self.colormapLineEdit), ('colormap_over_color', self.aboverangecolLineEdit), ('colormap_under_color', self.belowrangecolLineEdit)]:
            if not k in d.keys():
                continue
            le.setText(d[k])
        if 'colormap_min_value' in d.keys() and 'colormap_max_value' in d.keys():
            self.vminmaxLineEdit.setText('%s,%s' %(d['colormap_min_value'], d['colormap_max_value']))
        if plotbool:
            self.plot_generatedata(plotbool=True)

    def plot_generatedata(self, plotbool=True):
        self.plotd={}
        if len(self.fomdlist)==0:
            return
        fi=self.fomplotchoiceComboBox.currentIndex()
        fom=numpy.array([d[self.fomnames[fi]] for d in self.fomdlist])
        runkarr=numpy.array(['run__%d' %(d['runint']) for d in self.fomdlist])
        if 'expkeys' in self.filedlist[0].keys():#generally standard analysis class
            #runkarr=numpy.array([d['expkeys'][0] for d in self.filedlist])
            daqtimebool=self.usedaqtimeCheckBox.isChecked()
        else:#generally Process FOM
            daqtimebool=False
            
        # inds are inds from  self.fomdlist, not all of which are used because some are NaN
        fomdlistinds=numpy.where(numpy.logical_not(numpy.isnan(fom)))[0]
        if len(fomdlistinds)==0:
            print 'ABORTING PLOTTING BECAUSE ALL FOMs ARE NaN'
            return
        #here the fom and runkarr and sample arrays are setup 
        fom=fom[fomdlistinds]
        runkarr=runkarr[fomdlistinds]
        sample=numpy.array([self.fomdlist[i]['sample_no'] for i in fomdlistinds])
        #and now this is a dictionary that given a runk looks ups the inds from the above arrays, i.e. these inds are inds of the selction from fomdlist, NOT from fomdlist
        inds_runk=dict([(runk, numpy.where(runkarr==runk)[0]) for runk in list(set(runkarr))])
        

        t=[]
#        else:
#            hx=numpy.arange(len(fom))

        #remapinds=[i for runk in sorted(inds_runk.keys()) for i in inds_runk[runk]]
        
        if daqtimebool:
            t=numpy.zeros(len(fom), dtype='float64')
            for runk in sorted(inds_runk.keys()):
                fns=[self.filedlist[fomdlistinds[i]]['expkeys'][-1] for i in inds_runk[runk]]#reduce(dict.get, ['x','q','w'], d)
                t[inds_runk[runk]]=applyfcn_txtfnlist_run(gettimefromheader, self.expfiledict[runk]['run_path'], fns)
            t=numpy.array(t)
            t-=t.min()
#        else:
#            hx=numpy.array(sample)
        
        compplottype=str(self.CompPlotTypeComboBox.currentText())
        
        nanxy=[numpy.nan]*2
        nancomp=[numpy.nan]*4
        xy=numpy.ones((len(fom), 2), dtype='float64')*numpy.nan
        comps=numpy.ones((len(fom), 4), dtype='float64')*numpy.nan
        for runk in sorted(inds_runk.keys()):
            if not 'platemapdlist' in self.expfiledict[runk].keys() or len(self.expfiledict[runk]['platemapdlist'])==0:
#                if not compplottype=='none':
#                    comps+=[nancomp]*len(inds_runk[runk])
#                xy+=[nanxy]*len(inds_runk[runk])
                continue
            pmsmps=[d['Sample'] for d in self.expfiledict[runk]['platemapdlist']]
            xy[inds_runk[runk]]=numpy.float64([ \
                         [self.expfiledict[runk]['platemapdlist'][pmsmps.index(smp)][k] for k in ['x', 'y']] \
                         if smp in pmsmps else nanxy for smp in sample[inds_runk[runk]]])
                         
            if compplottype=='none':
                continue
                
            comps[inds_runk[runk]]=numpy.float64([\
                     [self.expfiledict[runk]['platemapdlist'][pmsmps.index(smp)][k] for k in ['A', 'B', 'C', 'D']] \
                     if smp in pmsmps else nancomp for smp in sample[inds_runk[runk]]])
#        xy=numpy.float64(xy)
#        comps=numpy.float64(comps)
        
        self.plotd['comps']=numpy.array([c/c.sum() for c in comps])
        self.plotd['xy']=xy
        self.plotd['fom']=fom
        self.plotd['inds_runk']=inds_runk
        self.plotd['t']=t
        self.plotd['sample_no']=sample
        self.plotd['fomname']=self.fomnames[fi]
        if plotbool:
            self.plot()
    def plotwithcaution(self):
        try:
            self.plot()
        except:
            print 'ERROR UPDATING PLOTS. Porbably data not setup, try selecting a standard plot'
    def plot(self):
        if len(self.plotd)==0:
            return

        self.plotw_comp.axes.cla()
        self.plotw_quat3d.axes.cla()
        self.plotw_plate.axes.cla()
        self.plotw_h.axes.cla()
        self.cbax_quat.cla()
        self.cbax_plate.cla()

        if len(self.plotd['fom'])==0:
            return

        x, y=self.plotd['xy'].T
        comps=self.plotd['comps']
        fom=self.plotd['fom']
        
        #h plot
        daqtimebool=self.usedaqtimeCheckBox.isChecked()
        if daqtimebool:
            hxarr=self.plotd['t']
            xl='time (s)'
        else:
            hxarr=self.plotd['sample_no']
            xl='sample_no'
        for runk in sorted(self.plotd['inds_runk'].keys()):
            hx=hxarr[self.plotd['inds_runk'][runk]]
            hy=fom[self.plotd['inds_runk'][runk]]
            sinds=numpy.argsort(hx)
            self.plotw_h.axes.plot(hx[sinds], hy[sinds], '.-', label=runk)
        leg=self.plotw_h.axes.legend(loc=0)
        leg.draggable()
        self.plotw_h.axes.set_xlabel(xl)
        self.plotw_h.axes.set_ylabel(self.plotd['fomname'])
        autotickformat(self.plotw_h.axes, x=daqtimebool, y=1)
        self.plotw_h.fig.canvas.draw()
        
        #plate plot
        cmapstr=str(self.colormapLineEdit.text())
        try:
            cmap=eval('cm.'+cmapstr)
        except:
            cmap=cm.jet

        clip=True
        skipoutofrange=[False, False]
        self.vmin=fom.min()
        self.vmax=fom.max()
        vstr=str(self.vminmaxLineEdit.text()).strip()
        if ',' in vstr:
            a, b, c=vstr.partition(',')
            try:
                a=myeval(a.strip())
                c=myeval(c.strip())
                self.vmin=a
                self.vmax=c
                for count, (fcn, le) in enumerate(zip([cmap.set_under, cmap.set_over], [self.belowrangecolLineEdit, self.aboverangecolLineEdit])):
                    vstr=str(le.text()).strip()
                    vstr=vstr.replace('"', '').replace("'", "")
                    if 'none' in vstr or 'None' in vstr:
                        skipoutofrange[count]=True
                        continue
                    if len(vstr)==0:
                        continue
                    c=col_string(vstr)
                    try:
                        fcn(c)
                        clip=False
                    except:
                        print 'color entry not understood:', vstr

            except:
                pass

        
        norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
        if skipoutofrange[0]:
            inds=numpy.where(fom>=self.vmin)
            fom=fom[inds]
            comps=comps[inds]
            x=x[inds]
            y=y[inds]

        if skipoutofrange[1]:
            inds=numpy.where(fom<=self.vmax)
            fom=fom[inds]
            comps=comps[inds]
            x=x[inds]
            y=y[inds]

        if numpy.any(fom>self.vmax):
            if numpy.any(fom<self.vmin):
                extend='both'
            else:
                extend='max'
        elif numpy.any(fom<self.vmin):
            extend='min'
        else:
            extend='neither'
        
        pointsizestr=str(self.compplotsizeLineEdit.text())
        
        m=self.plotw_plate.axes.scatter(x, y, c=fom, s=20, marker='s', edgecolor='none', cmap=cmap, norm=norm)
        if x.max()-x.min()<2. or y.max()-y.min()<2.:
            self.plotw_plate.axes.set_xlim(x.min()-1, x.max()+1)
            self.plotw_plate.axes.set_ylim(y.min()-1, y.max()+1)
        else:
            self.plotw_plate.axes.set_aspect(1.)

        sm=cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array(fom)
        cols=numpy.float32(map(sm.to_rgba, fom))[:, :3]#ignore alpha
        
        cb=self.plotw_plate.fig.colorbar(sm, cax=self.cbax_plate, extend=extend, format=autocolorbarformat((self.vmin, self.vmax)))
        cb.set_label(self.plotd['fomname'])
        self.plotw_plate.fig.canvas.draw()
        
        
        #comp plot
        compsinds=[i for i, (compv, colv) in enumerate(zip(comps, cols)) if not (numpy.any(numpy.isnan(compv)) or numpy.any(numpy.isnan(colv)))]
        if len(compsinds)==0:
            return
        self.quatcompclass.loadplotdata(comps[compsinds], cols[compsinds])
        plotw3dbool=self.quatcompclass.plot()
        if not plotw3dbool is None:
            if plotw3dbool:
                self.plotw_comp.hide()
                self.plotw_quat3d.show()
                self.plotw_quat3d.axes.set_axis_off()
                cb=self.plotw_quat3d.fig.colorbar(sm, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((self.vmin, self.vmax)))
                self.plotw_quat3d.fig.canvas.draw()
            else:
                self.plotw_quat3d.hide()
                self.plotw_comp.show()
                cb=self.plotw_comp.fig.colorbar(sm, cax=self.quatcompclass.cbax, extend=extend, format=autocolorbarformat((self.vmin, self.vmax)))
                self.plotw_comp.fig.canvas.draw()
            cb.set_label(self.plotd['fomname'])
#        comps=numpy.array([c[:4]/c[:4].sum() for c in comps])
#        i=self.ternskipComboBox.currentIndex()
#        inds=[j for j in range(4) if j!=i][:3]
#        terncomps=numpy.array([c[inds]/c[inds].sum() for c in comps])
#        reordercomps=comps[:, inds+[i]]
#        self.ellabels=self.techniquedictlist[0]['elements']
#        reorderlabels=[self.ellabels[j] for j in inds+[i]]


#        quat=QuaternaryPlot(self.plotw_quat3d.axes, ellabels=self.ellabels, offset=0)
#        quat.label()
#        quat.scatter(comps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
#        cb=self.plotw_quat3d.fig.colorbar(quat.mappable, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))

#        fomlabel=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText()), self.filterfomstr))
#        self.stackedternplotdict=dict([('comps', reordercomps), ('fom', fom), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel)])
#        
#        pointsizestr=str(self.compplotsizeLineEdit.text())
#        tern=TernaryPlot(self.plotw_comp.axes, ellabels=reorderlabels[:3], offset=0)
#        tern.label()
#        tern.scatter(terncomps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
#        cb=self.plotw_comp.fig.colorbar(tern.mappable, cax=self.cbax_comp, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
#
#
#
#        #self.plotw_quat3d.axes.mouse_init()
#        self.plotw_quat3d.axes.set_axis_off()
#        self.plotw_comp.fig.canvas.draw()
#        self.plotw_quat3d.fig.canvas.draw()

        #self.selectind=-1
        #self.plotselect()
        


    def plateclickprocess(self, coords_button):
        if len(self.techniquedictlist)==0:
            return
#        critdist=3.
#        xc, yc, button=coords_button
#        x=getarrfromkey(self.techniquedictlist, 'x')
#        y=getarrfromkey(self.techniquedictlist, 'y')
#        dist=((x-xc)**2+(y-yc)**2)**.5
#        if min(dist)<critdist:
#            self.selectind=numpy.argmin(dist)
#            self.plotselect()
#        if button==3:
#            self.addtoselectsamples([self.techniquedictlist[self.selectind]['Sample']])
#    def selectbelow(self):
#        try:
#            vmin, vmax=(self.vmin, self.vmax)
#        except:
#            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
#        idlist=[]
#        for d in self.techniquedictlist:
#            if d['FOM']<vmin:
#                idlist+=[d['Sample']]
#        if len(idlist)>0:
#            self.addtoselectsamples(idlist)

    def plotwsetup(self):
        
        self.plotw_comp=plotwidget(self)
        self.plotw_quat3d=plotwidget(self, projection3d=True)
        self.plotw_h=plotwidget(self)
        self.plotw_plate=plotwidget(self)
        

        for b, w in [\
            (self.textBrowser_plate, self.plotw_plate), \
            (self.textBrowser_h, self.plotw_h), \
            (self.textBrowser_comp, self.plotw_comp), \
            (self.textBrowser_comp, self.plotw_quat3d), \
            ]:
            w.setGeometry(b.geometry())
            b.hide()
        self.plotw_quat3d.hide()

        self.plotw_plate.axes.set_aspect(1)

        axrect=[0.88, 0.1, 0.04, 0.8]

        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_plate=self.plotw_plate.fig.add_axes(axrect)

        self.plotw_quat3d.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_quat=self.plotw_quat3d.fig.add_axes(axrect)

        self.plotw_h.fig.subplots_adjust(left=.22, bottom=.17)
        
        self.quatcompclass=quatcompplotoptions(self.plotw_comp, self.CompPlotTypeComboBox, plotw3d=self.plotw_quat3d, plotwcbaxrect=axrect)
    
    def batch_processallana(self):
        if int(self.FOMProcessNamesComboBox.currentIndex())==0:
            print 'quitting batch process because use analysis function was selected instead of a FOM process'
            return
        selprocesslabel=str(self.FOMProcessNamesComboBox.currentText()).partition('(')[0]
        presentanakeys=sorted([k for k, v in self.anadict.iteritems() if k.startswith('ana__')])
        for anak in presentanakeys:
            self.analysisclass.params['select_ana']=anak
            self.processeditedparams()#self.getactiveanalysisclass() run in here
            self.analyzedata()
            matchbool=False
            for i in range(1, int(self.FOMProcessNamesComboBox.count())):
                matchbool=(str(self.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])==selprocesslabel
                if matchbool:
                    break
            if not matchbool:
                print 'skipping %s, probably because no appropriate fom_files found' %anak
            self.FOMProcessNamesComboBox.setCurrentIndex(i)
            self.getactiveanalysisclass()
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
    
    def batch_analyzethenprocess(self):
        if int(self.FOMProcessNamesComboBox.currentIndex())==0:
            print 'quitting batch process because use analysis function was selected instead of a FOM process'
            return
        selprocesslabel=str(self.FOMProcessNamesComboBox.currentText()).partition('(')[0]
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        self.getactiveanalysisclass()
        anak=self.gethighestanak(getnextone=True)
        self.analyzedata()
        if anak!=self.gethighestanak(getnextone=False):
            print 'quitting batch process because analysis function did not successfully run'
            return 

        
        matchbool=False
        for i in range(1, int(self.FOMProcessNamesComboBox.count())):
            matchbool=(str(self.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])==selprocesslabel
            if matchbool:
                break
        if not matchbool:
            print 'skipping %s, probably because no appropriate fom_files found' %anak
        self.FOMProcessNamesComboBox.setCurrentIndex(i)
        self.getactiveanalysisclass()
        self.analysisclass.params['select_ana']=anak
        self.processeditedparams()#self.getactiveanalysisclass() run in here
        self.analyzedata()
        
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        
    def batch_analyzethenprocess_allsubspace(self):
        if int(self.FOMProcessNamesComboBox.currentIndex())==0:
            print 'quitting batch process because use analysis function was selected instead of a FOM process'
            return
        selprocesslabel_original=str(self.FOMProcessNamesComboBox.currentText()).partition('(')[0]
        selprocess_root=selprocesslabel_original.partition('__')[0]
        if len(selprocess_root)==0:
            print 'quitting batch process because FOM process function not iterable (must be "<root>__<indexstr>")'
            return
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        self.getactiveanalysisclass()
        anak=self.gethighestanak(getnextone=True)
        self.analyzedata()
        if anak!=self.gethighestanak(getnextone=False):
            print 'quitting batch process because analysis function did not successfully run'
            return 

        
        selprocesslabel_list=[str(self.FOMProcessNamesComboBox.itemText(i)).partition('(')[0] for i in range(1, int(self.FOMProcessNamesComboBox.count())) if (str(self.FOMProcessNamesComboBox.itemText(i)).partition('__')[0])==selprocess_root]
        for selprocesslabel in selprocesslabel_list:
            matchbool=False
            for i in range(1, int(self.FOMProcessNamesComboBox.count())):
                matchbool=(str(self.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])==selprocesslabel
                if matchbool:
                    break
            if not matchbool:
                print 'skipping %s, probably because no appropriate fom_files found' %anak
            self.FOMProcessNamesComboBox.setCurrentIndex(i)
            self.getactiveanalysisclass()
            self.analysisclass.params['select_ana']=anak
            self.processeditedparams()#self.getactiveanalysisclass() run in here
            anak_processed=self.gethighestanak(getnextone=True)
            self.analyzedata()
            if anak_processed!=self.gethighestanak(getnextone=False):
                print 'quitting batch process because processing function did not successfully run'
                return 
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        
        #user would prompt running of editanalysisparams_paramsd at this point but skip this since only updates the label
        
        
    def batch_process_allsubspace(self):
        anak=self.gethighestanak(getnextone=False)
        selprocesslabel_original=str(self.FOMProcessNamesComboBox.currentText()).partition('(')[0]
        selprocess_root=selprocesslabel_original.partition('__')[0]
        if len(selprocess_root)==0:
            print 'quitting batch process because FOM process function not iterable (must be "<root>__<indexstr>")'
            return
            
        selprocesslabel_list=[str(self.FOMProcessNamesComboBox.itemText(i)).partition('(')[0] for i in range(1, int(self.FOMProcessNamesComboBox.count())) if (str(self.FOMProcessNamesComboBox.itemText(i)).partition('__')[0])==selprocess_root]
        for selprocesslabel in selprocesslabel_list:
            matchbool=False
            for i in range(1, int(self.FOMProcessNamesComboBox.count())):
                matchbool=(str(self.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])==selprocesslabel
                if matchbool:
                    break
            if not matchbool:
                print 'skipping %s, probably because no appropriate fom_files found' %anak
            self.FOMProcessNamesComboBox.setCurrentIndex(i)
            self.getactiveanalysisclass()
            self.analysisclass.params['select_ana']=anak
            self.processeditedparams()#self.getactiveanalysisclass() run in here
            anak_processed=self.gethighestanak(getnextone=True)
            self.analyzedata()
            if anak_processed!=self.gethighestanak(getnextone=False):
                print 'quitting batch process because processing function did not successfully run'
                return 
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
    
    def batch_analyze_fcn_same_techclass(self):
        #uses the presently-selected analysis name, file type and 1st 2 characters of techniuqe to run the analysis on all  tech,type that match
        anname=self.analysisclass.analysis_name
        
        buttonstrings=[','.join([techv, typev]) for techv, typev in self.techk_typek if techv[:2]==self.techk[:2] and typev==self.typek]
        for buttonstr in buttonstrings:
            qlist=self.TechTypeButtonGroup.buttons()
        
            typetechfound=False
            for button in qlist:
                if str(button.text()).strip()==buttonstr:
                    button.setChecked(True)
                    typetechfound=True
                    break
            if not typetechfound:
                print 'Skipped %s because could find it in the options list' %buttonstr
                continue
            self.fillanalysistypes(self.TechTypeButtonGroup.checkedButton())
            

            cb=self.AnalysisNamesComboBox
            selind=[i for i in range(int(cb.count())) if str(cb.itemText(i)).startswith(anname)]
            if len(selind)==0:
                print 'Skipped %s because the analysis option was not available' %buttonstr
                continue
            cb.setCurrentIndex(selind[0])
            self.getactiveanalysisclass()
            self.analyzedata()

        
class treeclass_anadict():
    def __init__(self, tree):
        self.treeWidget=tree
        self.treeWidget.clear()
    
    def getlistofchecktoplevelitems(self):
        return [str(self.treeWidget.topLevelItem(count).text(0)).strip().strip(':') for count in range(int(self.treeWidget.topLevelItemCount()))\
            if bool(self.treeWidget.topLevelItem(count).checkState(0))]
    def maketoplevelchecked(self):
        for count in range(int(self.treeWidget.topLevelItemCount())):
            item=self.treeWidget.topLevelItem(count)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
    def filltree(self, d, startkey='ana_version', laststartswith='ana__'):
        self.treeWidget.clear()
        #assume startkey is not for dict and laststatswith is dict
        
        if len(startkey)>0:
            mainitem=QTreeWidgetItem([': '.join([startkey, d[startkey]])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
            self.treeWidget.setCurrentItem(mainitem)
        
        for k in sorted([k for k, v in d.iteritems() if k!=startkey and not isinstance(v, dict)]):
            mainitem=QTreeWidgetItem([': '.join([k, str(d[k])])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
            
        for k in sorted([k for k, v in d.iteritems() if not k.startswith(laststartswith) and isinstance(v, dict)]):
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
            
        anakl=sorted([k for k in d.keys() if k.startswith(laststartswith)])
        for k in anakl:
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
    def nestedfill(self, d, parentitem, laststartswith='files_'):
        nondictkeys=sorted([k for k, v in d.iteritems() if not isinstance(v, dict)])
        for k in nondictkeys:
            item=QTreeWidgetItem([': '.join([k, str(d[k])])], 0)
            parentitem.addChild(item)
        dictkeys1=sorted([k for k, v in d.iteritems() if not k.startswith(laststartswith) and isinstance(v, dict)])
        for k in dictkeys1:
            item=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], item)
            parentitem.addChild(item)
        dictkeys2=sorted([k for k in d.keys() if k.startswith(laststartswith)])
        for k in dictkeys2:
            item=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], item)
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



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', **kwargs)
            #self.calcui.importexp(exppath=r'K:\processes\experiment\temp\20160221.123408.run\20160221.123408.exp')
            #self.calcui.importexp(exppath=r'K:\processes\experiment\temp\20160218.162704.run\20160218.162704.exp')
            #TRdata:
            #self.calcui.importexp(exppath=r'K:\processes\experiment\temp\20160222.104337.run\20160222.104337.exp')
            #self.calcui.analyzedata()
            #self.calcui.importana(p=r'K:\processes\analysis\temp\20160609.121710.done\20160609.121710.ana')
            #self.calcui.analyzedata()\\htejcap.caltech.edu\share\home\processes\experiment\temp\20160609.162218.done\20160609.162218.pck
            if execute:
                self.calcui.exec_()
    #os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
#form.calcui.expfiledict
