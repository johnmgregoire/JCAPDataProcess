
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
from SaveImagesForm import Ui_SaveImagesDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'





cbl=[\
        self.xplotchoiceComboBox, \
        self.yplotchoiceComboBox, \
        self.rightyplotchoiceComboBox, \
        ]
arrkeys=[str(cb.currentText()) for cb in cbl]

self.fomplotd['fomname']


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

        allowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
        
class saveimagesDialog(QDialog, Ui_SaveImagesDialog):
    def __init__(self, parent, anafolder, fomname, plateid_dict_list=[], code_dict_list=[], x_y_righty=['x', 'y', '']):
        super(saveimagesDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
        self.plateid_dict_list=plateid_dict_list
        self.code_dict_list=code_dict_list
        
        QObject.connect(self.FilesTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.editname)
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    
        self.widgetItems={}
        self.widgetkeys=['plate_id','code', 'xy', 'hist']
        for k in self.widgetkeys:
            mainitem=QTreeWidgetItem([k], 0)
            self.FilesTreeWidget.addTopLevelItem(mainitem)
            self.widgetItems[k]=mainitem
        
        self.xyyname='-'.join([k for k in x_y_righty if len(k)>0])
        self.fomname=fomname
        
        for widgk, val_dict_list in zip(self.widgetkeys, [self.plateid_dict_list, self.code_dict_list]):
            mainitem=self.widgetItems[widgk]
            for (k, d) in val_dict_list:
                s='%s__%s-%s.png: fom_visualizer_png_image' %(widgk, k, self.fomname)
                item=QTreeWidgetItem([s], 0)
                item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Checked if checkbool else Qt.Unchecked)
                mainitem.addChild(item)
                d['item']=item
                
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
        
    def ExitRoutine(self):
        overbool=self.overwriteCheckBox.isChecked()
        


SaveImagesDialog
i_tabs=self.tabs__plateids.index(self.fomplotd['plate_id'][i_fomplotd])
        plotw=self.tabs__plotw_plate[i_tabs]
        

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
            
            
            
allowedvals=[str(mainitem.child(i).text(0)).strip() for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]

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
        
        
