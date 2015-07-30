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
        
        button_fcn=[\
        (self.AnaPushButton, self.importana), \
        (self.ExpPushButton, self.importexp), \
        (self.FolderPushButton, self.openontheflyfolder), \
        (self.UpdateFolderPushButton, self.updateontheflydata), \
        (self.FilenameFilterPushButton, self.createfilenamefilter), \
        (self.UpdateFiltersPushButton, self.updatefiltereddata), \

        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        self.widgetItems_pl_ru_te_ty_co=[]
        for k in ['plateid', 'run', 'technique', 'type']:
            mainitem=QTreeWidgetItem([k], 0)
            self.SelectTreeWidget.addTopLevelItem(mainitem)
            self.widgetItems_pl_ru_te_ty_co+=[mainitem]
        self.SelectTreeFileFilterTopLevelItem=None

        #QObject.connect(self.SelectTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        QObject.connect(self.AnaExpFomTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        
        QObject.connect(self.fomplotchoiceComboBox,SIGNAL("activated(QString)"),self.filterandplotfomdata)
        self.fomplotchoiceComboBox.insertItem(999,'sdfg')

        
        for count, c in enumerate(AnalysisClasses):
            self.OnFlyAnaClassComboBox.insertItem(count, c.analysis_name)
            
        self.plotwsetup()
    
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
    
    def importana(self):
        p=mygetopenfile(parent=self, xpath="%s" % os.getcwd(),markstr='Select .ana/.pck to import')
        if len(p)==0:
            return
        self.anadict=openana(p, stringvalues=False, erroruifcn=None)#don't allow erroruifcn because dont' want to clear temp ana folder until exp successfully opened and then clearanalysis and then copy to temp folder, so need the path defintion to be exclusively in previous line
        self.importexp(exppath=self.anadict['exp_path'])
        self.anadict=anadict
        self.anafolder=os.path.split(p)[0]
        
    def importexp(self, exppath=None):
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
        for runk, rund in self.expfiledict.iteritems():
            if runk.startswith('run__') and not 'platemapdlist' in rund.keys()\
                     and 'parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
                     and 'plate_id' in rund['parameters'].keys():
                rund['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(rund['parameters']['plate_id']), \
                    erroruifcn=\
                lambda s:mygetopenfile(parent=self, xpath="%s" % os.getcwd(), markstr='Error: %s select platemap for plate_no %s' %(s, rund['parameters']['plate_id'])))
                rund['platemapsamples']=[d['sample'] for d in rund['platemapdlist']]
        self.setupfilterchoices()
        self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)
        
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
            for k in ['plate_id', 'runint', 'code']:
                if not k in fomnames:
                    fomnames+=[k]
            for d in fomdlist:
                if not 'plate_id' in d.keys():
                    d['plate_id']=0
                if not 'runint' in d.keys():
                    d['runint']=0
                if not 'code' in d.keys():
                    if d['runint']==0 or (not 'sample_no' in d.keys) or d['sample_no']<=0:
                        d['code']=-1
                    else:
                        rund=self.expfiledict['run__%d' %d['runint']]
                        d['code']=rund['platemapdlist'][rund['platemapsamples'].index(d['sample_no'])]['code']
        
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
        else:
            d=self.expfiledict
        filed=d_nestedkeys(d, keylist)
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
        #self.l_usefombool+=[True]
        self.updatefomdlist_plateruncode(inds=[-1])
        self.AnaExpFomTreeWidgetFcns.appendFom(self.l_fomnames[-1], self.l_csvheaderdict[-1], clear=False)
        self.setupfilterchoices()
        self.updatefomplotchoices()
    
    def filterandplotfomdata(self, plotbool=True):
        mainitem=self.widgetItems_pl_ru_te_ty_co[0]
        plateidallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[1]
        runintallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
        codeallowedvals=[int(str(mainitem.child(i).text(0)).strip()) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
        fomname=str(self.fomplotchoiceComboBox.currentText())

        l_usefombool=self.AnaExpFomTreeWidgetFcns.getusefombools()
        
        plotdinfo=[]
        for usebool, fomdlist, fomnames in zip(l_usefombool, self.l_fomdlist, self.l_fomnames):
            if not usebool or not fomname in fomnames:
                continue
            plotdinfo+=[extractplotdinfo(d, fomname) for d in dlist if fomname in d.keys() and not numpy.isnan(d[fomname]) and d['plateid'] in plateidallowedvals and d['runint'] in runintallowedvals and d['code'] in codeallowedvals]
        for count, k in enumerate(['plateid','code','sample_no', 'fom', 'xy', 'comp']):
            self.fomplotd[k]=numpy.array(map(operator.itemgetter(count), plotdinfo))
        self.fomplotd['comp']=numpy.array([c/c.sum() for c in self.fomplotd['comp']])
        self.fomplotd['fomname']=fomname
        
        if plotbool:
            self.fomstats()
            self.plot()
        
    def updatefomplotchoices(self)
        self.fomplotchoiceComboBox.clear()
        self.stdcsvplotchoiceComboBox.clear()
        self.fomselectnames=sorted(list(set([nam for fomnames in self.l_fomnames for nam in fomnames])))
        if len(self.fomselectnames)==0:
            return
        for count, s in enumerate(self.fomselectnames):
            self.fomplotchoiceComboBox.insertItem(count, s)#fom choices are not associated with particular indeces of the l_ structures
        self.fomplotchoiceComboBox.setCurrentIndex(0)

        
        self.stdcsvplotchoiceComboBox.insertItem(0, 'null')
        tuplist=[(count, k) for count, csvheaderdict in enumerate(self.l_csvheaderdict) if 'plot_parameters' in csvheaderdict.keys() and 'plot__1' in csvheaderdict['plot_parameters'].keys()]
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

        self.fomplotchoiceComboBox.setCurrentIndex(self.fomnames.index(d['fom_name']))
        for k, le in [('colormap', self.colormapLineEdit), ('colormap_over_color', self.aboverangecolLineEdit), ('colormap_under_color', self.belowrangecolLineEdit)]:
            if not k in d.keys():
                continue
            le.setText(d[k])
        if 'colormap_min_value' in d.keys() and 'colormap_max_value' in d.keys():
            self.vminmaxLineEdit.setText('%s,%s' %(d['colormap_min_value'], d['colormap_max_value']))
        if plotbool:
            self.filterandplotfomdata(plotbool=True)
            
    def fomstats(self):
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
        
    def plotwsetup(self):
        
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
#        self.quatcompclass=quatcompplotoptions(self.plotw_comp, self.CompPlotTypeComboBox, plotw3d=self.plotw_quat3d, plotwcbaxrect=axrect)
        
        
#        self.browserdirmodel.hide()
#        self.browserdirmodel = QtGui.QTextBrowser(Dialog)
#        self.browserdirmodel.setGeometry(QtCore.QRect(220, 40, 291, 271))
#        
#
#        self.plateTabWidget
#        self.textBrowser_plate
#        self.AnaTreeWidget
#        self.textBrowser_xy
#        self.textBrowser_comp
#        self.compTabWidget
#        self.browser
#        self.FolderPushButton
#        self.AnaPushButton
#        self.ExpPushButton
#        self.UpdateFolderPushButton
#        self.OnFlyAnaClassComboBox
#        self.OnFlyStoreInterCheckBox 
#        self.compLineEdit
#        self.xyLineEdit 
#        self.sampleLineEdit
#        self.addComp 
#        self.remComp
#        self.remxy
#        self.addxy
#        self.remSample
#        self.addSample
#        self.fomplotchoiceComboBox
#        self.CompPlotTypeComboBox
#        self.stdcsvplotchoiceComboBox
#        self.compplotsizeLineEdit
#        self.belowrangecolLineEdit
#        self.colormapLineEdit
#        self.vminmaxLineEdit 
#        self.CompPlotOrderComboBox
#        self.aboverangecolLineEdit
#        self.rightyplotchoiceComboBox 
#        self.yplotchoiceComboBox
#        self.xplotchoiceComboBox 
#        self.customxylegendPushButton 
#        self.overlayselectCheckBox 
#        self.browserdirmodel = QtGui.QTextBrowser(Dialog)
#        self.browserdirmodel.setGeometry(QtCore.QRect(220, 40, 291, 271))
#        self.browserdirmodel.setObjectName(_fromUtf8("browserdirmodel"))



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.visui=visdataDialog(self, title='Visualize ANA, EXP, RUN data', **kwargs)
            if execute:
                self.visui.exec_()
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
    
