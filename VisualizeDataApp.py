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
        
        
        button_fcn=[\
        (self.FolderPushButton, self.openontheflyfolder), \
        (self.UpdateFolderPushButton, self.updateontheflydata), \
        (self.FilenameFilterPushButton, self.createfilenamefilter), \

        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
            
        mainitem=QTreeWidgetItem(['plate'], 0)
        self.SelectTreeWidget.addTopLevelItem(mainitem)
        self.SelectTreeWidget.setCurrentItem(mainitem)
        self.SelectTreeFileFilterTopLevelItem=None
        for k in ['2341', '3452', '56785']:
            item=QTreeWidgetItem([k], 0)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
            
            mainitem.addChild(item)
        mainitem.setExpanded(True)
        QObject.connect(self.SelectTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        
        QObject.connect(self.fomplotchoiceComboBox,SIGNAL("activated(QString)"),self.fomselect)
        self.fomplotchoiceComboBox.insertItem(999,'sdfg')
        #self.select_plateruncode_dict
        
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
        
        
        
    def openontheflyfolder(self):
        t=mygetdir(self, markstr='folder for on-the-fly analysis')
        if t is None or len(t)==0:
            return
            
        p=mygetopenfile(parent=self, markstr='select platemap .txt')
        if p is None or p=='':
            return
            
        self.expfolder=t
        self.platemappath=p
        
        self.lastmodtime=0
        self.expfolder=''
        self.expfiledict={}
        self.expfiledict['run__1']={}
        self.expfiledict['run__1']['run_path']=self.expfolder
        self.updateontheflydata()
    
    def updateontheflydata(self):
        self.lastmodtime=createontheflyrundict(self.expfiledict, self.expfolder, lastmodtime=self.lastmodtime)
        

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
        self.fomdlist=self.analysisclass.fomdlist
        self.fomnames=self.analysisclass.fomnames
        self.csvheaderdict=self.analysisclass.csvheaderdict#this contains default plot info
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
        
        #self.updateana()
        self.plot_preparestandardplot(plotbool=False)
        self.plot_generatedata(plotbool=True)
  
    def processclick_selecttreeitem(self, item, column):
        parent=item.parent()
        if parent is None:
            return
        k1, k2=str(parent.text(0)), int(str(item.text(column)))
        ch=bool(item.checkState(0))
        if ch != self.select_plateruncode_dict[k1][k2]:
            self.select_plateruncode_dict[k1][k2]=ch
            self.plot()
            
    
    def fomselect(self):
#        fi=self.fomplotchoiceComboBox.currentIndex()
#        fom=numpy.array([d[self.fomnames[fi]] for d in self.fomdlist])
#        
        #self.fom=numpy.random.rand(100)**3
        self.fomstats()
        #self.plot_generatedata()
        
    def fomstats(self):
        tempfmt=lambda x:('%.2e' if x>999. else ('%.4f' if x>.009 else '%.2e')) %x
        strarr=[]
        for fcn in [numpy.mean, numpy.median, numpy.std, numpy.min, numpy.max, .05, .1, .9, .95]:
            if isinstance(fcn, float):
                strarr+=[[('%d' %(fcn*100))+'%', tempfmt(numpy.percentile(self.fom, fcn*100))]]
            else:
                strarr+=[[fcn.func_name, tempfmt(fcn(self.fom))]]
        strarr=numpy.array(strarr)
        s='\n'.join(['\t'.join([v for v in a]) for a in strarr])
        self.fomstatsTextBrowser.setText(s)
        
        n, bins, patches = self.plotw_fomhist.axes.hist(self.fom, 20, normed=False, histtype='stepfilled')
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
    
