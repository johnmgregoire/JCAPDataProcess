import time
import os, os.path, shutil
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
from CalcFOMForm import Ui_CalcFOMDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'


sys.path.append(os.path.join(os.getcwd(),'AnalysisFunctions'))
from CA_CP_basics import *

AnalysisClasses=[Analysis__Ifin(), Analysis__Iave(), Analysis__Iphoto()]

DEBUGMODE=True

for ac in AnalysisClasses:
    ac.debugmode=DEBUGMODE

class calcfomDialog(QDialog, Ui_CalcFOMDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(calcfomDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
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
        (self.EditAnalysisParamsPushButton, self.editanalysisparams), \
        (self.AnalyzeDataPushButton, self.analyzedata), \
        (self.ViewResultPushButton, self.viewresult), \
        (self.EditDfltVisPushButton, self.editvisparams), \
        (self.SaveAnaPushButton, self.saveana), \
        (self.ClearAnalysisPushButton, self.clearanalysis), \
        (self.ClearSingleAnalysisPushButton, self.clearsingleanalysis), \
        (self.ImportAnalysisParamsPushButton, self.importanalysisparams), \

        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        self.runcheckboxlist=[\
        self.RunCheckBox_0, self.RunCheckBox_1, self.RunCheckBox_2, \
        self.RunCheckBox_3, self.RunCheckBox_4, self.RunCheckBox_5, \
        self.RunCheckBox_6, self.RunCheckBox_7]
        for cb in self.runcheckboxlist:
            QObject.connect(cb, SIGNAL("toggled(bool)"), self.filltechtyperadiobuttons)
        
        QObject.connect(self.ExpRunUseComboBox,SIGNAL("activated(QString)"),self.fillruncheckboxes)
        
        #QObject.connect(self.TechTypeButtonGroup,SIGNAL("buttonClicked(QAbstractButton)"),self.fillanalysistypes)
        self.TechTypeButtonGroup.buttonClicked[QAbstractButton].connect(self.fillanalysistypes)
        
        QObject.connect(self.AnalysisNamesComboBox,SIGNAL("activated(QString)"),self.getactiveanalysisclass)
        QObject.connect(self.fomplotchoiceComboBox,SIGNAL("activated(QString)"),self.plot_generatedata)
        QObject.connect(self.CompPlotTypeComboBox,SIGNAL("activated(QString)"),self.plot_generatedata)
        QObject.connect(self.stdcsvplotchoiceComboBox,SIGNAL("activated(QString)"),self.plot_preparestandardplot)
        QObject.connect(self.usedaqtimeCheckBox,SIGNAL("stateChanged()"),self.plot_generatedata)
        
        QObject.connect(self.AnaTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem)
        
        self.paramsdict_le_dflt=dict([\
         ('access', [self.AccessLineEdit, 'hte']), \
         ('name', [self.AnaNameLineEdit, 'temp_eche_name']), \
         ('ana_type', [self.AnaTypeLineEdit, 'eche']), \
         ('created_by', [self.UserNameLineEdit, 'eche']), \
         ('description', [self.AnaDescLineEdit, 'null']), \
        ])
        
        self.tempanafolder=getanadefaultfolder(erroruifcn=lambda s:mygetdir(parent=self, markstr='select ANA default folder'))
        self.AnaTreeWidgetFcns=treeclass_anadict(self.AnaTreeWidget)
        self.exppath='null'
        self.clearanalysis()

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
            kl=[str(item.text(0)).partition(':')[0].strip()]+kl
            item=item.parent()
        d=self.anadict
        while len(kl)>1:
            d=d[kl.pop(0)]
        d[kl[0]]=ans
        
    def importexp(self, expfiledict=None, exppath=None):
        if expfiledict is None:
            #TODO: define default path
            #exppath='exp/sampleexp_uvis.dat'
            exppath=mygetopenfile(self, xpath=os.path.join(os.getcwd(), 'experiment'), markstr='Select .pck or .exp EXP file', filename='.pck' )
            if len(exppath)==0:
                return
            expfiledict=readexpasdict(exppath, includerawdata=False, erroruifcn=None)
            if expfiledict is None:
                print 'Problem opening EXP'
                return
        self.clearexp()
        self.exppath=exppath
        self.expfolder=os.path.split(exppath)[0]
        self.expfiledict=expfiledict
        if self.getplatemapCheckBox.isChecked():
           for runk, rund in self.expfiledict.iteritems():
                if runk.startswith('run__') and not 'platemapdlist' in rund.keys()\
                         and 'parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
                         and 'plate_id' in rund['parameters'].keys():
                    rund['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(rund['parameters']['plate_id']), \
                        erroruifcn=\
                    lambda s:mygetopenfile(parent=self, xpath="%s" % os.getcwd(), markstr='Error: %s select platemap for plate_no %s' %(s, rund['parameters']['plate_id'])))

        
        self.paramsdict_le_dflt['ana_type'][1]=self.expfiledict['exp_type']
        self.paramsdict_le_dflt['created_by'][1]=self.expfiledict['exp_type']

        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            if k in ['ana_type', 'created_by']:
                le.setText(dfltstr)
        self.clearanalysis()
        
        self.anadict['exp_path']=self.exppath.replace('.pck', '.exp')
        
        self.fillexpoptions()
    
    def fillexpoptions(self):
        self.clearexp()
        
        self.runk_use=[(k, v['run_use']) for k, v in self.expfiledict.iteritems() if k.startswith('run__')]
        self.uselist=list(set(map(operator.itemgetter(1), self.runk_use)))
        if 'data' in self.uselist:
            temp=self.uselist.pop(self.uselist.index('data'))
            self.uselist=[temp]+self.uselist
        
        for i, k in enumerate(self.uselist):
            self.ExpRunUseComboBox.insertItem(i, k)

        self.ExpRunUseComboBox.setCurrentIndex(0)
        
        self.fillruncheckboxes()
    
    def fillruncheckboxes(self):
        self.usek=str(self.ExpRunUseComboBox.currentText())
        runklist=[runk for runk, usek in self.runk_use if usek==self.usek]
        for cb, runk in zip(self.runcheckboxlist, runklist):
            s=','.join([runk, self.expfiledict[runk]['name']])
            cb.setText(s)
            cb.setChecked(True)
        self.filltechtyperadiobuttons()
    
    def filltechtyperadiobuttons(self):
        qlist=self.TechTypeButtonGroup.buttons()
        numbuttons=len(qlist)
        for button in qlist:
            button.setText('')
            button.setToolTip('')
            
        self.selectrunklist=[str(cb.text()).partition(',')[0] for cb in self.runcheckboxlist if cb.isChecked()]
        self.selectrunklist=[s for s in self.selectrunklist if len(s)>0]
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
        
        count=0
        for nfiles, techk_typek in zip(numfiles, self.techk_typek):
            if count==numbuttons:
                break
            button=qlist[count]
            
            s=','.join(techk_typek)
            button.setText(s)
            button.setToolTip('%d files' %(nfiles))
            if count==0:
                button.setChecked(True)
                self.fillanalysistypes(button)
            count+=1
        
    
    def fillanalysistypes(self, button):
        if button is None:
            button=self.TechTypeButtonGroup.buttons()[0]
            button.setChecked(True)
        s=str(button.text())
        self.techk, garb, self.typek=s.partition(',')
        nfiles_classes=[len(c.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist, anadict=self.anadict)) for i, c in enumerate(AnalysisClasses)]
        self.AnalysisClassInds=[i for i, nf in enumerate(nfiles_classes) if nf>0]
        self.AnalysisNamesComboBox.clear()
        self.AnalysisNamesComboBox.insertItem(0, '')
        for count, i in enumerate(self.AnalysisClassInds):
            self.AnalysisNamesComboBox.insertItem(count+1, AnalysisClasses[i].analysis_name+('(%d)' %nfiles_classes[i]))
            self.AnalysisNamesComboBox.setCurrentIndex(1)
        self.getactiveanalysisclass()
    
    def getactiveanalysisclass(self):
        selind=int(self.AnalysisNamesComboBox.currentIndex())
        if selind==0:
            self.analysisclass=None
            return
        self.analysisclass=AnalysisClasses[self.AnalysisClassInds[selind-1]]
        self.activeana=None
    
    def clearexp(self):
        self.ExpRunUseComboBox.clear()
        for cbl in [self.runcheckboxlist, self.TechTypeButtonGroup.buttons()]:
            for cb in cbl:
                cb.setText('')
                cb.setToolTip('')
                cb.setChecked(False)
        self.plotd={}
    def runbatchprocess(self):
        return

    def importana(self):
        p=mygetopenfile(parent=self, xpath="%s" % os.getcwd(),markstr='Select .ana/.pck to import')
        if len(p)==0:
            return
        anadict=openana(p, stringvalues=True, erroruifcn=None)#don't allow erroruifcn because dont' want to clear temp ana folder until exp successfully opened and then clearanalysis and then copy to temp folder, so need the path defintion to be exclusively in previous line
        if not 'exp_path' in anadict.keys():
            return
        if anadict['ana_version']!='3':
            idialog=messageDialog(self, '.ana version %s is different from present. continue?' %anadict['ana_version'])
            if not idialog.exec_():
                return
        exppath=anadict['exp_path']
        expfiledict=readexpasdict(exppath, includerawdata=False)
        if len(expfiledict)==0:
            idialog=messageDialog(self, 'abort .ana import because fail to open .exp')
            idialog.exec_()
            return
        self.importexp(expfiledict=expfiledict, exppath=exppath)#clearanalysis happens here
        self.anadict=anadict
        anafolder=os.path.split(p)[0]
        for fn in os.listdir(anafolder):
            if fn.endswith('ana') or fn.endswith('pck'):
                continue
            shutil.copy(os.path.join(anafolder, fn), os.path.join(self.tempanafolder, fn))
        self.updateana()

    def editanalysisparams(self):
        if self.analysisclass is None or len(self.analysisclass.params)==0:
            return
        keys_paramsd=[k for k in self.analysisclass.params.keys() if isinstance(v, dict)]
        if len(keys_paramsd)==0:
            self.editanalysisparams_paramsd(self.analysisclass.params)
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
            self.analysisclass.processnewparams()
            selind=int(self.AnalysisNamesComboBox.currentIndex())
            nfiles=len(self.analysisclass.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist, anadict=self.anadict))
            self.AnalysisNamesComboBox.setItemText(selind, self.analysisclass.analysis_name+('(%d)' %nfiles))
    def analyzedata(self):
        if self.analysisclass is None:
            return
        
        checkbool, checkmsg=self.analysisclass.check_input()
        if not checkbool:
            idialog=messageDialog(self, 'Continue analysis? '+checkmsg)
            if not idialog.exec_():
                return
        #rawd=readbinaryarrasdict(keys)
        #expdatfolder=os.path.join(self.expfolder, 'raw_binary')
        expdatfolder=self.expfolder
        
        kfcn=lambda i:'ana__%d' %i
        i=1
        while kfcn(i) in self.anadict.keys():
            i+=1
        anak=kfcn(i)
        #try:
        if 1:
            self.analysisclass.perform(self.tempanafolder, expdatfolder=expdatfolder, anak=anak)
#        except:
#            idialog=messageDialog(self, 'Analysis Crashed. Nothing saved')
#            if not idialog.exec_():
#                removefiles(self.tempanafolder, [k for rund in \
#                   ([self.analysisclass.multirunfiledict]+self.analysisclass.runfiledict.items()) for typed in rund.items() for k in typed.keys()])
#                return
        checkbool, checkmsg=self.analysisclass.check_output()
        if not checkbool:
            idialog=messageDialog(self, 'Keep analysis? '+checkmsg)
            if not idialog.exec_():
                removefiles(self.tempanafolder, [k for d in \
                   ([self.analysisclass.multirunfiledict]+self.analysisclass.runfiledict.items()) for typed in d.values() for k in typed.keys()])
                return
                
        self.anadict[anak]={}
        self.activeana=self.anadict[anak]
        
        self.activeana['name']=self.analysisclass.analysis_name
        self.activeana['analysis_fcn_version']=self.analysisclass.analysis_fcn_version
        self.activeana['description']=self.analysisclass.description
        self.activeana['plot_parameters']=self.analysisclass.plotparams
        le, dflt=self.paramsdict_le_dflt['description']
        s=str(le.text()).strip()
        if len(s)==0 or 'null' in s:
            newdflt=self.activeana['description']
        else:
            newdflt=','.join([s, self.activeana['description']])
        if s==dflt:            
            le.setText(newdflt)
        self.paramsdict_le_dflt['description'][1]=newdflt
        
        if len(self.analysisclass.params)>0:
            self.activeana['parameters']={}
        for k, v in self.analysisclass.params.iteritems():
            if isinstance(v, dict):
                self.activeana['parameters'][k]={}
                for k2, v2 in v.iteritems():
                    self.activeana['parameters'][k][v2]=str(v2)
            else:
                self.activeana['parameters'][k]=str(v)
        self.activeana['technique']=self.techk
        runk_typek_b=sorted([('multi_run', typek, True) for typek in self.analysisclass.multirunfiledict.keys() if len(self.analysisclass.multirunfiledict[typek])>0])
        runk_typek_b+=sorted([(runk, typek, False) for runk, rund in self.analysisclass.runfiledict.iteritems() for typek in rund.keys() if len(rund[typek])>0])
        for runk, typek, b in runk_typek_b:
            frunk='files_'+runk
            if not frunk in self.activeana.keys():
                self.activeana[frunk]={}
            if b:
                self.activeana[frunk][typek]=copy.deepcopy(self.analysisclass.multirunfiledict[typek])
            else:
                self.activeana[frunk][typek]=copy.deepcopy(self.analysisclass.runfiledict[runk][typek])

        self.fomdlist=self.analysisclass.fomdlist
        self.filedlist=self.analysisclass.filedlist
        self.fomnames=self.analysisclass.fomnames
        self.csvheaderdict=self.analysisclass.csvheaderdict
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
        self.plot_generatedata(plotbool=True)


        
    def updateana(self):
        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            s=str(le.text()).strip()
            if len(s)==0:
                s=dfltstr
            self.anadict[k]=s
        
        self.AnaTreeWidgetFcns.filltree(self.anadict)
        
    def viewresult(self):
        d=copy.deepcopy(self.anadict)
        convertfilekeystolist(d)
        importfomintoanadict(d)
        self.parent.visdataui.importana(anafiledict=copy.deepcopy(d), anafolder=self.tempanafolder)
        
        self.parent.visdataui_exec()
        self.hide()

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
        fdlist=[v for k, v in anad.iteritems() if k.startswith('files_') and isinstance(v, dict)]
        removefiles(self.tempanafolder, [k for d in fdlist for k in d.keys()])
        
        if i<(len(keys)-1):
            for ki, knext in zip(keys[i:-1], keys[i+1:]):
                self.anadict[ki]=self.anadict[knext]
        del self.anadict[keys[-1]]
        self.activeana=None
        self.updateana()
        
    def clearanalysis(self):
        self.analysisclass=None
        self.anadict={}
        self.anadict['ana_version']='3'
        
        self.paramsdict_le_dflt['description'][1]='null'

        self.AnaTreeWidget.clear()
        
        for fn in os.listdir(self.tempanafolder):
            os.remove(os.path.join(self.tempanafolder, fn))
        
        
    def importanalysisparams(self):
        return


    def saveana(self):
        self.anafilestr=self.AnaTreeWidgetFcns.createtxt()
        if not 'ana_version' in self.anafilestr:
            return
         
        saveana_tempfolder(self.anafilestr, self.tempanafolder, anadict=self.anadict, erroruifcn=\
            lambda s:mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s, select folder for saving ANA'))
            
        self.importexp(expfiledict=self.expfiledict, exppath=self.exppath)#clear analysis happens here but exp_path wont' be lost
        #self.clearanalysis()
        
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
        totnumheadlines=writecsv_smpfomd(self.analysisclass.primarycsvpath, '', headerdict=self.csvheaderdict, replaceheader=True)
        fnf=os.path.split(self.analysisclass.primarycsvpath)[1]
        files_techd=self.activeana[[k for k in self.activeana.keys() if k.startswith('files_')][0]]
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
        runkarr=numpy.array([d['expkeys'][0] for d in self.filedlist])
        
        inds=numpy.where(numpy.logical_not(numpy.isnan(fom)))[0]
        if len(inds)==0:
            print 'ABORTING PLOTTING BECAUSE ALL FOMs ARE NaN'
            return
        fom=fom[inds]
        runkarr=runkarr[inds]
        sample=numpy.array([self.fomdlist[i]['sample_no'] for i in inds])
        
        inds_runk=dict([(runk, numpy.where(runkarr==runk)[0]) for runk in list(set(runkarr))])
        daqtimebool=self.usedaqtimeCheckBox.isChecked()

        t=[]
#        else:
#            hx=numpy.arange(len(fom))

        for runk in sorted(inds_runk.keys()):
            if daqtimebool:
                fns=[self.filedlist[inds[i]]['expkeys'][-1] for i in inds_runk[runk]]#reduce(dict.get, ['x','q','w'], d)
                t+=[applyfcn_txtfnlist_run(gettimefromheader, self.expfiledict[runk]['run_path'], fns)]

           # hy+=[fom[inds_runk[runk]]]
        if daqtimebool:
            t=numpy.array(t)
            t-=t.min()
#        else:
#            hx=numpy.array(sample)
        
        compplottype=str(self.CompPlotTypeComboBox.currentText())
        
        nanxy=[numpy.nan]*2
        nancomp=[numpy.nan]*4
        xy=[]
        comps=[]
        for runk in sorted(inds_runk.keys()):
            if not 'platemapdlist' in self.expfiledict[runk].keys() or len(self.expfiledict[runk]['platemapdlist'])==0:
                if not compplottype=='none':
                    comps+=[nancomp]*len(inds_runk[runk])
                xy+=[nanxy]*len(inds_runk[runk])
                continue
            pmsmps=[d['Sample'] for d in self.expfiledict[runk]['platemapdlist']]
            xy+=[(smp in pmsmps and \
                         ([self.expfiledict[runk]['platemapdlist'][pmsmps.index(smp)][k] for k in ['x', 'y']],) \
                         or (nanxy, ))[0] for smp in sample[inds_runk[runk]]]
                         
            if not compplottype=='none':
                pmsmps=[d['Sample'] for d in self.expfiledict[runk]['platemapdlist']]
                comps+=[(smp in pmsmps and \
                         ([self.expfiledict[runk]['platemapdlist'][pmsmps.index(smp)][k] for k in ['A', 'B', 'C', 'D']],) \
                         or (nancomp, ))[0] for smp in sample[inds_runk[runk]]]
        xy=numpy.float64(xy)
        comps=numpy.float64(comps)
        
        self.plotd['comps']=numpy.array([c/c.sum() for c in comps])
        self.plotd['xy']=xy
        self.plotd['fom']=fom
        self.plotd['inds_runk']=inds_runk
        self.plotd['t']=t
        self.plotd['sample_no']=sample
        self.plotd['fomname']=self.fomnames[fi]
        if plotbool:
            self.plot()
        
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
        
        m=self.plotw_plate.axes.scatter(x, y, c=fom, s=70, marker='s', cmap=cmap, norm=norm)
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

class treeclass_anadict():
    def __init__(self, tree):
        self.treeWidget=tree
        self.treeWidget.clear()
        
        
    def filltree(self, d, startkey='ana_version', laststartswith='ana__'):
        self.treeWidget.clear()
        #assume startkey is not for dict and laststatswith is dict
        
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
            if execute:
                self.calcui.exec_()
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
