import time, itertools
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
from VisualizeAuxFcns import *
from VisualizeDataForm import Ui_VisDataDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'

from CalcFOMApp import AnalysisClasses



class visdataDialog(QDialog, Ui_VisDataDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(visdataDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
        
        #self.SelectTreeView.setModel(CheckableDirModel(self))
        self.AnaExpFomTreeWidgetFcns=treeclass_anaexpfom(self.AnaExpFomTreeWidget)
        self.OnFlyStoreInterCheckBox.setEnabled(False)
        button_fcn=[\
        (self.AnaPushButton, self.importana), \
        (self.ExpPushButton, self.importexp), \
        (self.FolderPushButton, self.openontheflyfolder), \
        (self.UpdateFolderPushButton, self.updateontheflydata), \
        (self.FilenameFilterPushButton, self.createfilenamefilter), \
        (self.UpdateFiltersPushButton, self.updatefiltereddata), \
        (self.UpdatePlotPushButton, self.plotfom), \
        (self.addComp, self.addValuesComp), \
        (self.remComp, self.remValuesComp), \
        (self.addxy, self.addValuesXY), \
        (self.remxy, self.remValuesXY), \
        (self.addSample, self.addValuesSample), \
        (self.remSample, self.remValuesSample), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        self.widgetItems_pl_ru_te_ty_co=[]
        for k in ['plate_id', 'run', 'technique', 'type']:
            mainitem=QTreeWidgetItem([k], 0)
            self.SelectTreeWidget.addTopLevelItem(mainitem)
            self.widgetItems_pl_ru_te_ty_co+=[mainitem]
        self.SelectTreeFileFilterTopLevelItem=None

        #QObject.connect(self.SelectTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        QObject.connect(self.AnaExpFomTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        
        QObject.connect(self.fomplotchoiceComboBox,SIGNAL("activated(QString)"), self.updatefomchoiceandplot)

        QObject.connect(self.compPlotMarkSelectionsCheckBox,SIGNAL("released()"), self.plotfom)
        
        for count, c in enumerate(AnalysisClasses):
            self.OnFlyAnaClassComboBox.insertItem(count, c.analysis_name)
            
        self.plotwsetup()
        
        self.l_fomdlist=[]
        self.l_fomnames=[]
        self.l_csvheaderdict=[]
        
        self.anafiledict={}
        self.expfiledict={}
        
        
        
        self.ellabels=['A', 'B', 'C', 'D']
        
        
        self.clearfomplotd()
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
    
    def importana(self, p=None):
        if p is None:
            p=mygetopenfile(parent=self, xpath="%s" % os.getcwd(),markstr='Select .ana/.pck to import')
        if len(p)==0:
            return
        self.anafiledict=openana(p, stringvalues=False, erroruifcn=None)
        self.anafolder=os.path.split(p)[0]
        

        
        self.importexp(exppath=self.anafiledict['exp_path'], fromana=True)
        
        self.l_fomdlist=[]
        self.l_fomnames=[]
        self.l_csvheaderdict=[]

        #this fcn appends all ana fom files to the l_ structures and append to Fom item in tree
        readandformat_anafomfiles(self.anafolder, self.anafiledict, self.l_fomdlist, self.l_fomnames, self.l_csvheaderdict, self.AnaExpFomTreeWidgetFcns)
        
        self.updatefomdlist_plateruncode()
        
        self.setupfilterchoices()
        self.updatefomplotchoices()

        
        
    def importexp(self, exppath=None, fromana=False):
        if exppath is None:
            exppath=mygetopenfile(self, xpath=os.path.join(os.getcwd(), 'experiment'), markstr='Select .pck or .exp EXP file', filename='.pck' )
        if exppath is None or len(exppath)==0:
            return
        expfiledict=readexpasdict(exppath, includerawdata=False, erroruifcn=None)
        if expfiledict is None:
            print 'Problem opening EXP'
            return
#        self.clearexp()
        self.exppath=exppath
        self.expfolder=os.path.split(exppath)[0]
        self.expfiledict=expfiledict
        masterels=None
        for runk, rund in self.expfiledict.iteritems():
            if not (runk.startswith('run__') and not 'platemapdlist' in rund.keys()\
                     and 'parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
                     and 'plate_id' in rund['parameters'].keys()):
                masterels=['A', 'B', 'C', 'D']
                continue
            rund['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(str(rund['parameters']['plate_id']), \
                erroruifcn=\
            lambda s, xpath:mygetopenfile(parent=self, xpath=xpath, markstr='Error: %s select platemap for plate_no %s' %(s, rund['parameters']['plate_id']))))
            rund['platemapsamples']=[d['sample_no'] for d in rund['platemapdlist']]
            els=getelements_plateidstr(str(rund['parameters']['plate_id']))
            if els is None:
                continue
            if len(els)>4:
                els=els[:4]
            if masterels is None:
                masterels=els
            elif masterels==els:
                continue
            elif set(masterels)==set(els):
                idialog=messageDialog(self, 'Modify platemap so %s permuted to match previous plate with elements %s?' %(','.join(els), ','.join(masterels)))
                if idialog.exec_():
                    rund['platemapdlist']=[dict(d, origA=d['A'], origB=d['B'], origC=d['C'], origD=d['D']) for d in rund['platemapdlist']]
                    lets=['A', 'B', 'C', 'D']
                    for d in rund['platemapdlist']:
                        for let, el in zip(lets, masterels):
                            d[let]=d['orig'+lets[els.index(el)]]
                else:
                    masterels=['A', 'B', 'C', 'D']#this will keep any subsequent .exp from matching the masterels
            else:
                idialog=messageDialog(self, 'WARNING: plate_ids with incommensurate elements have been added')
                idialog.exec_()
                masterels=['A', 'B', 'C', 'D']
        if masterels is None or masterels==['A', 'B', 'C', 'D']:
            self.ellabels=['A', 'B', 'C', 'D']
        else:#to get here evrythign has a platemap
            self.ellabels=masterels+['A', 'B', 'C', 'D'][len(masterels):]
            for runk, rund in self.expfiledict.iteritems():
                for d in rund['platemapdlist']:
                    for oldlet, el in zip(['A', 'B', 'C', 'D'], self.ellabels):
                        d[el]=d[oldlet]

        self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)
        self.fillcomppermutations()
        if not fromana:
            self.setupfilterchoices()
            self.updatefomplotchoices()
        self.clearfomplotd()
        
    def openontheflyfolder(self):
        t=mygetdir(self, markstr='folder for on-the-fly analysis')
        if t is None or len(t)==0:
            return
            
        p=mygetopenfile(parent=self, markstr='select platemap .txt')
        if p is None or p=='':
            return
            
        self.expfolder=t
        self.platemappath=p#this is self. but probably not necessary because not used elsehwere after being read below
        
        self.lastmodtime=0
        self.expfolder=''
        self.expfiledict={}
        self.expfiledict['run__1']={}
        self.expfiledict['run__1']['run_path']=self.expfolder
        self.expfiledict['run__1']['platemapdlist']=readsingleplatemaptxt(self.platemappath)
        self.expfiledict['run__1']['platemapsamples']=[d['sample'] for d in self.expfiledict['run__1']['platemapdlist']]
        self.expfiledict['run__1']['files_technique__onthefly']={}
        self.expfiledict['run__1']['files_technique__onthefly']['all_files']={}
        self.expfiledict['run__1']['parameters']={}
        self.expfiledict['run__1']['parameters']['plate_id']=0
        
        self.updateontheflydata()
        self.anafiledict={}
        self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)
        
        self.ellabels=['A', 'B', 'C', 'D']
        self.fillcomppermutations()
        self.clearfomplotd()
        
    def updateontheflydata(self):
        #this treates all files in the folder the same and by doing so assumes each file is a measurement on s asample. this could read a .csv fom file but it would be sample_no=nan and would not be ported to self.fomdlist. that is tricky and could be done but not necessary if "on-the-fly" is used for a raw data stream.
        self.lastmodtime, d_appended=createontheflyrundict(self.expfiledict, self.expfolder, lastmodtime=self.lastmodtime)
        self.setupfilterchoices()
        self.AnaExpFomTreeWidgetFcns.appendexpfiles(d_appended)
        

    #filters for exp file:
    #  run defines a run__ within exp and this is by defintion for only 1 plate_id so filtering by code happens subsequently
    #  plate_id defines a subset of runs within exp and similarly filtering by code happens subsequently
    #  code defines a subset of samples within each run
    #filters for ana file:
    #  ana defines an ana__ with ana and this may contain multipl runs/plate_ids but fom .csv within the ana__ have run and plate_id integers for subsequenct filtering and then code filtering after that
    
    def updatefomdlist_plateruncode(self, inds=None):
        if inds is None:
            inds=range(len(self.l_fomdlist))
        for ind in inds:
            fomdlist=self.l_fomdlist[ind]
            fomnames=self.l_fomnames[ind]

            for d in fomdlist:
                if not 'plate_id' in d.keys():
                    d['plate_id']=0
                    fomnames+=['plate_id']
                if not 'runint' in d.keys():
                    d['runint']=0
                    fomnames+=['runint']
                if not 'anaint' in d.keys():
                    d['anaint']=0
                    fomnames+=['anaint']
                if not 'code' in d.keys() and (d['runint']==0 or (not 'sample_no' in d.keys()) or d['sample_no']<=0):
                    d['code']=-1
                    fomnames+=['code']
                if not (d['runint']==0 or (not 'sample_no' in d.keys()) or d['sample_no']<=0):
                    rund=self.expfiledict['run__%d' %d['runint']]
                    pmd=rund['platemapdlist'][rund['platemapsamples'].index(d['sample_no'])]
                    for k in self.ellabels+['code', 'x', 'y']:
                        if not k in d.keys():
                            d[k]=pmd[k]
                            fomnames+=[k]
        
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
        keylist=[s.strip('*')]
        item=item.parent()
        while not item.parent() is None:
            keylist=[str(item.text(0))]+keylist
            item=item.parent()
        anaorexp=str(item.text(0))
        if anaorexp=='ana':
            d=self.anafiledict
            p=os.path.join(self.anafolder, keylist[-1])
        else:
            d=self.expfiledict
            p=os.path.join(self.expfolder, keylist[-1])
        filed=d_nestedkeys(d, keylist)
        filed['path']=p
        self.plotxy(filed=filed)
        #TODO: how does x-y plotting work? use this filed to do it
            
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
        self.filteredexpfilekeys=[list(l_keytup)+[filek] for pl, expkeytup in l_keytup for co, filek in zip(self.exp_keys_codearr_dict[(pl, expkeytup)], sorted(d_nestedkeys(self.expfiledict, expkeytup).keys())) if co in allowedvals]
        
        self.filterandplotfomdata()
        #filter ana fom data by plate, run and code
        
        #need to get the codes adn think about how to getapplicablefilesnames, i.e. create filedlist for simple cases, flag analysis classes by 'simple"
    def performontheflyfom(self):
        analysisclass=AnalysisClasses[self.OnFlyAnaClassComboBox.currentIndex()]
        analysisclass.getapplicablefilenames(self.expfiledict, 'onthefly', 'onthefly', 'all_files')
        
        if self.SelectTreeFileFilterTopLevelItem is None:
            searchstrs=[]
        else:
            searchstrs=[str(self.SelectTreeFileFilterTopLevelItem.child(i).text(0)).strip() for i in range(self.SelectTreeFileFilterTopLevelItem.childCount()) if bool(self.SelectTreeFileFilterTopLevelItem.child(i).checkState(0))]
        
        #do the fitlering by search string after gettapplicablefilenames so the "critfracapplicable" might be really low
        analysisclass.filedlist=[d for d in analysisclass.filedlist if not (False in [s in d['fn'] for s in searchstrs])]
        
        checkbool, checkmsg=self.analysisclass.check_input(critfracapplicable=.001)
        if not checkbool:
            idialog=messageDialog(self, 'Continue analysis? '+checkmsg)
            if not idialog.exec_():
                return
        #rawd=readbinaryarrasdict(keys)
        #expdatfolder=os.path.join(self.expfolder, 'raw_binary')

        self.analysisclass.perform(None, expdatfolder=self.expfolder, anak='')
        self.l_fomdlist+=[self.analysisclass.fomdlist]#on-the-fly analysis gets appended to the list of dictionaries, but since opening ana cleans these lists, the l_ structures will start with ana csvs.
        self.l_fomnames+=[self.analysisclass.fomnames]
        self.l_csvheaderdict+=[self.analysisclass.csvheaderdict]#this contains default plot info
        #self.clearfomplotd()  don't need to clear here because all indexes in fomplotd will still work
        #self.l_usefombool+=[True]
        self.updatefomdlist_plateruncode(inds=[-1])
        self.AnaExpFomTreeWidgetFcns.appendFom(self.l_fomnames[-1], self.l_csvheaderdict[-1])
        self.setupfilterchoices()
        self.updatefomplotchoices()
    
    def filterandplotfomdata(self, plotbool=True):
        self.clearfomplotd()
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[0]
        plateidallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[1]
        runintallowedvals=[int(str(mainitem.child(i).text(0)).lstrip('run__')) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
        codeallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        
        fomname=str(self.fomplotchoiceComboBox.currentText())
        compcolorbool=(fomname=='comp. color')
        if compcolorbool:
            fomname='sample_no'
        l_usefombool=self.AnaExpFomTreeWidgetFcns.getusefombools()
        
        plotdinfo=[]
        for fomdlist_index0, (usebool, fomdlist, fomnames) in enumerate(zip(l_usefombool, self.l_fomdlist, self.l_fomnames)):
            if not usebool or not fomname in fomnames:
                continue
            plotdinfo+=[extractplotdinfo(d, fomname, self.expfiledict, fomdlist_index0, fomdlist_index1) for fomdlist_index1, d in enumerate(fomdlist) if fomname in d.keys() and d['plate_id'] in plateidallowedvals and d['runint'] in runintallowedvals and d['code'] in codeallowedvals]#and not numpy.isnan(d[fomname]), don't do this so can do fomname swap without loss of samples
        for count, k in enumerate(['fomdlist_index0','fomdlist_index1','plate_id','code','sample_no', 'fom', 'xy', 'comps']):
            self.fomplotd[k]=numpy.array(map(operator.itemgetter(count), plotdinfo))
        self.fomplotd['comps']=numpy.array([c/c.sum() for c in self.fomplotd['comps']])
        if compcolorbool:
            self.fomplotd['fomname']='comp. color'
        else:
            self.fomplotd['fomname']=fomname
        #if fomname is in multiple l_fomdlist a given sample can be included in fomplotd numerous times. this create ambiguity for selecting samples and the plotted fom colored symbols will overlay each other and only the top one will be visible
        if plotbool:
            self.fomstats()
            self.plotfom()
    
    def updatefomchoiceandplot(self):
        fomname=str(self.fomplotchoiceComboBox.currentText())
        compcolorbool=(fomname=='comp. color')
        if compcolorbool:
            self.fomplotd['fomname']='comp. color'
            self.fomplotd['fom']=self.fomplotd['sample_no']
            return
        self.fomplotd['fomname']=fomname
        self.fomdlist['fom']=numpy.array([self.l_fomdlist[i0][i1][fomname] for i0,i1 in zip(self.fomdlist['fomdlist_index0'], self.fomdlist['fomdlist_index1'])])
        
        self.plotfom()
        
    def updatefomplotchoices(self):
        self.fomplotchoiceComboBox.clear()
        self.stdcsvplotchoiceComboBox.clear()
        self.fomselectnames=sorted(list(set([nam for fomnames in self.l_fomnames for nam in fomnames])))
        if len(self.fomselectnames)==0:
            return
        self.fomplotchoiceComboBox.insertItem(0,'comp. color')
        for count, s in enumerate(self.fomselectnames):
            self.fomplotchoiceComboBox.insertItem(count+1, s)#fom choices are not associated with particular indeces of the l_ structures
        self.fomplotchoiceComboBox.setCurrentIndex(0)

        
        self.stdcsvplotchoiceComboBox.insertItem(0, 'null')
        tuplist=[(count, csvheaderdict) for count, csvheaderdict in enumerate(self.l_csvheaderdict) if 'plot_parameters' in csvheaderdict.keys() and 'plot__1' in csvheaderdict['plot_parameters'].keys()]
        keys=['%d-%s' %(count, k) for count, csvheaderdict in tuplist for k in sorted(csvheaderdict['plot_parameters'].keys()) if k.startswith('plot__') and 'fom_name' in csvheaderdict['plot_parameters'][k].keys() and csvheaderdict['plot_parameters'][k]['fom_name'] in self.fomselectnames]
        for count, s in enumerate(keys):
            self.stdcsvplotchoiceComboBox.insertItem(count+1, s)
#            if len(keys)==0:#not sure of new plots will be created in this app
#                count=-1
#                newk='new plot__1'
#            else:
#                newk='new plot__%d' %(int(keys[-1].partition('__')[2])+1)
#            self.stdcsvplotchoiceComboBox.insertItem(count+1, newk)

        self.stdcsvplotchoiceComboBox.setCurrentIndex(0)
        

    
    def plot_preparestandardplot(self, plotbool=True):
        s=str(self.stdcsvplotchoiceComboBox.currentText())
        if s=='null':
           return
        ind, garb, plotk=s.partition('-')
        ind=int(ind)
        d=self.l_csvheaderdict[ind]['plot_parameters'][plotk]

        self.fomplotchoiceComboBox.setCurrentIndex(self.fomnames.index(d['fom_name'])+1)
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
        
        if len(self.fomplotd['fom'])==0:
            self.fomstatsTextBrowser.setText('')
            return
        tempfmt=lambda x:('%.2e' if x>999. else ('%.4f' if x>.009 else '%.2e')) %x
        strarr=[]
        for fcn in [numpy.mean, numpy.median, numpy.std, numpy.min, numpy.max, .05, .1, .9, .95]:
            if isinstance(fcn, float):
                strarr+=[[('%d' %(fcn*100))+'%', tempfmt(numpy.percentile(self.fomplotd['fom'], fcn*100))]]
            else:
                strarr+=[[fcn.func_name, tempfmt(fcn(self.fomplotd['fom']))]]
        strarr=numpy.array(strarr)
        s='\n'.join(['\t'.join([v for v in a]) for a in strarr])
        self.fomstatsTextBrowser.setText(s)
        n, bins, patches = self.plotw_fomhist.axes.hist(self.fomplotd['fom'], 20, normed=False, histtype='stepfilled')
        #self.plotw_fomhist.fig.setp(patches)
        self.plotw_fomhist.fig.canvas.draw()
    
    def plotxy(self, plotd=None, fomplotdind=None):
        return
                #h plot
#        daqtimebool=self.usedaqtimeCheckBox.isChecked()
#        if daqtimebool:
#            hxarr=self.fomplotd['t']
#            xl='time (s)'
#        else:
#            hxarr=self.fomplotd['sample_no']
#            xl='sample_no'
#        for runk in sorted(self.fomplotd['inds_runk'].keys()):
#            hx=hxarr[self.fomplotd['inds_runk'][runk]]
#            hy=fom[self.fomplotd['inds_runk'][runk]]
#            sinds=numpy.argsort(hx)
#            self.plotw_h.axes.plot(hx[sinds], hy[sinds], '.-', label=runk)
#        leg=self.plotw_h.axes.legend(loc=0)
#        leg.draggable()
#        self.plotw_h.axes.set_xlabel(xl)
#        self.plotw_h.axes.set_ylabel(self.fomplotd['fomname'])
#        autotickformat(self.plotw_h.axes, x=daqtimebool, y=1)
#        self.plotw_h.fig.canvas.draw()
    
    def fillcomppermutations(self):
        if self.ellabels==['A', 'B', 'C', 'D']:
            ans=userinputcaller(self, inputs=[('A', str, 'A'), ('B', str, 'B'), ('C', str, 'C'), ('D', str, 'D')], title='Enter element labels',  cancelallowed=True)
            if not ans is None:
                self.ellabels=[v.strip() for v in ans]
        self.CompPlotOrderComboBox.clear()
        for count, l in enumerate(itertools.permutations(self.ellabels, 4)):
            self.CompPlotOrderComboBox.insertItem(count, ','.join(l))
        self.CompPlotOrderComboBox.setCurrentIndex(0)
        
    def plotfom(self):
        
        if len(self.fomplotd['plate_id'])==0:
            return
        
        newplateids=sorted(list(set(self.fomplotd['plate_id'])))
        if self.tabs__plateids!=newplateids:
            self.tabs__plateids=self.setup_TabWidget(self.tabs__plateids, newplateids, compbool=False)
        
        newcodes=sorted(list(set(self.fomplotd['code'])))
        if self.tabs__codes!=newcodes:
            self.tabs__codes=self.setup_TabWidget(self.tabs__codes, newcodes, compbool=True)

        plate=self.fomplotd['plate_id']
        code=self.fomplotd['code']
        x, y=self.fomplotd['xy'].T
        comps=self.fomplotd['comps']
        fom=self.fomplotd['fom']
        idtupsarr=numpy.array([self.fomplotd['fomdlist_index0'],self.fomplotd['fomdlist_index1']]).T

        if self.fomplotd['fomname']=='comp. color':
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
        self.quatcompclass.ellabels=[self.ellabels[i] for i in self.comppermuteinds]
        
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

        
        
        for val, plotw in zip(self.tabs__codes, self.tabs__plotw_comp):
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
        
    def plateplot(self, plotw, x, y, cols, sm):
        plotw.axes.cla()
        plotw.cbax.cla()
        if len(cols)==0:
            return
        m=plotw.axes.scatter(x, y, c=cols, s=70, marker='s')#, cmap=self.cmap, norm=self.norm)
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
#        plotw.axes.cla()
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
        self.plotxy(fomplotdind=self.selectind)

    def compclickprocess(self, coords_button_ax):
        
        if len(self.fomplotd['fom'])==0:
            return
        
        code=self.fomplotd['code']
        
        
        tabi=self.compTabWidget.currentIndex()
        val=self.tabs__codes[tabi]
        plotw=self.tabs__plotw_comp[tabi]
        inds=numpy.where((code==val)&numpy.logical_not(numpy.isnan(self.fomplotd['fom'])))[0]
        
        x, y=self.fomplotd['xy'][inds].T
        comps=self.fomplotd['comps'][inds]
        
        if len(x)==0:
            return

        critdist=.1
        xc, yc, button, ax=coords_button_ax
        
        compclick=plotw.toComp(xc, yc, ax)
        if compclick is None:
            return
        
        permcomp=comps[:, self.comppermuteinds]
        
        dist=numpy.array([(((c-compclick)**2).sum())**.5 for c in permcomp])

        if min(dist)>critdist:
            return
        self.selectind=inds[numpy.argmin(dist)]

        self.updateinfo()

        if button==3:#right click
            self.addrem_select_fomplotdinds(fomplotdind=self.selectind, remove=False)
        elif button==2:#center click
            self.addrem_select_fomplotdinds(fomplotdind=self.selectind, remove=True)
        self.plotxy(fomplotdind=self.selectind)
            
    def plotwsetup(self):
        
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
        
#        self.plotw_comp=plotwidget(self)
#        self.plotw_quat3d=plotwidget(self, projection3d=True)
#        self.plotw_h=plotwidget(self)
#        self.plotw_plate=plotwidget(self)
        self.plotw_fomhist=plotwidget(self)
        
        
        
        for b, w in [\
#            (self.textBrowser_plate, self.plotw_plate), \
#            (self.textBrowser_h, self.plotw_h), \
#            (self.textBrowser_comp, self.plotw_comp), \
#            (self.textBrowser_comp, self.plotw_quat3d), \
            (self.textBrowser_fomhist, self.plotw_fomhist), \
            ]:
            w.setGeometry(b.geometry())
            b.hide()
#        self.plotw_quat3d.hide()
#
#        self.plotw_plate.axes.set_aspect(1)
#
#        axrect=[0.88, 0.1, 0.04, 0.8]
#
#        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0]-.01)
#        self.cbax_plate=self.plotw_plate.fig.add_axes(axrect)
#
#        self.plotw_quat3d.fig.subplots_adjust(left=0, right=axrect[0]-.01)
#        self.cbax_quat=self.plotw_quat3d.fig.add_axes(axrect)
#
#        self.plotw_h.fig.subplots_adjust(left=.22, bottom=.17)
#        
        self.quatcompclass=quatcompplotoptions(None, self.CompPlotTypeComboBox, plotw3d=None, include3doption=True, plotwcbaxrect=[0.88, 0.1, 0.04, 0.8])
        
    def updateinfo(self):
        self.compLineEdit.setText(','.join(['%.2f' %n for n in self.fomplotd['comps'][self.selectind]]))

        self.xyLineEdit.setText(','.join(['%.2f' %n for n in self.fomplotd['xy'][self.selectind]]))

        self.sampleLineEdit.setText('%d' %self.fomplotd['sample_no'][self.selectind])
    
    #***selectind is of the fomplotd arrays. add or remove is only if found in fomplotd, when adding to spreadsheet use (plate,sample,run,ana) as index
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
            dist=numpy.array([((numpy.array(v)-arr)**2).sum() for xyv in self.fomplotd[k]])
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
    

if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.visui=visdataDialog(self, title='Visualize ANA, EXP, RUN data', **kwargs)
            self.visui.importana(p='//htejcap.caltech.edu/share/home/users/hte/demo_proto/analysis/eche/1/20150716.220140.ana')
            #self.visui.plotfom()
            if execute:
                self.visui.exec_()
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
    
