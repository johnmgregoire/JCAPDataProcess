
import time, itertools, string
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
#import numpy.ma as ma
#import matplotlib.colors as colors
#import matplotlib.cm as cm
#import matplotlib.mlab as mlab
import pylab
import pickle
#from fcns_math import *
from fcns_io import *
from fcns_ui import *
#from VisualizeAuxFcns import *
from SaveImagesForm import Ui_SaveImagesDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'





cbl=[\
        self.xplotchoiceComboBox, \
        self.yplotchoiceComboBox, \
        self.rightyplotchoiceComboBox, \
        ]
x_y_righty=[str(cb.currentText()) for cb in cbl]




mainitem=self.widgetItems_pl_ru_te_ty_co[0]
plateid_dict_list=[(str(val), {'plotw':plotw, 'checked':\
           (True in [bool(mainitem.child(i).checkState(0)) for i in range(mainitem.childCount()) if str(val)==str(mainitem.child(i).text(0)).strip()])\
                })\
                for val, plotw in zip(self.tabs__codes, self.tabs__plotw_comp)]
                
mainitem=self.widgetItems_pl_ru_te_ty_co[-1]
code_dict_list=[(str(val), {'plotw':plotw, 'checked':\
           (True in [bool(mainitem.child(i).checkState(0)) for i in range(mainitem.childCount()) if str(val)==str(mainitem.child(i).text(0)).strip()])\
                })\
                for val, plotw in zip(self.tabs__codes, self.tabs__plotw_comp)]


idialog=saveimagesDialog(self, self.anafolder, self.fomplotd['fomname'], plateid_dict_list=plateid_dict_list, code_dict_list=code_dict_list, histplow=self.plotw_fomhist, xyplotw=self.plotw_xy, x_y_righty=x_y_righty, repr_anaint_plots=self.repr_anaint_plots)
idialog.exec_()

class saveimagesDialog(QDialog, Ui_SaveImagesDialog):
    def __init__(self, parent, anafolder, fomname, plateid_dict_list=[], code_dict_list=[], histplow=None, xyplotw=None, x_y_righty=['x', 'y', ''], repr_anaint_plots=1):
        super(saveimagesDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
        self.plateid_dict_list=plateid_dict_list
        self.code_dict_list=code_dict_list
        self.repr_anaint_plots=repr_anaint_plots
        if '.zip' in anafolder:
            idialog=messageDialog(self, 'Cannot save to ANA because it is in a .zip ')
            idialog.exec_()
            self.reject()
            return
        
        fnl=[fn for fn in os.listdir(anafolder.namelist) if fn.endswith('.ana')]
        if len(fnl)==0:
            idialog=messageDialog(self, 'Cannot save to ANA because no .ana in the folder')
            idialog.exec_()
            self.reject()
            return
        
        self.anafn=fnl[0]
        
        self.anafolder=anafolder
        QObject.connect(self.FilesTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.editname)
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    
        self.widgetTopLevelItems={}
        self.widgetkeys=['plate_id','code', 'xy', 'hist']
        for k in self.widgetkeys:
            mainitem=QTreeWidgetItem([k], 0)
            self.FilesTreeWidget.addTopLevelItem(mainitem)
            self.widgetTopLevelItems[k]=mainitem
        
        self.xyyname='-'.join([k for k in x_y_righty if len(k)>0])
        self.fomname=fomname
        
        self.widget_plow_dlist=[]
        for widgk, val_dict_list in zip(self.widgetkeys[0:2], [self.plateid_dict_list, self.code_dict_list]):
            mainitem=self.widgetTopLevelItems[widgk]
            for (k, d) in val_dict_list:
                s=self.filterchars('%s__%s-%s.png' %(widgk, k, self.fomname))
                s+=': python_visualizer_png_image'
                item=QTreeWidgetItem([s], 0)
                item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Checked if checkbool else Qt.Unchecked)
                mainitem.addChild(item)
                d['item']=item
                self.widget_plow_dlist+=[d]
        for widgk, plotw, lab in zip(self.widgetkeys[2:4], [xyplotw, histplow], [self.xyyname, self.fomname]):
            if plotw is None:
                continue
            d={'plotw':plotw}
            s=self.filterchars('%s__%s.png' %(widgk, lab))
            s+=': python_visualizer_png_image'
            item=QTreeWidgetItem([s], 0)
            item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked if checkbool else Qt.Unchecked)
            mainitem.addChild(item)
            d['item']=item
            self.widget_plow_dlist+=[d]
    def editname(self, item, column):
        if item is None:
            item=widget.currentItem()
        s=str(item.text(column))
        st=s.partition('.png: ')[0]
        v=st[0]
        keepstr=''.join(st[1:])
        ans=userinputcaller(self, inputs=[('filename', str, v)], title='Enter new filename',  cancelallowed=True)
        if ans is None or ans[0].strip()==v:
            return
        ans=ans[0].strip()
        
        item.setText(column,''.join([ans, keepstr]))
    
    def filterchars(self, s):
        valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
        return ''.join([c for c in s if c in valid_chars])
    def ExitRoutine(self):
        overbool=self.overwriteCheckBox.isChecked()
        lines=[]
        for d in self.widget_plow_dlist:
            if not bool(d['item'].checkState(0)):
                continue
            pngfn, garb, pngattr=str(d['item'].text(0)).partition(': ')
            pylab.figure(d['plotw'].fig.number)
            existfns=os.listdir(self.anafolder)
            for fn, a in [(pngfn, pngattr), (pngfn.replace('png', 'eps'), pngattr.replace('png', 'eps'))]:
                if (fn in existfns) and not overbool:
                    i=2
                    while fn in existfns:
                        fn=''.join([fn[:-4], '_%d' %i, fn[-4:]])
                        i+=1
                savep=os.path.join(self.anafolder, fn)
                existfns+=[fn]
                pylab.savefig(savep)
                lines+=[(fn, a)]
        if len(lines)==0:
            return
        p=os.path.join(self.anafolder, self.anafn)
        anadict=readana(p, erroruifcn=None, stringvalues=True, returnzipclass=False)#cannot be a .zip
        d=anadict['ana__%d' %self.repr_anaint_plots]
        d=d['files_multi_run']
        for fn, a in lines:
            d[fn]=a#if fn exists and was overwritten this will jdo nothing or update the attrstr
        anafilestr=strrep_filedict(anadict)
        
        if self.doneCheckBox.isChecked() and os.path.split(self.anafolder)[1].count('.')>1:
            saveana_tempfolder(anafilestr, self.anafolder, erroruifcn=None, skipana=True, anadict=None, savefolder=self.anafolder.rpartition('.')[0]+'.done')
        else:
            with open(p, mode='w') as f:
                f.write(anafilestr)


