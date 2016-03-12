import time, itertools
import os, os.path, shutil
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
try:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
except ImportError:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
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
from VisualizeAuxFcns import *
from VisualizeBatchFcns import BatchFcnList, BatchDescList
from VisualizeDataForm import Ui_VisDataDialog
from SaveImagesApp import *
from LoadCSVApp import loadcsvDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'
from OpenFromInfoApp import openfrominfoDialog
from CalcFOMApp import AnalysisClasses


class visdataDialog(QDialog, Ui_VisDataDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(visdataDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
        
        #self.SelectTreeView.setModel(CheckableDirModel(self))
        self.AnaExpFomTreeWidgetFcns=treeclass_anaexpfom(self.AnaExpFomTreeWidget, self.SummaryTextBrowser)
        self.OnFlyStoreInterCheckBox.setEnabled(False)
        button_fcn=[\
        (self.AnaPushButton, self.importana), \
        (self.ExpPushButton, self.importexp), \
        (self.OpenInfoPushButton, self.importfrominfo), \
        (self.FolderPushButton, self.openontheflyfolder), \
        (self.UpdateFolderPushButton, self.updateontheflydata), \
        (self.FilenameFilterPushButton, self.createfilenamefilter), \
        (self.UpdateFiltersPushButton, self.updatefiltereddata), \
        (self.UpdatePlotPushButton, self.plotfom), \
        (self.ontheflyPushButton, self.performontheflyfom), \
        (self.customxystylePushButton, self.getxystyle_user), \
        (self.customxylegendPushButton, self.getcustomlegendfcn), \
        (self.addComp, self.addValuesComp), \
        (self.remComp, self.remValuesComp), \
        (self.addxy, self.addValuesXY), \
        (self.remxy, self.remValuesXY), \
        (self.addSample, self.addValuesSample), \
        (self.remSample, self.remValuesSample), \
        (self.SaveFigsPushButton, self.savefigs), \
        (self.SaveStdFigsPushButton, self.save_all_std_plots), \
        (self.LoadCsvPushButton, self.loadcsv), \
        (self.ClearPushButton, self.clearall), \
        (self.RaiseErrorPushButton, self.raiseerror), \
        (self.BatchPushButton, self.runbatchprocess), \
        ]

        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        self.widgetItems_pl_ru_te_ty_co=[]
        for k in ['plate_id', 'run', 'technique', 'type','code']:
            mainitem=QTreeWidgetItem([k], 0)
            self.SelectTreeWidget.addTopLevelItem(mainitem)
            self.widgetItems_pl_ru_te_ty_co+=[mainitem]
        self.SelectTreeFileFilterTopLevelItem=None

        #QObject.connect(self.SelectTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        QObject.connect(self.AnaExpFomTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        
        QObject.connect(self.fomplotchoiceComboBox,SIGNAL("activated(QString)"), self.filterandplotfomdata)
        QObject.connect(self.stdcsvplotchoiceComboBox,SIGNAL("activated(QString)"), self.plot_preparestandardplot)

        QObject.connect(self.compPlotMarkSelectionsCheckBox,SIGNAL("released()"), self.plotfom)
        
        for count, c in enumerate(AnalysisClasses):
            self.OnFlyAnaClassComboBox.insertItem(count, c.analysis_name)
            
        self.batchprocesses=BatchFcnList
        batchdesc=BatchDescList
        for i, l in enumerate(batchdesc):
            self.BatchComboBox.insertItem(i, l)
            
        self.plotwsetup()
        
        self.clearall()
    
    def raiseerror(self):
        raiseerror
    
    def runbatchprocess(self):
        if self.batchprocesses[self.BatchComboBox.currentIndex()](self):
            idialog=messageDialog(self, 'Error in batch process - aborted.')
            idialog.exec_()
        
    def clearall(self):
        self.l_fomdlist=[]
        self.l_fomnames=[]
        self.l_csvheaderdict=[]
        self.l_platemap4keys=[]
        
        self.repr_anaint_plots=1
        self.anafiledict={}
        self.expfiledict={}
        self.expzipclass=None
        self.anazipclass=None
        self.customlegendfcn=lambda sample, els, comp, code, fom: `sample`
        
        self.ellabels=['A', 'B', 'C', 'D']
        
        self.expfolder=''
        self.clearfomplotd()
        self.clearvisuals()
    def clearfomplotd(self):
        self.fomplotd=dict({},fomdlist_index0=[], fomdlist_index1=[], plate_id=[], code=[],sample_no=[], fom=[], xy=[], comp=[], fomname='')
        self.select_idtups=[]
        self.select_circs_plotws=[]
        self.browser.setText('')
    def createfilenamefilter(self):
        
        ans=userinputcaller(self, inputs=[('filename search string', str, '')], title='Enter search string',  cancelallowed=True)
        if ans is None or ans[0].strip()=='':
            return
        ans=ans[0].strip()
        
        if self.SelectTreeFileFilterTopLevelItem is None:
            self.SelectTreeFileFilterTopLevelItem=QTreeWidgetItem(['required filename str'], 0)
        self.SelectTreeWidget.addTopLevelItem(self.SelectTreeFileFilterTopLevelItem)
        
        item=QTreeWidgetItem([ans], 0)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(0, Qt.Checked)
    
        self.SelectTreeFileFilterTopLevelItem.addChild(item)
    
    def importfrominfo(self):
        idialog=openfrominfoDialog(self, runtype='', exp=True, ana=True, run=False)
        idialog.exec_()
        if idialog.selecttype=='ana':
            self.importana(p=idialog.selectpath)
        if idialog.selecttype=='exp':
            self.importexp(experiment_path=idialog.selectpath)
    def importana(self, p=None, anafiledict=None, anafolder=None, anazipclass=None):
        if anafiledict is None or anafolder is None:
            if p is None:
                p=selectexpanafile(self, exp=False, markstr='Select .ana/.pck to import, or .zip file')
            if len(p)==0:
                return
            self.anafiledict, anazipclass=readana(p, stringvalues=False, erroruifcn=None, returnzipclass=True)
            if p.endswith('.ana') or p.endswith('.pck'):
                self.anafolder=os.path.split(p)[0]
            else:
                self.anafolder=p
            if self.anazipclass:
                self.anazipclass.close()
            self.anazipclass=anazipclass
        else:
            self.anafiledict=anafiledict
            self.anafolder=anafolder
            if self.anazipclass:
                self.anazipclass.close()
            self.anazipclass=anazipclass#when run from CalcFOMApp the .ana can't be in a .zip so make this the default anazipclass=None 
        self.clearvisuals()
        summlines=['ANA:']
        summlines+=['-'.join([anak, self.anafiledict[anak]['description'] if 'description' in self.anafiledict[anak].keys() else '']) for anak in self.sorted_ana_exp_keys()]
        self.SummaryTextBrowser.setText('\n'.join(summlines))
        self.importexp(experiment_path=self.anafiledict['experiment_path'], fromana=True)
        
        self.l_fomdlist=[]
        self.l_fomnames=[]
        self.l_csvheaderdict=[]
        self.l_platemap4keys=[]
        
        #this fcn appends all ana fom files to the l_ structures and append to Fom item in tree
        readandformat_anafomfiles(self.anafolder, self.anafiledict, self.l_fomdlist, self.l_fomnames, self.l_csvheaderdict, self.l_platemap4keys, self.AnaExpFomTreeWidgetFcns, anazipclass=self.anazipclass, anakl=self.sorted_ana_exp_keys())
        self.expanafilenameLineEdit.setText(os.path.normpath(self.anafolder))
        self.updatefomdlist_plateruncode()
        
        self.setupfilterchoices()
        self.updatefomplotchoices()
        self.fillxyoptions(clear=True)

    def importexp(self, experiment_path=None, fromana=False):#experiment_path here is the folder, not the file. thsi fcn geretaes expapth, which is the file, but it could be the file too
        if experiment_path is None:
            exppath=selectexpanafile(self, exp=True, markstr='Select .exp/.pck EXP file, or .zip file')
            if exppath is None or len(exppath)==0:
                return
        else:
            if experiment_path.endswith('.exp') or experiment_path.endswith('.pck'):
                exppath=experiment_path
            else:
                exppath=buildexppath(experiment_path)
        expfiledict, expzipclass=readexpasdict(exppath, includerawdata=False, erroruifcn=None, returnzipclass=True)
        if expfiledict is None:
            print 'Problem opening EXP'
            return
#        self.clearexp()
        self.exppath=exppath
        self.expfolder=os.path.split(exppath)[0]
        self.expfiledict=expfiledict
        if self.expzipclass:
            self.expzipclass.close()
        self.expzipclass=expzipclass
        masterels=None
        for runk, rund in self.expfiledict.iteritems():
            if not runk.startswith('run__'):
               continue
            if not ('parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
                     and 'plate_id' in rund['parameters'].keys()):
                print 'critical info missing for ', runk
            if not 'platemapdlist' in rund.keys():
                pmlines, pmpath=get_lines_path_file(p=getplatemappath_plateid(str(rund['parameters']['plate_id']), \
                  erroruifcn=\
                  lambda s, xpath:mygetopenfile(parent=self, xpath=xpath, markstr='Error: %s select platemap for plate_no %s' %(s, rund['parameters']['plate_id']))))
                
                if len(pmpath)==0:
                    idialog=messageDialog(self, 'invalid platemap for %s' %rund['parameters']['plate_id'])
                    idialog.exec_()
                    rund['platemapdlist']=[]
                    return#just try to cancel things so user can open file again
                else:
                    rund['platemapdlist']=readsingleplatemaptxt('', lines=pmlines)#path not used here because passing lines
                    s=str(self.platemapfilenameLineEdit.text())
                    ps=os.path.normpath(pmpath)
                    if not ps in s:
                        self.platemapfilenameLineEdit.setText(','.join([s, ps]).strip(','))
            rund['platemapsamples']=[d['sample_no'] for d in rund['platemapdlist']]
            els=getelements_plateidstr(str(rund['parameters']['plate_id']))
            if els is None:
                print 'cannot find elements for ', str(rund['parameters']['plate_id'])
                masterels=['A', 'B', 'C', 'D']
                continue
#            if len(els)>4:
#                els=els[:4]
            if masterels is None:
                masterels=els
            elif masterels==els:
                continue
            elif set(masterels)==set(els):
                idialog=messageDialog(self, 'Would you like to modify platemap so %s permuted to match previous plate with elements %s?' %(','.join(els), ','.join(masterels)))
                if idialog.exec_():
                    rund['platemapdlist']=[dict(d, origA=d['A'], origB=d['B'], origC=d['C'], origD=d['D'], origE=d['E'], origF=d['F'], origG=d['G'], origH=d['H']) for d in rund['platemapdlist']]
                    channelsused=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][:max(4, len(masterels))]
                    for d in rund['platemapdlist']:
                        d.update([('orig'+k, d[k]) for k in channelsused])
                    for d in rund['platemapdlist']:
                        for let, el in zip(channelsused, masterels):
                            d[let]=d['orig'+channelsused[els.index(el)]]#this allows plates with different permutations of the same set fo elements (as the first plate to be read here) to have their platemaps permuted to match.
                else:
                    masterels=['A', 'B', 'C', 'D']#this will keep any subsequent .exp from matching the masterels and when plots are made they are just vs the platemap channels not the printed elements
            else:#this patholigcal case of having different sets of elements in the same exp/ana is not handled for >4 element prints
                idialog=messageDialog(self, 'WARNING: %s has elements %s but elements %s were already loaded' %(runk,','.join(els), ','.join(masterels)))
                idialog.exec_()
                masterels=['A', 'B', 'C', 'D']
        if masterels is None or masterels==['A', 'B', 'C', 'D']:
            self.ellabels=['A', 'B', 'C', 'D']
        else:#to get here evrythign has a platemap
            self.remap_platemaplabels(newellabels=masterels)

        self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)
        self.fillcomppermutations()
        self.clearfomplotd()
        
        
        if fromana:
            summlines=[str(self.SummaryTextBrowser.toPlainText())]
            get4elementsetstr=lambda anad: ''.join(self.getellabels_pm4keys(anad['platemap_comp4plot_keylist'].split(','))) if 'platemap_comp4plot_keylist' in anad.keys() else ''
            nonabcdsummlines=['-'.join([anak, get4elementsetstr(self.anafiledict[anak])]) for anak in self.sorted_ana_exp_keys()]
            nonabcdsummlines=[l for l in nonabcdsummlines if not l.endswith('-')]#remove the regular ABCD ones
            if len(nonabcdsummlines)>0:
                summlines=['4-plot elements (if not ABCD):']+nonabcdsummlines+summlines
        else:
            self.clearvisuals()
            summlines=[]
            self.expanafilenameLineEdit.setText(os.path.normpath(self.expfolder))
            self.updatefomdlist_plateruncode(createnewfromexp=True)
            self.AnaExpFomTreeWidgetFcns.appendFom(self.l_fomnames[-1], self.l_csvheaderdict[-1])
            self.setupfilterchoices()
            self.updatefomplotchoices()
            self.fillxyoptions(clear=True)
        summlines+=['RUN:']
        summlines+=['-'.join([runk, self.expfiledict[runk]['description'] if 'description' in self.expfiledict[runk].keys() else '']) for runk in self.sorted_ana_exp_keys(ana=False)]
        summlines+=['FOM:']
        self.SummaryTextBrowser.setText('\n'.join(summlines))
        
    def sorted_ana_exp_keys(self, ana=True):
        if ana:
            anarun='ana__'
            anaexpfiled=self.anafiledict
        else:
            anarun='run__'
            anaexpfiled=self.expfiledict
        sorttups=sorted([(int(k[len(anarun):]), k) for k in anaexpfiled.keys() if k.startswith(anarun)])
        return map(operator.itemgetter(1), sorttups)
    def remap_platemaplabels(self, newellabels=None):#should work for up to 8 elements, only the length of ellables will be used
        if not newellabels is None:
            if len(newellabels)<4:
                self.ellabels=newellabels+['A', 'B', 'C', 'D'][len(newellabels):]#allows for <4 elements
            else:
                self.ellabels=newellabels
                
        for runk, rund in self.expfiledict.iteritems():
                if not runk.startswith('run__'):
                    continue
                for d in rund['platemapdlist']:
                    for oldlet, el in zip(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], self.ellabels):
                        d[el]=d[oldlet]
        self.ellabelsLineEdit.setText(','.join(self.ellabels))
    def openontheflyfolder(self, folderpath=None, platemappath=None):#assume on -the-fly will never involve a .zip
        if folderpath is None:
            folderpath=mygetdir(self, markstr='folder for on-the-fly analysis')
        if folderpath is None or len(folderpath)==0:
            return
        self.ellabels=['A', 'B', 'C', 'D']
        if platemappath is None:
            plateidstr=os.path.split(os.path.split(folderpath)[0])[1].rpartition('_')[2][:-1]
            els=getelements_plateidstr(plateidstr)
            platemappath=getplatemappath_plateid(plateidstr, \
                erroruifcn=\
            lambda s, xpath:mygetopenfile(parent=self, xpath=xpath, markstr='Error: %s select platemap for plate_no %s' %(s, plateidstr)))
        if platemappath is None or platemappath=='':
            return
        
        self.clearfomplotd()
        self.clearvisuals()
        
        self.expfolder=folderpath
       
        self.lastmodtime=0
        
        self.expfiledict={}
        self.expfiledict['exp_version']=0
        self.expfiledict['run__1']={}
        self.expfiledict['run__1']['run_path']=self.expfolder
        self.expfiledict['run__1']['run_use']='onthefly'
        self.expfiledict['run__1']['platemapdlist']=readsingleplatemaptxt(platemappath)
        self.expfiledict['run__1']['platemapsamples']=[d['sample_no'] for d in self.expfiledict['run__1']['platemapdlist']]
        self.expfiledict['run__1']['files_technique__onthefly']={}
        self.expfiledict['run__1']['files_technique__onthefly']['all_files']={}
        self.expfiledict['run__1']['parameters']={}
        self.expfiledict['run__1']['parameters']['plate_id']=0
        
        self.platemapfilenameLineEdit.setText(os.path.normpath(platemappath))
        self.remap_platemaplabels(newellabels=els)#if els weren't found the argument will be None so ellables will still be the default from earlier in this function and the remap wont' do anything to a standard platemap
        
        self.anafolder=''
        
        self.anafiledict={}
        self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)
        self.updateontheflydata()
        self.updatefomdlist_plateruncode(createnewfromexp=True)
        self.AnaExpFomTreeWidgetFcns.appendFom(self.l_fomnames[-1], self.l_csvheaderdict[-1])

        
        self.fillcomppermutations()

        self.setupfilterchoices()
        self.updatefomplotchoices()
        self.fillxyoptions(clear=True)
        
        
        
    def updateontheflydata(self):
        #this treates all files in the folder the same and by doing so assumes each file is a measurement on s asample. this could read a .csv fom file but it would be sample_no=nan and would not be ported to self.fomdlist. that is tricky and could be done but not necessary if "on-the-fly" is used for a raw data stream.
        try:
            self.lastmodtime
        except:
            return
        self.lastmodtime, d_appended=createontheflyrundict(self.expfiledict, self.expfolder, lastmodtime=self.lastmodtime)
        self.setupfilterchoices()
        self.AnaExpFomTreeWidgetFcns.appendexpfiles(d_appended)
        self.fillxyoptions()

    #filters for exp file:
    #  run defines a run__ within exp and this is by defintion for only 1 plate_id so filtering by code happens subsequently
    #  plate_id defines a subset of runs within exp and similarly filtering by code happens subsequently
    #  code defines a subset of samples within each run
    #filters for ana file:
    #  ana defines an ana__ with ana and this may contain multipl runs/plate_ids but fom .csv within the ana__ have run and plate_id integers for subsequenct filtering and then code filtering after that
    
    def updatefomdlist_plateruncode(self, inds=None, createnewfromexp=False):
        if createnewfromexp:
            runint_pl_techd=[(int(runk.partition('run__')[2]), rund['parameters']['plate_id'], techd) for runk, rund in [(runk, rund) for runk, rund in self.expfiledict.iteritems() if runk.startswith('run__')] for techk, techd in rund.iteritems() if techk.startswith('files_technique__')]
            runint_pl_smp=sorted(list(set([(runint, pl, filed['sample_no']) for runint, pl, techd in runint_pl_techd for typed in techd.itervalues() for filed in typed.itervalues() if filed['sample_no']>0])))
            self.l_fomdlist=[[dict({}, anaint=0, runint=runint, plate_id=pl, sample_no=smp) for runint, pl, smp in runint_pl_smp]]
            if len(self.l_fomdlist[0])>0:
                self.l_fomnames=[['anaint', 'runint', 'plate_id', 'sample_no']]
                self.l_csvheaderdict=[{}]
                self.l_platemap4keys=[['A', 'B', 'C', 'D']]
            else:
                self.l_fomdlist=[]
                self.l_fomnames=[]
                self.l_csvheaderdict=[]
                self.l_platemap4keys=[]
            
        if inds is None:
            inds=range(len(self.l_fomdlist))
        for ind in inds:
            fomdlist=self.l_fomdlist[ind]
            fomnames=self.l_fomnames[ind]
            for k in ['plate_id', 'runint', 'anaint', 'code']:
                if not k in fomnames:
                    fomnames+=[k]
            for d in fomdlist:
                if not 'plate_id' in d.keys():
                    d['plate_id']=0
                if not 'runint' in d.keys():
                    d['runint']=0
                if not 'anaint' in d.keys():
                    d['anaint']=0
                if not 'code' in d.keys() and (d['runint']==0 or (not 'sample_no' in d.keys()) or d['sample_no']<=0):
                    d['code']=-1
                if not (d['runint']==0 or (not 'sample_no' in d.keys()) or d['sample_no']<=0):
                    rund=self.expfiledict['run__%d' %d['runint']]
                    try:
                        pmd=rund['platemapdlist'][rund['platemapsamples'].index(d['sample_no'])]
                        for k in self.ellabels+['code', 'x', 'y']+['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][:max(4, len(self.ellabels))]:#use A B C D and more if more elements printed
                            if not k in d.keys():
                                #print kTODO
                                d[k]=pmd[k]
                                
                                if not k in fomnames:
                                    fomnames+=[k]
                    except:
                        idialog=messageDialog(self, 'Platemap not valid ')
                        idialog.exec_()
                        return
    
    def fillxyoptions(self, clear=False):
        
        cbl=[\
        self.xplotchoiceComboBox, \
        self.yplotchoiceComboBox, \
        self.rightyplotchoiceComboBox, \
        ]
        
        
        fomopts=set([n for fomnames in self.l_fomnames for n in fomnames])
        arropts=self.AnaExpFomTreeWidgetFcns.set_allfilekeys.difference(fomopts)
        cb=self.yplotchoiceComboBox
        if not clear:#arr options and then fom options except if appending then don't change existing indeces and add the new stuff, which presumably will be iether fom or arr opts
            existset=set([str(cb.itemText(i)) for i in range(cb.count())])
            opts=sorted(list((fomopts.union(arropts)).difference(existset)))
            if len(opts)==0:
                return
            shiftinds=len(existset)+1
        else:
            opts=sorted(list(arropts))+sorted(list(fomopts))
            shiftinds=1
        for cb in cbl:
            if clear:
                cb.clear()
                cb.insertItem(0, 'None')
            for count, s in enumerate(opts):
                cb.insertItem(count+shiftinds, s)
        
    def setupfilterchoices(self):
        #for foms in ana only need the sets of run,plate,code so set that up here and iadd it in below
        sets_pl_ru_co=[set([d[k] for fomdlist in self.l_fomdlist for d in fomdlist]) for k in ['plate_id', 'runint', 'code']]
        sets_pl_ru_te_ty_co=[set(['%d' %v for v in sets_pl_ru_co[0]])]
        sets_pl_ru_te_ty_co+=[set(['run__%d' %v for v in sets_pl_ru_co[1]])]
        sets_pl_ru_te_ty_co+=[set([])]
        sets_pl_ru_te_ty_co+=[set([])]
        sets_pl_ru_te_ty_co+=[sets_pl_ru_co[2]]#code stays as int for now and is convereted below
        #for exp filtering, build a new construct where plate,run,tech,type are wrapped in keys and the value is the array of codes, sorted by filename
        self.exp_keys_codearr_dict={}
        codeset=set([])
        for runk, rund in self.expfiledict.iteritems():
            if not (runk.startswith('run__') and 'platemapdlist' in rund.keys()):
                continue
            plateid=rund['parameters']['plate_id']
            for techk, techd in rund.iteritems():
                if not techk.startswith('files_technique'):
                    continue
                for typek, typed in techd.iteritems():
                    keytup=('%d' %plateid, (runk, techk, typek))
                    codes=[]
                    for filek in sorted(typed.keys()):
                        filed=typed[filek]
                        smp=filed['sample_no']
                        if numpy.isnan(smp) or not smp in rund['platemapsamples']:
                            codes+=[-1]#codes are intgeters so can't uses nan
                        else:
                            codes+=[rund['platemapdlist'][rund['platemapsamples'].index(smp)]['code']]
                    codeset=codeset.union(set(codes))
                    self.exp_keys_codearr_dict[keytup]=numpy.int32(codes)
        flattups=[[pl]+list(kt) for pl, kt in self.exp_keys_codearr_dict.keys()]
        for mainitem in self.widgetItems_pl_ru_te_ty_co:
            items=mainitem.takeChildren()
            for item in items:
                del item
        for i, (mainitem, setfromfoms) in enumerate(zip(self.widgetItems_pl_ru_te_ty_co[:-1], sets_pl_ru_te_ty_co)):
            vals=sorted(list(set(map(operator.itemgetter(i),flattups)).union(setfromfoms)))
            for s in vals:
                item=QTreeWidgetItem([s], 0)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Checked)
                mainitem.addChild(item)
            mainitem.setExpanded(True)
        mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
        for co in sorted(list(codeset)):
            item=QTreeWidgetItem(['%d' %co], 0)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
            mainitem.addChild(item)
        mainitem.setExpanded(True)

    def processclick_selecttreeitem(self, item, column):
        s=str(item.text(column))
        if not s.startswith('*'):
            return
        keylist=[s.strip('*').strip(':')]
        item=item.parent()
        while not item.parent() is None:
            keylist=[str(item.text(0)).strip(':')]+keylist
            item=item.parent()
        anaorexp=str(item.text(0))
        if anaorexp=='ana':
            d=self.anafiledict
            p=os.path.join(self.anafolder, keylist[-1])
            zipclass=self.anazipclass
        else:
            d=self.expfiledict
            runk=keylist[-4]
            fn=keylist[-1]
            ans=buildrunpath_selectfile(fn, self.expfolder, runp=self.expfiledict[runk]['run_path'], expzipclass=self.expzipclass, returnzipclass=True)
            if ans is None:
                return
            p, zipclass=ans
            
        filed=d_nestedkeys(d, keylist)
        filed=copy.copy(filed)#to avoid zipclass being incorproated into exp or anafiledict
        filed['path']=p
        filed['zipclass']=zipclass
        self.plotxy(filed=filed)
            
    def updatefiltereddata(self):
        #filter exp data by parsing the list of exp_keys_codearr_dict keys by plate,run,tech,type filters then filtering by code
        l_keytup=self.exp_keys_codearr_dict.keys()
        for count, mainitem in enumerate(self.widgetItems_pl_ru_te_ty_co[:-1]):
            allowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
            if count==0:
                l_keytup=[kt for kt in l_keytup if kt[0] in allowedvals]
            else:
                l_keytup=[kt for kt in l_keytup if kt[1][count-1] in allowedvals]
        mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
        allowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        #uses the run,tech,typ filekey tuple to get and then sort the filenames, zip those with the codes and then check if each code is in the allowedvalues and if so build the full run,tech,type,fn key list
        if self.SelectTreeFileFilterTopLevelItem is None:
            searchstrs=[]
        else:
            searchstrs=[str(self.SelectTreeFileFilterTopLevelItem.child(i).text(0)).strip() for i in range(self.SelectTreeFileFilterTopLevelItem.childCount()) if bool(self.SelectTreeFileFilterTopLevelItem.child(i).checkState(0))]
        self.filteredexpfilekeys=[list(l_keytup)+[filek] for pl, expkeytup in l_keytup for co, filek in zip(self.exp_keys_codearr_dict[(pl, expkeytup)], sorted(d_nestedkeys(self.expfiledict, expkeytup).keys())) if (co in allowedvals and not (False in [s in filek for s in searchstrs]))]
        #filteredexpfilekeys is not used anywhere!!!
        self.filterandplotfomdata()
        #filter ana fom data by plate, run and code
        
        #need to get the codes adn think about how to getapplicablefilesnames, i.e. create filedlist for simple cases, flag analysis classes by 'simple"
    def performontheflyfom(self):#onthefly fom calc could be on existing (not on thefly) .exp so expfolder could be .zip
        self.analysisclass=AnalysisClasses[self.OnFlyAnaClassComboBox.currentIndex()]
        mainitem=self.widgetItems_pl_ru_te_ty_co[2]
        temp=[str(mainitem.child(i).text(0)).strip().partition('__')[2] for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        if len(temp)==0:
            return
        te=temp[0]#only the first tech checked
        mainitem=self.widgetItems_pl_ru_te_ty_co[3]
        temp=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        if len(temp)==0:
            return
        ty=temp[0]#only the first type checked
        self.analysisclass.getapplicablefilenames(self.expfiledict, '', te, ty)#empty "data usek" string will not filter and then filter by the first checked technique and type

        if self.SelectTreeFileFilterTopLevelItem is None:
            searchstrs=[]
        else:
            searchstrs=[str(self.SelectTreeFileFilterTopLevelItem.child(i).text(0)).strip() for i in range(self.SelectTreeFileFilterTopLevelItem.childCount()) if bool(self.SelectTreeFileFilterTopLevelItem.child(i).checkState(0))]
        
        #do the fitlering by search string after gettapplicablefilenames so the "critfracapplicable" might be really low
        self.analysisclass.filedlist=[d for d in self.analysisclass.filedlist if not (False in [s in d['fn'] for s in searchstrs])]
        
        checkbool, checkmsg=self.analysisclass.check_input(critfracapplicable=.001)
        if not checkbool:
            idialog=messageDialog(self, 'Continue analysis? '+checkmsg)
            if not idialog.exec_():
                return
        #rawd=readbinaryarrasdict(keys)
        #expdatfolder=os.path.join(self.expfolder, 'raw_binary')

        self.analysisclass.perform(None, expdatfolder=self.expfolder, anak='', zipclass=self.expzipclass, expfiledict=self.expfiledict)
        self.l_fomdlist+=[self.analysisclass.fomdlist]#on-the-fly analysis gets appended to the list of dictionaries, but since opening ana cleans these lists, the l_ structures will start with ana csvs.
        self.l_fomnames+=[self.analysisclass.fomnames]
        self.l_csvheaderdict+=[self.analysisclass.csvheaderdict]#this contains default plot info
        self.l_csvheaderdict[-1]['anak']='ana__onthefly'
        self.l_platemap4keys+=[['A', 'B', 'C', 'D']]
        #self.clearfomplotd()  don't need to clear here because all indexes in fomplotd will still work
        #self.l_usefombool+=[True]
        self.updatefomdlist_plateruncode(inds=[-1])
        self.AnaExpFomTreeWidgetFcns.appendFom(self.l_fomnames[-1], self.l_csvheaderdict[-1], uncheckprevious=True)
        self.setupfilterchoices()
        self.updatefomplotchoices()
        self.fillxyoptions()
    def gethighestrunk(self, getnextone=False):
        kfcn=lambda i:'run__%d' %i
        i=1
        while kfcn(i) in self.expfiledict.keys():
            i+=1
        if getnextone:
            runk=kfcn(i)
        else:
            runk=kfcn(i-1)
            if not runk in self.expfiledict.keys():
                return None
        return runk
        
    def loadcsv(self):
    
        newrunk=self.gethighestrunk(getnextone=True)#create a new run, maybe wouldn't need to if somethign already loaded but usually thsi will be used to load only .csv so need to create a run for toehr mechanics to work
        
        pmpath=str(self.platemapfilenameLineEdit.text()).split(',')[-1]#last used platemap or empty if non loaded
        
        idialog=loadcsvDialog(self, ellabels=self.ellabels, platemappath=pmpath, csvstartpath=self.expfolder, runk=newrunk)
        if idialog.error:
            return
        if not idialog.exec_():
            return
        if idialog.error:
            return
        self.ellabels=idialog.ellabels
        if not 'exp_version' in self.expfiledict.keys():
            self.expfiledict['exp_version']=0
        
        self.expfiledict[newrunk]=copy.deepcopy(idialog.rund)
        s=str(self.platemapfilenameLineEdit.text())
        ps=str(idialog.platemapLineEdit.text())
        if not ps in s:
            self.platemapfilenameLineEdit.setText(','.join([s, ps]).strip(','))
                        
        fomnames=copy.copy(idialog.fomnames)
        self.expfiledict[newrunk]['run_path']=idialog.csvpath
        self.expfiledict[newrunk]['run_use']='usercsv'
        self.expfiledict[newrunk]['files_technique__usercsv']={}
        self.expfiledict[newrunk]['files_technique__usercsv']['csv_files']=copy.deepcopy(idialog.runfilesdict)
        
        self.l_fomdlist+=[copy.deepcopy(idialog.fomdlist)]#on-the-fly analysis gets appended to the list of dictionaries, but since opening ana cleans these lists, the l_ structures will start with ana csvs.
        self.l_fomnames+=[copy.copy(idialog.fomnames)]
        self.l_csvheaderdict+=[{}]
        self.l_csvheaderdict[-1]['anak']='ana__loadcsv'
        self.l_platemap4keys+=[['A', 'B', 'C', 'D']]
        #self.clearfomplotd()  don't need to clear here because all indexes in fomplotd will still work
        
        if self.ellabels==['A', 'B', 'C', 'D']:#If default ellabels give option for user to enter new ones. otherwise assume thigns already loaded and use existing ellabels
            self.fillcomppermutations()
        else:
            self.remap_platemaplabels()
        if newrunk=='run__1':
            self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)#might erase things that already exist
        self.updatefomdlist_plateruncode()#inds=[-1])
        self.AnaExpFomTreeWidgetFcns.appendFom(self.l_fomnames[-1], self.l_csvheaderdict[-1], uncheckprevious=True)
        self.setupfilterchoices()
        self.updatefomplotchoices()
        self.fillxyoptions()#clear=True
        
    def filterandplotfomdata(self, plotbool=True):
        self.clearfomplotd()
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[0]
        plateidallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[1]
        runintallowedvals=[int(str(mainitem.child(i).text(0)).lstrip('run__')) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
        codeallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        
        fomname=str(self.fomplotchoiceComboBox.currentText())
        compcolorbool=(fomname=='comp.color')
        if compcolorbool:
            fomname='sample_no'
        l_usefombool=self.AnaExpFomTreeWidgetFcns.getusefombools()
        
        plotdinfo=[]
        for fomdlist_index0, (usebool, fomdlist, fomnames, platemapkeys) in enumerate(zip(l_usefombool, self.l_fomdlist, self.l_fomnames, self.l_platemap4keys)):#the pmkeys here provides custom comps calcualtion without reassigning any pm channels
            if not usebool or not fomname in fomnames:
                continue
            plotdinfo+=[extractplotdinfo(d, platemapkeys, fomname, self.expfiledict, fomdlist_index0, fomdlist_index1) for fomdlist_index1, d in enumerate(fomdlist) if fomname in d.keys() and d['plate_id'] in plateidallowedvals and d['runint'] in runintallowedvals and d['code'] in codeallowedvals]#and not numpy.isnan(d[fomname]), don't do this so can do fomname swap without loss of samples
        for count, k in enumerate(['fomdlist_index0','fomdlist_index1','plate_id','code','sample_no', 'fom', 'xy', 'comps']):
            self.fomplotd[k]=numpy.array(map(operator.itemgetter(count), plotdinfo))
        self.fomplotd['comps']=numpy.array([c/c.sum() for c in self.fomplotd['comps']])
        if compcolorbool:
            self.fomplotd['fomname']='comp.color'
        else:
            self.fomplotd['fomname']=fomname
        #if fomname is in multiple l_fomdlist a given sample can be included in fomplotd numerous times. this create ambiguity for selecting samples and the plotted fom colored symbols will overlay each other and only the top one will be visible
        if plotbool:
            self.fomstats()
            self.plotfom()
    
#    #can point the activate fom checkbox to here but user has to click "OK" to refilter data to ensure that the scope fo the plot matches the checked fitler boxes. can just re-filter without much loss of speed
#    def updatefomchoiceandplot(self):
#        fomname=str(self.fomplotchoiceComboBox.currentText())
#        compcolorbool=(fomname=='comp.color')
#        if compcolorbool:
#            self.fomplotd['fomname']='comp.color'
#            self.fomplotd['fom']=self.fomplotd['sample_no']
#            return
#        
#        if False in [fomname in self.l_fomdlist[i0][i1].keys() for i0,i1 in zip(self.fomplotd['fomdlist_index0'], self.fomplotd['fomdlist_index1'])]:
#            idialog=messageDialog(self, 'selected FOM is not in all of presently filtered samples.\nOK to re-filter or Cancel and select other FOM')
#            if not idialog.exec_():
#                return
#            self.filterandplotfomdata()
#        self.fomplotd['fom']=numpy.array([self.l_fomdlist[i0][i1][fomname] for i0,i1 in zip(self.fomplotd['fomdlist_index0'], self.fomplotd['fomdlist_index1'])])
#        self.fomplotd['fomname']=fomname
#        
#        self.plotfom()
        
    def updatefomplotchoices(self):
        self.fomplotchoiceComboBox.clear()
        self.stdcsvplotchoiceComboBox.clear()
        self.numStdPlots=0
        self.fomselectnames=sorted(list(set([nam for fomnames in self.l_fomnames for nam in fomnames])))
        if len(self.fomselectnames)==0:
            return
        self.fomplotchoiceComboBox.insertItem(0,'comp.color')
        for count, s in enumerate(self.fomselectnames):
            self.fomplotchoiceComboBox.insertItem(count+1, s)#fom choices are not associated with particular indeces of the l_ structures
        self.fomplotchoiceComboBox.setCurrentIndex(0)

        
        self.stdcsvplotchoiceComboBox.insertItem(0, 'null')
        #these 2 lines assemble a subset of the ;_ data structure entires based on if all the nec essary properties are there for being a "standard plot"
        tuplist=[(count, csvheaderdict) for count, csvheaderdict in enumerate(self.l_csvheaderdict) if 'plot_parameters' in csvheaderdict.keys() and 'plot__1' in csvheaderdict['plot_parameters'].keys()]
        keys=['%d; %s; %s; %s' %(count+1, csvheaderdict['plot_parameters'][k]['fom_name'], csvheaderdict['anak'], k) for count, csvheaderdict in tuplist for k in sorted(csvheaderdict['plot_parameters'].keys()) if k.startswith('plot__') and 'fom_name' in csvheaderdict['plot_parameters'][k].keys() and csvheaderdict['plot_parameters'][k]['fom_name'] in self.fomselectnames]
        for count, s in enumerate(keys):
            self.stdcsvplotchoiceComboBox.insertItem(count+1, s)
            self.numStdPlots+=1
#            if len(keys)==0:#not sure of new plots will be created in this app
#                count=-1
#                newk='new plot__1'
#            else:
#                newk='new plot__%d' %(int(keys[-1].partition('__')[2])+1)
#            self.stdcsvplotchoiceComboBox.insertItem(count+1, newk)

        self.stdcsvplotchoiceComboBox.setCurrentIndex(0)
        

    
    def plot_preparestandardplot(self, plotbool=True, loadstyleoptions=True):
        s=str(self.stdcsvplotchoiceComboBox.currentText())
        if s=='null':
            for mainitem in self.widgetItems_pl_ru_te_ty_co[:2]:
                for i in range(mainitem.childCount()):
                    mainitem.child(i).setCheckState(0, Qt.Checked)
            return
        #ind=int(self.stdcsvplotchoiceComboBox.currentIndex())-1#can not use current index because not all l_ things may have required standard plot options and some may have many
        
        ind, fomname, anak, plotk=s.split('; ')
        ind=int(ind)-1
        #check only the rleevant plate_id and run in top treewidget
        dlist=self.l_fomdlist[ind]
        platelist=set(['%s' %d['plate_id'] for d in dlist if 'plate_id' in d.keys()])
        runlist=set(['run__%d' %d['runint'] for d in dlist if 'runint' in d.keys()])
        for mainitem, vals in zip(self.widgetItems_pl_ru_te_ty_co[:2], [platelist, runlist]):
            for i in range(mainitem.childCount()):
                item=mainitem.child(i)
                item.setCheckState(0, Qt.Checked if str(item.text(0)) in vals else Qt.Unchecked)
        #check only the fom in bottom tree widget
        self.AnaExpFomTreeWidgetFcns.uncheckfoms()
        item=self.AnaExpFomTreeWidgetFcns.fomwidgetItem.child(ind)
        item.setCheckState(0, Qt.Checked)
        d=self.l_csvheaderdict[ind]['plot_parameters'][plotk]
        fomnames=[self.fomplotchoiceComboBox.itemText(i) for i in range(self.fomplotchoiceComboBox.count())]
        if not d['fom_name'] in fomnames:
            return
        self.fomplotchoiceComboBox.setCurrentIndex(fomnames.index(d['fom_name']))
        if loadstyleoptions:
            for k, le in [('colormap', self.colormapLineEdit), ('colormap_over_color', self.aboverangecolLineEdit), ('colormap_under_color', self.belowrangecolLineEdit)]:
                if not k in d.keys():
                    continue
                le.setText(d[k])
            if 'colormap_min_value' in d.keys() and 'colormap_max_value' in d.keys():
                self.vminmaxLineEdit.setText('%s,%s' %(d['colormap_min_value'], d['colormap_max_value']))
        if plotbool:
            self.filterandplotfomdata(plotbool=True)
            
    def fomstats(self):
        self.plotw_fomhist.axes.cla()
        fom=self.fomplotd['fom']
        fom=fom[numpy.logical_not(numpy.isnan(fom))]
        if len(fom)==0:
            self.fomstatsTextBrowser.setText('')
            return
        tempfmt=lambda x:('%.2e' if x>999. else ('%.4f' if x>.009 else '%.2e')) %x
        strarr=[]
        for fcn in [numpy.mean, numpy.median, numpy.std, numpy.min, numpy.max, .05, .1, .9, .95]:
            if isinstance(fcn, float):
                strarr+=[[('%d' %(fcn*100))+'%', tempfmt(numpy.percentile(fom, fcn*100))]]
            else:
                strarr+=[[fcn.func_name, tempfmt(fcn(fom))]]
        strarr=numpy.array(strarr)
        s='\n'.join(['\t'.join([v for v in a]) for a in strarr])
        self.fomstatsTextBrowser.setText(s)
        
        n, bins, patches = self.plotw_fomhist.axes.hist(fom, 20, normed=False, histtype='stepfilled')
        autotickformat(self.plotw_fomhist.axes, x=1, y=0)
        #self.plotw_fomhist.fig.setp(patches)
        self.plotw_fomhist.fig.canvas.draw()
    
    def extractxy_fomnames(self, arrkeys):
        #get the fomdlist that have the requested fomname and make sure it is represented in the fomplotd,  which is post-filters
        #if plotting fom1 vs fom2 they both need to be in the same fomd, i.e. this routine will not try to pair them up by plate,sample or other means
        fominds_xyy=[[i0 for i0, fomnames in enumerate(self.l_fomnames) if k in fomnames and i0 in self.fomplotd['fomdlist_index0']] for k in arrkeys]
        if len(fominds_xyy[0])+len(fominds_xyy[1])+len(fominds_xyy[2])==0:#if none of x,y,yl in fomnames quit but otherwise only use x,y,yl that are in fomnames
            return None
        x_inds_fom=[]
        plotdata=[[[], []], [[], []]]
        selectpointdata=[[[], []], [[], []]]
        for count, (k, i0list) in enumerate(zip(arrkeys, fominds_xyy)):
            inds_fom=[[(i0, i1), self.l_fomdlist[i0][i1][k]] for i0 in i0list for i1 in self.fomplotd['fomdlist_index1'][self.fomplotd['fomdlist_index0']==i0]]
            if len(inds_fom)==0:
                continue
            if count==0:
                x_inds_fom=inds_fom
            else:
                if arrkeys[0]=='None':#for x use indexes
                    ytemp=map(operator.itemgetter(1), inds_fom)
                    ytemp=numpy.array(ytemp)
                    ytemp=ytemp[numpy.logical_not(numpy.isnan(ytemp))]
                    xtemp=numpy.arange(len(ytemp))
                    plotdata[count-1]=[xtemp, ytemp]
                    if not self.selectind is None:
                        i0, i1=(self.fomplotd['fomdlist_index0'][self.selectind], self.fomplotd['fomdlist_index1'][self.selectind])
                        if (i0, i1) in map(operator.itemgetter(0), inds_fom):
                            i=map(operator.itemgetter(0), inds_fom).index((i0, i1))
                            selectpointdata[count-1]=[[i], [inds_fom[i][1]]]
                else:
                    #pair up fom data points between x and y
                    indsset=sorted(list(set(map(operator.itemgetter(0), inds_fom)).intersection(map(operator.itemgetter(0), x_inds_fom))))
                    if len(indsset)==0:
                        continue
                    if not self.selectind is None:
                        i0, i1=(self.fomplotd['fomdlist_index0'][self.selectind], self.fomplotd['fomdlist_index1'][self.selectind])
                        if (i0, i1) in indsset:
                            selectpointdata[count-1]=[[self.l_fomdlist[i0][i1][arrkeys[0]]], [self.l_fomdlist[i0][i1][k]]]#signle data point corresponding to select sample
                    xtemp=numpy.array([fom for inds, fom in x_inds_fom if inds in indsset])
                    ytemp=numpy.array([fom for inds, fom in inds_fom if inds in indsset])
                    notnaninds=numpy.where(numpy.logical_not(numpy.isnan(xtemp))&numpy.logical_not(numpy.isnan(ytemp)))[0]
                    xtemp=xtemp[notnaninds]
                    sortinds=numpy.argsort(xtemp)
                    xtemp=xtemp[sortinds]
                    ytemp=ytemp[notnaninds][sortinds]
                    plotdata[count-1]=[xtemp, ytemp]

        return plotdata, selectpointdata
    def extractxy_ana(self, arrkeys, anaint, runint, smp):
        xyy=[None, None, None]
        anak='ana__%d' %anaint
        anarunk='files_run__%d' %runint
        if not anarunk in self.anafiledict[anak].keys():
            return xyy
        anarund=self.anafiledict[anak][anarunk]
        mainitem=self.widgetItems_pl_ru_te_ty_co[2]
        #allowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        fn_filed_tosearch=[(fn, filed) for techk, techd in anarund.iteritems() for fn, filed in techd.iteritems() if techk.startswith('inter_') and filed['sample_no']==smp]#techk in allowedvals 
        
        for count, k in enumerate(arrkeys):
            if k=='None':
                continue
            fn_filed_keyind_rawselind=[(fn, filed, filed['keys'].index(k), None if not 'rawselectinds' in filed['keys'] else filed['keys'].index('rawselectinds')) for fn, filed in fn_filed_tosearch if k in filed['keys']]
            if len(fn_filed_keyind_rawselind)>0:#ideally this is length 1 because if onlger that means foudn the same array multiple places and choosing the 1 found first
                fn, filed, keyind, rawselind=fn_filed_keyind_rawselind[0]
                selcolinds=[keyind]
                rawselbool=not rawselind is None
                if rawselbool:
                    selcolinds+=[rawselind]
                arr2d=getarrs_filed(os.path.join(self.anafolder, fn), filed, selcolinds=selcolinds, zipclass=self.anazipclass)
                if not arr2d is None:
                    xyy[count]={}
                    xyy[count]['arr']=arr2d[0]
                    xyy[count]['path']=os.path.join(self.anafolder, fn)
                    xyy[count]['k']=k
                    if rawselbool:
                        xyy[count]['rawselectinds']=numpy.int32(arr2d[1])
        return xyy
    
    def extractxy_exp(self, arrkeys, runint, smp):
        xyysubset=[None]*len(arrkeys)#this is a subset of x, y and yr if any of those found in ana
        runk='run__%d' %runint
        rund=self.expfiledict[runk]
        mainitem=self.widgetItems_pl_ru_te_ty_co[2]
        techallowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        mainitem=self.widgetItems_pl_ru_te_ty_co[3]
        typeallowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        techitems=[(techk, techd) for techk, techd in rund.iteritems() if techk in techallowedvals and isinstance(techd, dict)]
        if self.SelectTreeFileFilterTopLevelItem is None:
            searchstrs=[]
        else:
            searchstrs=[str(self.SelectTreeFileFilterTopLevelItem.child(i).text(0)).strip() for i in range(self.SelectTreeFileFilterTopLevelItem.childCount()) if bool(self.SelectTreeFileFilterTopLevelItem.child(i).checkState(0))]

        fn_filed_tosearch=[(fn, filed) for techk, techd in techitems for typek, typed in techd.iteritems() for fn, filed in typed.iteritems() if typek in typeallowedvals and filed['sample_no']==smp and (not (False in [s in fn for s in searchstrs]))]
        
        for count, k in enumerate(arrkeys):
            if k=='None':
                continue
            fn_filed_keyind=[(fn, filed, filed['keys'].index(k)) for fn, filed in fn_filed_tosearch if k in filed['keys']]
            if len(fn_filed_keyind)>0:#ideally this is length 1 because if onlger that means foudn the same array multiple places and choosing the 1 found first
                fn, filed, keyind=fn_filed_keyind[0]
                selcolinds=[keyind]
                ans=buildrunpath_selectfile(fn, self.expfolder, runp=rund['run_path'], expzipclass=self.expzipclass, returnzipclass=True)
                if ans is None:
                    continue
                p, zipclass=ans
                arr2d=getarrs_filed(p, filed, selcolinds=selcolinds, zipclass=zipclass)
                if zipclass!=self.expzipclass:
                    zipclass.close()
                if not arr2d is None:
                    xyysubset[count]={}
                    xyysubset[count]['arr']=arr2d[0]
                    xyysubset[count]['path']=p
                    xyysubset[count]['k']=k
        return xyysubset
        
    def extractxydata(self, arrkeys, filed=None):
        #plottign from single file so x is required to be in there and then if either of the y are in, filter by nan and sort. No label for legend because not necessarily a sample_no, i.e. could be a fom file selected
        if not filed is None:
            keyinds=[filed['keys'].index(arrk) if arrk in filed['keys'] else None for arrk in arrkeys]
            if keyinds[0] is None or (keyinds[1] is None and keyinds[2] is None):#no pari of x,y to plot
                return None
            selcolinds=[keyind for keyind in keyinds if not keyind is None]
            arr2d=getarrs_filed(filed['path'], filed, selcolinds=selcolinds, zipclass=filed['zipclass'])
            plotdata=[[[], []], [[], []]]
            for count, (keyind, yind_arr2d) in enumerate(zip(keyinds[1:], [1, -1])):
                if keyind is None:
                    continue
                xtemp=arr2d[0]
                ytemp=arr2d[yind_arr2d]
                notnaninds=numpy.where(numpy.logical_not(numpy.isnan(xtemp))&numpy.logical_not(numpy.isnan(ytemp)))[0]
                xtemp=xtemp[notnaninds]
                sortinds=numpy.argsort(xtemp)
                xtemp=xtemp[sortinds]
                ytemp=ytemp[notnaninds][sortinds]
                plotdata[count]=[xtemp, ytemp]
            return plotdata, [[[], []], [[], []]], {}
        #try to find any of the keys in foms and if so all plot data comes from there. In this case selectind is used to highlight a point int he x-y plot but not used to find data. all data in fomplotd will be considered
        if len(self.l_fomnames)>0:
            tempplotdatatup=self.extractxy_fomnames(arrkeys)
            if not tempplotdatatup is None:
                return tempplotdatatup[0], tempplotdatatup[1], {}
        #from here on not fom so find the data arrays,  and since "select" referse to an index of fomplotd, there is no special "selectpointdata"
        if self.selectind is None:
            return None
        selectpointdata=None
        i0, i1=(self.fomplotd['fomdlist_index0'][self.selectind], self.fomplotd['fomdlist_index1'][self.selectind])
        anaint, runint, smp=[self.l_fomdlist[i0][i1][k] for k in ['anaint', 'runint', 'sample_no']]

        if anaint==0 and runint==0:
            return None
        if anaint>0:
            xyydlist=self.extractxy_ana(arrkeys, anaint, runint, smp)
        else:
            xyydlist=[None, None, None]
        if runint>0:
            lefttogetinds=[count for count, (d, arrk) in enumerate(zip(xyydlist, arrkeys)) if d is None and not arrk=='None']
            if len(lefttogetinds)>0:
                xyysubset=self.extractxy_exp([arrkeys[i] for i in lefttogetinds], runint, smp)
                for i, d in zip(lefttogetinds, xyysubset):#d might stil be None at this points
                    xyydlist[i]=d
        plotdata=[[[], []], [[], []]]
        for count, (xd, yd) in enumerate([(xyydlist[0], xyydlist[1]), (xyydlist[0], xyydlist[2])]):
            if xd is None or yd is None:
                continue
            if len(xd['arr'])==len(yd['arr']):
                plotdata[count]=[xd['arr'], yd['arr']]
                continue
            for draw, dint in [(xd, yd), (yd, xd)]:#rawselectinds applied to the array deemed to be raw by not having rawselectinds. cannot plot 2 interlen things against each other
                if 'rawselectinds' in dint.keys() and (not 'rawselectinds' in draw.keys()) and len(draw['arr'])>(dint['rawselectinds'].max()):
                    draw['arr']=draw['arr'][dint['rawselectinds']]
                    break
            if len(xd['arr'])==len(yd['arr']):
                plotdata[count]=[xd['arr'], yd['arr']]
                continue
            if count==0:
                print len(xd['arr']), len(yd['arr'])
                idialog=messageDialog(self, 'ERROR: %s and %s are length %d and %d after reading from \n%s\n%s' %(xd['k'], yd['k'], len(xd['arr']), len(yd['arr']), xd['path'], yd['path']))
                idialog.exec_()
                return None
        getval=lambda k:self.fomplotd[k][self.selectind]
        lab=self.customlegendfcn(getval('sample_no'), self.getellabels_pm4keys(self.l_platemap4keys[i0]), getval('comps'), getval('code'), getval('fom'))
        return plotdata, [[[], []], [[], []]], dict([('xylab', lab)])
        
    def getellabels_pm4keys(self, pmkeys):
        ellabelinds=[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].index(pmk) for pmk in pmkeys]
        return [self.ellabels[i] if i<len(self.ellabels) else 'X' for i in ellabelinds]#pmkeys should refer to element label indeces that exist but if not fill the X to softly notify the user that soemthig is wrong, i.e. not all the element labels were read from the database
    def plotxy(self, filed=None):#filed to plot from a  single file and must have key 'path' in addition to standard filed
        cbl=[\
        self.xplotchoiceComboBox, \
        self.yplotchoiceComboBox, \
        self.rightyplotchoiceComboBox, \
        ]
        arrkeys=[str(cb.currentText()) for cb in cbl]
        if arrkeys==(['None']*3):
            return
        tempplotdatatup=self.extractxydata(arrkeys, filed=filed)
        if tempplotdatatup is None:
            return 
        self.plotdata, self.selectpointdata, plotattrd=tempplotdatatup
        
        
        if not self.overlayselectCheckBox.isChecked():
            self.plotw_xy.axes.cla()
            self.plotw_xy.twaxes.cla()
        
        if self.overlayselectCheckBox.isChecked():
            self.xyplotcolorrotation=self.xyplotcolorrotation[1:]+[self.xyplotcolorrotation[0]]
            self.xyplotstyled['c']=self.xyplotcolorrotation[0]
        else:
            self.xyplotcolorrotation=['b', 'k', 'm', 'y', 'c','r', 'g']
            self.xyplotstyled['c']='b'
            
        somethingplotted=False
        for count, (ax, (xarr, yarr), (sxarr, syarr), xl, yl) in enumerate(zip([self.plotw_xy.axes, self.plotw_xy.twaxes], self.plotdata, self.selectpointdata, [arrkeys[0], arrkeys[0]], [arrkeys[1], arrkeys[2]])):
            if len(xarr)==0:
                continue
            somethingplotted=True
            if count==0:
                styled=dict([(k, v) for k, v in self.xyplotstyled.iteritems() if not 'sel' in k and not 'right_' in k and v!=''])
            else:
                styled=dict([(k.partition('right_')[2], v) for k, v in self.xyplotstyled.iteritems() if 'right_' in k and v!=''])
            if count==0 and 'xylab' in plotattrd.keys():
                styled['label']=plotattrd['xylab']
            ax.plot(xarr, yarr, **styled)
            ax.set_xlabel(xl)
            ax.set_ylabel(yl)
            if len(sxarr)==0:
                continue
            selstyled=dict([(k.partition('select_')[2], v) for k, v in self.xyplotstyled.iteritems() if 'select_' in k and v!=''])
            selstyled['marker']=self.xyplotstyled['marker']
            ax.plot(sxarr, syarr, **selstyled)
            
        leg=self.plotw_xy.axes.legend(loc=0)
        #leg.draggable()


            
        autotickformat(self.plotw_xy.axes, x=1, y=1)
        autotickformat(self.plotw_xy.twaxes, x=0, y=1)
        self.plotw_xy.fig.canvas.draw()
    
    def getcustomlegendfcn(self):
        widg=legendformatwidget(self.parent)
        widg.exec_()
        self.customlegendfcn=widg.genlegfcn
        
        
    def fillcomppermutations(self):
        if self.ellabels==['A', 'B', 'C', 'D']:#default to only using 4 elements , i.e. if more than that then they should have been ready correctly from database and are not enter-able here
            ans=userinputcaller(self, inputs=[('A', str, 'A'), ('B', str, 'B'), ('C', str, 'C'), ('D', str, 'D')], title='Enter element labels',  cancelallowed=True)
            if not ans is None:
                self.ellabels=[v.strip() for v in ans]
                self.remap_platemaplabels()
        self.CompPlotOrderComboBox.clear()
        if len(self.ellabels)==4:
            els=self.ellabels
        else:
            els=['0', '1', '2', '3']# for when there are more than 4 elements from which 4-el selections will be made from the anadict['platemap_comp4plot_keylist'] and this permuation permutes that selection
        for count, l in enumerate(itertools.permutations(els, 4)):
            self.CompPlotOrderComboBox.insertItem(count, ','.join(l))
        self.CompPlotOrderComboBox.setCurrentIndex(0)
        
    def plotfom(self):
        
        if len(self.fomplotd['plate_id'])==0:
            return
        
        newplateids=sorted(list(set(self.fomplotd['plate_id'])))
        if self.tabs__plateids!=newplateids:
            self.tabs__plateids=self.setup_TabWidget(self.tabs__plateids, newplateids, compbool=False)
        
        newcodes=sorted(list(set(self.fomplotd['code'])))
        if len(newcodes)>1:#if more than 1 code make -1 an additional tab that plots all codes together
            newcodes+=[-1]
        if self.tabs__codes!=newcodes:
            self.tabs__codes=self.setup_TabWidget(self.tabs__codes, newcodes, compbool=True)
        fom=self.fomplotd['fom']#this is just sample_no if 'comp.color'
        inds=numpy.where(numpy.logical_not(numpy.isnan(fom)))[0]
        fom=fom[inds]
        plate=self.fomplotd['plate_id'][inds]
        code=self.fomplotd['code'][inds]
        x, y=(self.fomplotd['xy'][inds]).T
        comps=self.fomplotd['comps'][inds]
        
        idtupsarr=numpy.array([self.fomplotd['fomdlist_index0'][inds],self.fomplotd['fomdlist_index1'][inds]]).T

        if len(inds)==0:
            idialog=messageDialog(self, 'Nothing to plot, all FOMs probably NaN. Existing plots to remain unchanged.')
            idialog.exec_()
            return
        elif self.fomplotd['fomname']=='comp.color':
            cols=QuaternaryPlotInstance.rgb_comp(comps)
            sm=None
        else:
            #plate plot
            cmapstr=str(self.colormapLineEdit.text())
            try:
                self.cmap=eval('cm.'+cmapstr)
            except:
                self.cmap=cm.jet

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
                    for count, (fcn, le) in enumerate(zip([self.cmap.set_under, self.cmap.set_over], [self.belowrangecolLineEdit, self.aboverangecolLineEdit])):
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

            
            self.norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
            if skipoutofrange[0]:
                inds=numpy.where(fom>=self.vmin)
                plate=plate[inds]
                code=code[inds]
                fom=fom[inds]
                comps=comps[inds]
                x=x[inds]
                y=y[inds]
                idtupsarr=idtupsarr[inds]
            if skipoutofrange[1]:
                inds=numpy.where(fom<=self.vmax)
                plate=plate[inds]
                code=code[inds]
                fom=fom[inds]
                comps=comps[inds]
                x=x[inds]
                y=y[inds]
                idtupsarr=idtupsarr[inds]
            if numpy.any(fom>self.vmax):
                if numpy.any(fom<self.vmin):
                    self.extend='both'
                else:
                    self.extend='max'
            elif numpy.any(fom<self.vmin):
                self.extend='min'
            else:
                self.extend='neither'
            
            sm=cm.ScalarMappable(norm=self.norm, cmap=self.cmap)
            sm.set_array(fom)
            cols=numpy.float32(map(sm.to_rgba, fom))[:, :3]
  
        self.comppermuteinds=list([l for l in itertools.permutations([0, 1, 2, 3], 4)][self.CompPlotOrderComboBox.currentIndex()])
        
        pmkeys=self.l_platemap4keys[idtupsarr[0][0]]#get the first pmkeys and then check if the others are the same. this is just ABCD unless changed by platemap_comp4plot_keylist
        pmkeys_consistent_bools=[self.l_platemap4keys[idtup[0]]==pmkeys for idtup in idtupsarr]
        if False in pmkeys_consistent_bools:
            idialog=messageDialog(self, 'Trying to plot FOMs from ana__ with different 4-element lists. Continue?')
            if not idialog.exec_():
                return
            els=['X', 'X', 'X', 'X']
            print 'Trying to plot FOMs from ana__ with different 4-element lists'
        else:
            els=self.getellabels_pm4keys(pmkeys)
        self.quatcompclass.ellabels=[els[i] for i in self.comppermuteinds]
        
        self.select_circs_plotws=[(None, None)]*len(self.select_idtups)
        for val, plotw in zip(self.tabs__plateids, self.tabs__plotw_plate):
            inds=numpy.where(plate==val)[0]
            self.plateplot(plotw, x[inds], y[inds], cols[inds], sm)
            for xvyv, tupind in [((xv, yv), self.select_idtups.index(tuple(tupa))) for xv, yv, tupa in zip(x[inds], y[inds], idtupsarr[inds]) if tuple(tupa) in self.select_idtups]:
                circ = pylab.Circle(xvyv, radius=1, edgecolor='r', facecolor='none')
                self.select_circs_plotws[tupind]=(circ, plotw)
                plotw.axes.add_patch(circ)
        
#        if self.compPlotMarkSelectionsCheckBox.isChecked():
#            
#            #cols=numpy.float64([[1, 0, 0] if tuple(tupa) in self.select_idtups else [0, 0, 0] for tupa in idtupsarr])
#            compstocolor=numpy.float64([comps for tupa, comps in idtupsarr if tuple(tupa) in self.select_idtups])

        
        if int(self.CompPlotTypeComboBox.currentIndex())>0:
            for val, plotw in zip(self.tabs__codes, self.tabs__plotw_comp):
                if val<0:#tab for code -1 is to plot all codes together
                    inds=numpy.where(code>=0)[0]
                else:
                    inds=numpy.where(code==val)[0]
                if self.compPlotMarkSelectionsCheckBox.isChecked():
                    c=numpy.float64([[1, 0, 0] if tuple(tupa) in self.select_idtups else [0, 0, 0] for tupa in idtupsarr[inds]])
                    sortinds_inds=numpy.argsort(c.sum(axis=1))#this sorting puts the "brightest" colors on top so any duplicate black compositions are plotted underneath
                    inds=inds[sortinds_inds]
                    c=c[sortinds_inds]
                    #compstocolor=numpy.float64([comps for tupa, comps in idtupsarr[inds] if tuple(tupa) in self.select_idtups])
                else:
                    c=cols[inds]
                plotw.toComp=self.compplot(plotw, comps[inds], c, sm)
        
        if len(idtupsarr)==0:
            self.repr_anaint_plots=1
        else:
            self.repr_anaint_plots=numpy.median([self.l_fomdlist[i0][i1]['anaint'] for i0, i1 in idtupsarr]) #not sure if there is a better way to deicde whcih ana saved figures becomes associated with
            
    
    def plateplot(self, plotw, x, y, cols, sm):
        plotw.axes.cla()
        plotw.cbax.cla()
        if len(cols)==0:
            return
        userstr=str(self.platescatterLineEdit.text())
        try:
            if not userstr[0].isdigit():
                marker=userstr[0]
                s=int(userstr[1:])
            else:
                marker='s'
                s=int(userstr)
        except:
            print 'plate scatter format to default because cannot understand ', userstr
            marker='s'
            s=70
        m=plotw.axes.scatter(x, y, c=cols, s=s, marker=marker, edgecolor='none')#, cmap=self.cmap, norm=self.norm)
        if x.max()-x.min()<2. or y.max()-y.min()<2.:
            plotw.axes.set_xlim(x.min()-1, x.max()+1)
            plotw.axes.set_ylim(y.min()-1, y.max()+1)
        else:
            plotw.axes.set_aspect(1.)
        if sm is None:
            plotw.cbax.cla()
        else:
            cb=plotw.fig.colorbar(sm, cax=plotw.cbax, extend=self.extend, format=autocolorbarformat((self.vmin, self.vmax)))
            cb.set_label(self.fomplotd['fomname'])
        plotw.fig.canvas.draw()
        
    def compplot(self, plotw, comps, cols, sm):
        plotw.axes.cla()#uncommented on 20160213, must be some issue with clearing for some plats
#        plotw.cbax.cla()
        if len(cols)==0:
            return lambda x, y, ax: None
        s=str(self.compplotsizeLineEdit.text()).strip()
        if len(s)==0:
            s='patch'
        elif s[0].isdigit():
            s=int(s)
        
        compsinds=[i for i, (compv, colv) in enumerate(zip(comps, cols)) if not (numpy.any(numpy.isnan(compv)) or numpy.any(numpy.isnan(colv)))]
        if len(compsinds)==0:
            return lambda x, y, ax: None
        self.quatcompclass.loadplotdata(comps[compsinds][:, self.comppermuteinds], cols[compsinds])
        plotw3dbool=self.quatcompclass.plot(plotw=plotw, s=s)
        #plotw.redoaxes(projection3d=)
        if sm is None:
            self.quatcompclass.cbax.cla()
        else:
            if not plotw3dbool is None:
                if plotw3dbool:
                    cb=plotw.fig.colorbar(sm, cax=self.quatcompclass.cbax, extend=self.extend, format=autocolorbarformat((self.vmin, self.vmax)))
                else:
                    cb=plotw.fig.colorbar(sm, cax=self.quatcompclass.cbax, extend=self.extend, format=autocolorbarformat((self.vmin, self.vmax)))
                cb.set_label(self.fomplotd['fomname'])
        plotw.fig.canvas.draw()
        return self.quatcompclass.toComp
    
    def setup_TabWidget(self, oldopts, newopts, compbool=False):
        if compbool:
            geom=self.plottabgeom_comp
            tabw=self.compTabWidget
            l=self.tabs__plotw_comp
            fcn=self.compclickprocess
        else:
            geom=self.plottabgeom_plate
            tabw=self.plateTabWidget
            l=self.tabs__plotw_plate
            fcn=self.plateclickprocess
        if len(newopts)<len(oldopts):
            for i in range(len(newopts), len(oldopts)):
                tabw.setTabText(i, '')
                tabw.setTabEnabled(i, False)
        elif len(newopts)>len(l):
            for count in range(len(newopts)-len(l)):
                plotw=plotwidget(self)
                plotw.setGeometry(geom)
                if not compbool:
                    plotw.createcbax()
                plotw.axes.set_aspect(1)
                l+=[plotw]
                tabw.addTab(plotw, '')
                QObject.connect(plotw, SIGNAL("genericclickonplot"), fcn)
        for i, val in enumerate(newopts):
            tabw.setTabText(i, str(val))
            tabw.setTabEnabled(i, True)
        self.textBrowser_plate.hide()
        return newopts
    
    def plateclickprocess(self, coords_button_ax):
        if len(self.fomplotd['fom'])==0:
            return
        
        plate=self.fomplotd['plate_id']
        
        tabi=self.plateTabWidget.currentIndex()
        val=self.tabs__plateids[tabi]
        plotw=self.tabs__plotw_plate[tabi]
        inds=numpy.where((plate==val)&numpy.logical_not(numpy.isnan(self.fomplotd['fom'])))[0]
        
        x, y=self.fomplotd['xy'][inds].T
        
        
        if len(x)==0:
            return
        
        critdist=2.
        xc, yc, button, ax=coords_button_ax
        
        dist=((x-xc)**2+(y-yc)**2)**.5

        if min(dist)>critdist:
            return
        self.selectind=inds[numpy.argmin(dist)]#index of the fomplotd arrays

        self.updateinfo()

        if button==3:#right click
            self.addrem_select_fomplotdinds(fomplotdind=self.selectind, remove=False)
        elif button==2:#center click
            self.addrem_select_fomplotdinds(fomplotdind=self.selectind, remove=True)
        self.plotxy()

    def compclickprocess(self, coords_button_ax):
        
        if len(self.fomplotd['fom'])==0:
            return
        
        code=self.fomplotd['code']
        
        
        tabi=self.compTabWidget.currentIndex()
        val=self.tabs__codes[tabi]
        plotw=self.tabs__plotw_comp[tabi]
        inds=numpy.where(((val<0)|(code==val))&numpy.logical_not(numpy.isnan(self.fomplotd['fom'])))[0]
        
        x, y=self.fomplotd['xy'][inds].T
        comps=self.fomplotd['comps'][inds]
        
        if len(x)==0:
            return

        critdist=.1
        xc, yc, button, ax=coords_button_ax
        
        compclick=plotw.toComp(xc, yc, ax)
        if compclick is None:
            return
        
        permcomp=comps[:, self.comppermuteinds]#this comps may be a custom selection of 4 platemap channels according to platemap_comp4plot_keylist, in which case the string permutation selection will not match this
        
        dist=numpy.array([(((c-compclick)**2).sum())**.5 for c in permcomp])

        if min(dist)>critdist:
            return
        self.selectind=inds[numpy.argmin(dist)]

        self.updateinfo()

        if button==3:#right click
            self.addrem_select_fomplotdinds(fomplotdind=self.selectind, remove=False)
        elif button==2:#center click
            self.addrem_select_fomplotdinds(fomplotdind=self.selectind, remove=True)
        self.plotxy()
    
    def clearvisuals(self):
        self.browser.setText('')
        self.fomstatsTextBrowser.setText('')
        self.SummaryTextBrowser.setText('')
        self.expanafilenameLineEdit.setText('')
        for plotw in self.tabs__plotw_plate+self.tabs__plotw_comp:
            plotw.axes.cla()
            plotw.fig.canvas.draw()
        self.tabs__plateids=self.setup_TabWidget(self.tabs__plateids, [-1], compbool=False)
        self.tabs__codes=self.setup_TabWidget(self.tabs__codes, [-1], compbool=True)
        
        self.ellabelsLineEdit.setText('')
        self.platemapfilenameLineEdit.setText('')

        self.plotw_xy.axes.cla()
        self.plotw_xy.twaxes.cla()
        self.plotw_xy.fig.canvas.draw()
        
        self.plotw_fomhist.axes.cla()
        self.plotw_fomhist.fig.canvas.draw()
    def plotwsetup(self):
        self.xyplotstyled=dict({}, marker='o', ms=5, c='b', ls='-', lw=0.7, right_marker='None', right_ms=3, right_ls=':', right_lw=0.7, select_ms=6, select_c='r', right_c='g')
        self.xyplotcolorrotation=['b', 'k', 'm', 'y', 'c','r', 'g']
        self.selectind=None
        self.plottabgeom_comp=self.textBrowser_comp.geometry()
        self.textBrowser_comp.hide()
        
        self.plottabgeom_plate=self.textBrowser_plate.geometry()
        self.textBrowser_plate.hide()
        
        self.tabs__plotw_plate=[]
        self.tabs__plotw_comp=[]
        self.plateTabWidget.removeTab(0)
        self.compTabWidget.removeTab(0)
        self.tabs__plateids=self.setup_TabWidget([], [-1], compbool=False)
        self.tabs__codes=self.setup_TabWidget([], [-1], compbool=True)
        

        self.plotw_xy=plotwidget(self)
        self.plotw_xy.twaxes=self.plotw_xy.axes.twinx()

        self.plotw_fomhist=plotwidget(self)
        
        
        
        for b, w in [\
            (self.textBrowser_xy, self.plotw_xy), \
            (self.textBrowser_fomhist, self.plotw_fomhist), \
            ]:
            w.setGeometry(b.geometry())
            b.hide()

        self.plotw_xy.fig.subplots_adjust(left=.22, bottom=.17)
        
        self.quatcompclass=quatcompplotoptions(None, self.CompPlotTypeComboBox, plotw3d=None, include3doption=True, plotwcbaxrect=[0.88, 0.1, 0.04, 0.8])
        
    def updateinfo(self):
        self.compLineEdit.setText(','.join(['%.2f' %n for n in self.fomplotd['comps'][self.selectind]]))

        self.xyLineEdit.setText(','.join(['%.2f' %n for n in self.fomplotd['xy'][self.selectind]]))

        self.sampleLineEdit.setText('%d' %self.fomplotd['sample_no'][self.selectind])
    
    #selectind is of the fomplotd arrays. add or remove is only if found in fomplotd, when adding to spreadsheet use (plate,sample,run,ana) as index
    def addrem_select_fomplotdinds(self, remove=False, fomplotdind=None, smplist=None, xy=None, comp=None):#only 1 of index, smplist, xy, comp should be not None
        selectinds=[]
        if not fomplotdind is None:
            selectinds=[fomplotdind]
        elif not smplist is None:
            selectinds=[count for count, smp in enumerate(self.fomplotd['sample_no']) if smp in smplist]
        elif not xy is None or not comp is None:
            if not xy is None:
                k='xy'
                arr=numpy.array(xy)
            else:
                k='comps'
                arr=numpy.array(comp)
            xy=numpy.array(xy)
            dist=numpy.array([((numpy.array(xyv)-arr)**2).sum() for xyv in self.fomplotd[k]])
            selectinds=list(numpy.where(dist==dist.min())[0])
        if len(selectinds)==0:
            return
        self.selectind=selectinds[-1]
        #make id tup as the pair fo indeces that points to a particular fomd in l_fomdlist
        idtupset=set([tuple([self.fomplotd[k][i] for k in ['fomdlist_index0','fomdlist_index1']]) for i in selectinds])
        if remove:
            tupstoremove=list(set(self.select_idtups).intersection(idtupset))
            indstoremove=sorted([self.select_idtups.index(tup) for tup in tupstoremove])[::-1]
            if len(indstoremove)==0:
                return
            for i in indstoremove:
                self.select_idtups.pop(i)
                circ, plotw=self.select_circs_plotws.pop(i)
                if not circ is None:
                    circ.remove()
                    plotw.fig.canvas.draw()
        else:
            tupstoadd=sorted(list(idtupset.difference(set(self.select_idtups))))
            if len(tupstoadd)==0:
                return
            for tup in tupstoadd:
                self.select_idtups+=[tup]
                self.select_circs_plotws+=[self.drawcirc_idtup(tup)]
        self.writeselectbrowsertext()
        
    
    def drawcirc_idtup(self, idtup):
        idtupsarr=numpy.array([self.fomplotd['fomdlist_index0'],self.fomplotd['fomdlist_index1']]).T
        idtuplist=[tuple(a) for a in idtupsarr]
        if not idtup in idtuplist:#not sure why this would be but just in case
            return None, None
        
        i_fomplotd=idtuplist.index(idtup)
        i_tabs=self.tabs__plateids.index(self.fomplotd['plate_id'][i_fomplotd])
        plotw=self.tabs__plotw_plate[i_tabs]
        circ = pylab.Circle(self.fomplotd['xy'][i_fomplotd], radius=1, edgecolor='r', facecolor='none')
        plotw.axes.add_patch(circ)
        plotw.fig.canvas.draw()
        return (circ, plotw)
                
    def writeselectbrowsertext(self):
        sorthelp=['plate_id', 'sample_no', 'runint', 'anaint', 'code']+self.ellabels+['x', 'y']
        gensortind=lambda k: sorthelp.index(k) if k in sorthelp else len(sorthelp)
        sortind_k=sorted(list(set([(gensortind(k), k) for i0, i1 in self.select_idtups for k in self.l_fomnames[i0]])))
        keys=map(operator.itemgetter(1), sortind_k)
        
        strfmt=lambda x: ('%d' if isinstance(x, int) else ('%.3f' if (x==0. or (x<1000. and x>.04)) else '%.4e')) %x
        genstrlist_inds=lambda i0, i1: [strfmt(self.l_fomdlist[i0][i1][k]) if k in self.l_fomdlist[i0][i1].keys() else 'NaN' for k in keys]
            
        lines=['\t'.join(keys)]
        lines+=['\t'.join(genstrlist_inds(i0, i1)) for i0, i1 in self.select_idtups]
        selectsamplesstr='\n'.join(lines)
        
        self.browser.setText(selectsamplesstr)
        
    def addValuesSample(self, remove=False):
        sampleNostr = str(self.sampleLineEdit.text())

        try:
            if ',' in sampleNostr:
                smplist=eval('['+sampleNostr+']')
            else:
                smplist=[int(eval(sampleNostr.strip()))]
        except:
            print 'error adding samples'
            return
        self.addrem_select_fomplotdinds(smplist=smplist, remove=remove)
    
    def remValuesSample(self):
        self.addValuesSample(remove=True)
        
    def addValuesComp(self, remove=False):
        compstr = str(self.compLineEdit.text())
        try:
            abcd=numpy.array(eval('['+compstr.strip()+']'))
            if abcd.sum()<=0.:
                raise
            abcd/=abcd.sum()
        except:
            print 'error adding composition'
            return
        self.addrem_select_fomplotdinds(comp=abcd, remove=remove)
        
    def remValuesComp(self):
        self.addValuesComp(remove=True)

    def addValuesXY(self, remove=False):
        xystr = str(self.xyLineEdit.text())
        try:
            xy=numpy.array(eval('['+xystr.strip()+']'))
        except:
            print 'error adding x,y'
            return
        self.addrem_select_fomplotdinds(xy=xy, remove=remove)

    def remValuesXY(self):
        self.addValuesXY(remove=True)
    
    def getxystyle_user(self):
        inputs=[(k, type(v), str(v)) for k, v in self.xyplotstyled.iteritems() if not (k.startswith('right_') or k.startswith('select_'))]
        inputs+=[(k, type(v), str(v)) for k, v in self.xyplotstyled.iteritems() if k.startswith('select_')]
        inputs+=[(k, type(v), str(v)) for k, v in self.xyplotstyled.iteritems() if k.startswith('right_')]
        ans=userinputcaller(self, inputs=inputs, title='Enter x-y plot parameters',  cancelallowed=True)
        if ans is None:
            return
        self.xyplotstyled=dict([(tup[0], v) for tup, v in zip(inputs, ans)])
        
    def savefigs(self, save_all_std_bool=False, batchidialog=None, lastbatchiteration=False, filenamesearchlist=None):
        cbl=[\
                self.xplotchoiceComboBox, \
                self.yplotchoiceComboBox, \
                self.rightyplotchoiceComboBox, \
                ]
        x_y_righty=[str(cb.currentText()) for cb in cbl if str(cb.currentText())!='None']

        mainitem=self.widgetItems_pl_ru_te_ty_co[0]
        plateid_dict_list=[(str(val), {'plotw':plotw, 'checked':\
                   (True in [bool(mainitem.child(i).checkState(0)) for i in range(mainitem.childCount()) if str(val)==str(mainitem.child(i).text(0)).strip()])\
                        })\
                        for val, plotw in zip(self.tabs__plateids, self.tabs__plotw_plate)]
        print [(bool(mainitem.child(i).checkState(0)), str(val), str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount())]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
        code_dict_list=[(str(val), {'plotw':plotw, 'checked':\
                   (True in [bool(mainitem.child(i).checkState(0)) for i in range(mainitem.childCount()) if str(val)==str(mainitem.child(i).text(0)).strip()])\
                        })\
                        for val, plotw in zip(self.tabs__codes, self.tabs__plotw_comp)]
        print [(bool(mainitem.child(i).checkState(0)), str(val), str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount())]


        xyplotw=None if save_all_std_bool else self.plotw_xy 
        idialog=saveimagesDialog(self, self.anafolder, self.fomplotd['fomname'], plateid_dict_list=plateid_dict_list, code_dict_list=code_dict_list, histplow=self.plotw_fomhist, xyplotw=xyplotw, x_y_righty=x_y_righty, repr_anaint_plots=self.repr_anaint_plots, selectsamplebrowser=self.browser, filenamesearchlist=filenamesearchlist)
        
        anaklist_activeplots=[self.l_csvheaderdict[i0]['anak'] for i0 in self.fomplotd['fomdlist_index0']]
        if len(set(anaklist_activeplots))==1:# if all the FOMs in active plot are from the same ana__ then use that as prepend string ni filenames of images
            idialog.prependfilenameLineEdit.setText(anaklist_activeplots[0]+'-')
        if save_all_std_bool:
            if not batchidialog is None:
                idialog.updateoptionsfrombatchidialog(batchidialog, lastbatchiteration=lastbatchiteration)
            idialog.ExitRoutine()
            if idialog.newanapath and lastbatchiteration:
                self.importana(p=idialog.newanapath)
        else:
            idialog.exec_()
            if idialog.newanapath:
                self.importana(p=idialog.newanapath)
    
    def save_all_std_plots(self):
        if 'copied' in os.path.split(self.anafolder)[1]:
            idialog=messageDialog(self, 'Cannot batch-save plots on a .copied folder. Save a single plot first then batch.')
            idialog.exec_()
            return
        comboind_strlist=[]
        for i in range(1, self.numStdPlots+1):
            self.stdcsvplotchoiceComboBox.setCurrentIndex(i)
            comboind_strlist+=[(i, str(self.stdcsvplotchoiceComboBox.currentText()))]
        if len(comboind_strlist)==0:
            idialog=messageDialog(self, 'No Standard plots found, nothing saved')
            idialog.exec_()
            return
        batchidialog=saveimagesbatchDialog(self, comboind_strlist)
        batchidialog.exec_()
        loadstyleoptions= not batchidialog.plotstyleoverrideCheckBox.isChecked()
        
        cbinds=batchidialog.selectcomboboxinds
        for i in cbinds:
            self.stdcsvplotchoiceComboBox.setCurrentIndex(i)
            self.plot_preparestandardplot(loadstyleoptions=loadstyleoptions)
            filenamesearchlist=str(batchidialog.filenamesearchLineEdit.text()).split(',')
            filenamesearchlist=[s.strip() for s in filenamesearchlist if len(s.strip())>0]
            filenamesearchlist=None if len(filenamesearchlist)==0 else filenamesearchlist
            self.savefigs(save_all_std_bool=True, batchidialog=batchidialog, filenamesearchlist=filenamesearchlist, lastbatchiteration=(i==cbinds[-1]))#for std plots all foms will be from same ana__  and prepend str will be filled in automatically

if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.visui=visdataDialog(self, title='Visualize ANA, EXP, RUN data', **kwargs)
#            p=r'\\htejcap.caltech.edu\share\home\processes\analysis\temp\20150909.230012.done\20150909.230012.ana'
#            self.visui.importana(p=p)
#            self.visui.plotfom()
            if execute:
                self.visui.exec_()

    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
    
