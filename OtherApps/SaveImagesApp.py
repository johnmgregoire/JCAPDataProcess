
#import time, itertools, 
import string
import os, os.path
#import sys, shutil
#import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#import operator
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
#from fcns_math import *
from fcns_io import *
from fcns_ui import *
#from VisualizeAuxFcns import *
from SaveImagesForm import Ui_SaveImagesDialog
from SaveImagesBatchForm import Ui_SaveImagesBatchDialog
from fcns_compplots import *
#from quatcomp_plot_options import quatcompplotoptions
matplotlib.rcParams['backend.qt4'] = 'PyQt4'




class saveimagesDialog(QDialog, Ui_SaveImagesDialog):
    def __init__(self, parent, anafolder, fomname, plateid_dict_list=[], code_dict_list=[], histplow=None, xyplotw=None, selectsamplebrowser=None, x_y_righty=['x', 'y', ''], repr_anaint_plots=1, filenamesearchlist=None):
        #filenamesearchlist is nested list, level 0 of filenamesearchlist is OR and level 1 is AND
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
        
        fnl=[fn for fn in os.listdir(anafolder) if fn.endswith('.ana') and not fn.startswith('.')]
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
        self.widgetkeys=['plate_id','code', 'xy', 'hist', 'select_samples_text']
        for k in self.widgetkeys:
            mainitem=QTreeWidgetItem([k], 0)
            self.FilesTreeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(True)
            self.widgetTopLevelItems[k]=mainitem
        
        self.xyyname='-'.join([k for k in x_y_righty if len(k)>0])
        self.fomname=fomname
        if filenamesearchlist is None:
            searchchecker=lambda filen:True#not used in this instance
        else:
            searchchecker=lambda filen:True in [not (False in [searchstr in filen for searchstr in searchlist]) for searchlist in filenamesearchlist]
        
        self.widget_plow_dlist=[]
        for widgk, val_dict_list in zip(self.widgetkeys[0:2], [self.plateid_dict_list, self.code_dict_list]):
            mainitem=self.widgetTopLevelItems[widgk]
            for (k, d) in val_dict_list:
                filen=self.filterchars('%s__%s-%s.png' %(widgk, k, self.fomname))
                s=filen+': python_visualizer_png_image'
                item=QTreeWidgetItem([s], 0)
                item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
                if filenamesearchlist is None:
                    item.setCheckState(0, Qt.Checked if d['checked'] else Qt.Unchecked)
                else:
                    item.setCheckState(0, Qt.Checked if searchchecker(filen) else Qt.Unchecked)
                mainitem.addChild(item)
                d['item']=item
                self.widget_plow_dlist+=[d]
        for widgk, plotw, lab in zip(self.widgetkeys[2:4], [xyplotw, histplow], [self.xyyname, self.fomname]):
            if plotw is None:
                continue
            mainitem=self.widgetTopLevelItems[widgk]
            d={'plotw':plotw}
            filen=self.filterchars('%s__%s.png' %(widgk, lab))
            s=filen+': python_visualizer_png_image'
            item=QTreeWidgetItem([s], 0)
            item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            if filenamesearchlist is None:
                item.setCheckState(0, Qt.Unchecked)
            else:
                item.setCheckState(0, Qt.Checked if searchchecker(filen) else Qt.Unchecked)
            mainitem.addChild(item)
            d['item']=item
            self.widget_plow_dlist+=[d]
        
        self.selectsamplesname=fomname
        self.widget_textbrowser_dlist=[]
        for widgk, browser, lab in zip(self.widgetkeys[4:5], [selectsamplebrowser], [self.selectsamplesname]):
            if browser is None:
                continue
            mainitem=self.widgetTopLevelItems[widgk]
            d={'browser':browser}
            filen=self.filterchars('%s__%s.txt' %(widgk, lab))
            s=filen+': python_visualizer_txt'
            item=QTreeWidgetItem([s], 0)
            item.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            if filenamesearchlist is None:
                item.setCheckState(0, Qt.Unchecked)
            else:
                item.setCheckState(0, Qt.Checked if searchchecker(filen) else Qt.Unchecked)
            mainitem.addChild(item)
            d['item']=item
            self.widget_textbrowser_dlist+=[d]
            
        self.newanapath=False
            
            
    def editname(self, item, column):
        if item is None:
            item=widget.currentItem()
        s=str(item.text(column))
        st=s.partition('.png: ')
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
    
    def updateoptionsfrombatchidialog(self, batchidialog, lastbatchiteration=False):
        prependstr=str(batchidialog.prependfilenameLineEdit.text())
        combinedprependstr=self.filterchars(prependstr+str(self.prependfilenameLineEdit.text()))
        self.prependfilenameLineEdit.setText(combinedprependstr)
        
        self.overwriteCheckBox.setChecked(batchidialog.overwriteCheckBox.isChecked())
        self.epsCheckBox.setChecked(batchidialog.epsCheckBox.isChecked())
        
        
        if lastbatchiteration:#only want to convert to done on last image being batch-saved
            self.doneCheckBox.setChecked(batchidialog.doneCheckBox.isChecked())#for batch save, images saved in place and then box check in the end if convert to .done chosen
        
    def ExitRoutine(self):
        overbool=self.overwriteCheckBox.isChecked()
        prependstr=self.filterchars(str(self.prependfilenameLineEdit.text()))
        
        oldp=os.path.join(self.anafolder, self.anafn)
        
        anadict=readana(oldp, erroruifcn=None, stringvalues=True, returnzipclass=False)#cannot be a .zip
        
        startingwithcopiedbool='copied' in os.path.split(self.anafolder)[1]
        if startingwithcopiedbool or self.doneCheckBox.isChecked():#must convert to .done if starting with .copied. allows .done to be edited which is bad practice
            if not os.path.split(self.anafolder)[1].count('.')>1:
                idialog=messageDialog(self, 'Cannot save because ANA folder has no extension')
                idialog.exec_()
                return
            if startingwithcopiedbool:#if modiyfing a .copied then need a new time stamp
                newanafn=timestampname()+'.ana'
                newanafolder=self.anafolder.rpartition('.')[0][:-15]+newanafn[:-4]+'.done'
                movebool=False
                
            else:
                newanafolder=self.anafolder.rpartition('.')[0]+'.done'#this reapleces .run with .done but more generally .anything with .done
                movebool=True
                newanafn=self.anafn
            saveana_tempfolder(None, self.anafolder, erroruifcn=None, skipana=True, anadict=None, movebool=movebool, savefolder=newanafolder, saveanafile=False)#move files if necessary but don't create .ana or .exp yet. Do this first so image files get put only into new folder
            self.newanapath=os.path.join(newanafolder, newanafn)
        else:#writing files and new ana into existing folder
            newanafn=self.anafn
            newanafolder=self.anafolder
        
        #images here
        lines=[]
        for d in self.widget_plow_dlist:
            if not bool(d['item'].checkState(0)):
                continue
            pngfn, garb, pngattr=str(d['item'].text(0)).partition(': ')
            pngfn=self.filterchars(prependstr+pngfn)
            existfns=os.listdir(newanafolder)
            fn_attr_list=[(pngfn, pngattr)]
            if self.epsCheckBox.isChecked():
                fn_attr_list+=[(pngfn.replace('png', 'eps'), pngattr.replace('png', 'eps'))]
            for fn, a in fn_attr_list:
                if (fn in existfns) and not overbool:
                    i=2
                    fnorig=fn
                    while fn in existfns:
                        fn=''.join([fnorig[:-4], '__%d' %i, fnorig[-4:]])
                        i+=1
                savep=os.path.join(newanafolder, fn)
                existfns+=[fn]
                d['plotw'].fig.savefig(savep)
                lines+=[(fn, a)]
        
        #txt here
        txtlines=[]
        for d in self.widget_textbrowser_dlist:
            if not bool(d['item'].checkState(0)):
                continue
            pngfn, garb, pngattr=str(d['item'].text(0)).partition(': ')
            pngfn=prependstr+pngfn
            existfns=os.listdir(newanafolder)
            fn_attr_list=[(pngfn, pngattr)]
            for fn, a in fn_attr_list:
                if (fn in existfns) and not overbool:
                    i=2
                    fnorig=fn
                    while fn in existfns:
                        fn=''.join([fnorig[:-4], '__%d' %i, fnorig[-4:]])
                        i+=1
                savep=os.path.join(newanafolder, fn)
                existfns+=[fn]
                with open(savep, mode='w') as f:
                    f.write(str(d['browser'].toPlainText()))
                txtlines+=[(fn, a)]
                
                
        if (len(lines)+len(txtlines))>0:
            da=anadict['ana__%d' %self.repr_anaint_plots]
            if not 'files_multi_run' in da.keys():
                da['files_multi_run']={}
            df=da['files_multi_run']
            if len(lines)>0:
                if not 'image_files' in df.keys():
                    df['image_files']={}
                d=df['image_files']
                for fn, a in lines:
                    d[fn]=a#if fn exists and was overwritten this will jdo nothing or update the attrstr
            if len(txtlines)>0:
                if not 'txt_files' in df.keys():
                    df['txt_files']={}
                d=df['txt_files']
                for fn, a in txtlines:
                    d[fn]=a#if fn exists and was overwritten this will jdo nothing or update the attrstr
                    
        newp=os.path.join(newanafolder, newanafn)
        saveanafiles(newp, anadict=anadict, changeananame=True)#need to overwrite the name because may be a new anafolder/timestamp



class saveimagesbatchDialog(QDialog, Ui_SaveImagesBatchDialog):
    def __init__(self, parent, comboind_strlist):
        super(saveimagesbatchDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent

        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    
        self.widgetTopLevelItems={}
        self.comboind_strlist=comboind_strlist
        for comboind, k in self.comboind_strlist:
            mainitem=QTreeWidgetItem([k], 0)
            mainitem.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            mainitem.setCheckState(0, Qt.Checked)
            self.FilesTreeWidget.addTopLevelItem(mainitem)
            self.widgetTopLevelItems[k]={}
            self.widgetTopLevelItems[k]['item']=mainitem
            self.widgetTopLevelItems[k]['comboind']=comboind

    def ExitRoutine(self):
        self.selectcomboboxinds=sorted([d['comboind'] for d in self.widgetTopLevelItems.values() if bool(d['item'].checkState(0))])
