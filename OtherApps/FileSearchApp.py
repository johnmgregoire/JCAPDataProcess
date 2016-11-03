#cd C:\Python27\Lib\site-packages\PyQt4
#pyuic4 -x C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\QtDesign\CreateExpForm.ui -o C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\CreateExpForm.py
import time, shutil, glob
import os, os.path
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
#from fcns_math import *
from fcns_io import *
from fcns_ui import *
from FileSearchForm import Ui_filesearchDialog
from DBPaths import *

class filesearchDialog(QDialog, Ui_filesearchDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(filesearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        QObject.connect(self.treeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.openpath)

        button_fcn=[\
        (self.findfoldersButton, self.findfolders), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        #        (self.EditParamsPushButton, self.editrunparams), \
        #(self.EditExpParamsPushButton, self.editexpparams), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        

        self.toplevelitems=[]
        

        
    
    def openpath(self, item, column):
        s=str(item.text(column))
        while not item.parent() is None:
            item=item.parent()
            s=r'%s\%s' %(str(item.text(0)).rpartition('~')[2], s)
    
        s=s.replace(chr(47),chr(92))
        
        ans=userinputcaller(self, inputs=[('file path', str, s)], title='Path available for copy',  cancelallowed=True)
#        if ans is None:
#            return
#        ans=ans[0].strip()
        
    def findfolders(self):
        self.treeWidget.clear()

        self.toplevelitems=[]
        
        self.withinstr=str(self.withinfileLineEdit.text()).strip()
        self.foldersearchstr=str(self.foldernameLineEdit.text()).strip()
        searchtups=[]
        
        for i, (cb, lab, fold) in enumerate(zip([self.exp_k_checkBox, self.exp_j_checkBox, self.ana_k_checkBox, self.ana_j_checkBox], ['EXP', 'EXP', 'ANA', 'ANA'], [tryprependpath(EXPFOLDERS_L, ''), tryprependpath(EXPFOLDERS_J, ''), tryprependpath(ANAFOLDERS_L, ''), tryprependpath(ANAFOLDERS_J, '')])):
            if len(fold)==0 or not cb.isChecked(): #didn't find exp or ana folder but found other one
                self.toplevelitems+=[None]
                continue
            mainitem=QTreeWidgetItem(['%s~%s' %(lab, fold.rstrip(chr(47)).rstrip(chr(92)))], 0)
#            mainitem.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
#            mainitem.setCheckState(0, Qt.Checked)
            if i==0:
                item0=mainitem
            self.treeWidget.addTopLevelItem(mainitem)

            for typefold in [fn for fn in os.listdir(fold) if os.path.isdir(os.path.join(fold, fn))]:
                item=QTreeWidgetItem([typefold],  0)
                typefoldpath=os.path.join(fold, typefold)
                addtypefold=False
                for expanafold in [fn for fn in os.listdir(typefoldpath) if self.foldersearchstr in fn and os.path.isdir(os.path.join(typefoldpath, fn))]:
                    expanafoldpath=os.path.join(typefoldpath, expanafold)
                    fnstart='.'.join(expanafold.split('.')[:2])
                    expanafn=fnstart+'.'+lab.lower()
                    p=os.path.join(expanafoldpath, expanafn)
                    if not os.path.isfile(p):
                        continue
                    if self.withinstr:
                        with open(p, mode='r') as f:
                            found=self.withinstr in f.read()
                        if not found:
                            continue
                    subitem=QTreeWidgetItem([r'%s/%s' %(expanafold, expanafn)],  0)
                    item.addChild(subitem)
                    addtypefold=True
                if addtypefold:
                    mainitem.addChild(item)
            mainitem.setExpanded(True)
            self.toplevelitems+=[mainitem]
            break
        self.treeWidget.setCurrentItem(item0)



    def nestedfill(self, fold, parentitem, fnendswith, level):
        
        
        subfolds=[fn for fn in os.listdir(fold) if os.path.isdir(os.path.join(fold, fn))]
        addbool=(level=='top')
        for fn in subfolds:
            item=QTreeWidgetItem([fn],  0)
#            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
#            if level=='top' and fn!='temp':#don't auto check the non-temp folders like eche, uvis, imag
#                item.setCheckState(0, Qt.Unchecked)
#            else:
#                item.setCheckState(0, Qt.Checked)
            

            
            p=os.path.join(fold, fn)
            print p
            subaddbool=self.nestedfill(p, item, fnendswith,'sub')
            if subaddbool:
                parentitem.addChild(item)
            addbool=addbool or subaddbool
            
        if self.foldersearchstr in fold:
            fnstoadd=[fn for fn in os.listdir(fold) if os.path.isfile(os.path.join(fold, fn)) and fn.endswith(fnendswith)]
            for fnadd in fnstoadd:
                item=QTreeWidgetItem([fn],  0)
                parentitem.addChild(item)
                
    
        return (len(fnstoadd)>0) or addbool



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
            super(MainMenu, self).__init__(None)
            #self.setupUi(self)
            self.filesearchui=filesearchDialog(self, title='Search for exp/ana files', **kwargs)
            #self.expui.importruns(pathlist=['20150422.145113.donex.zip'])
            #self.expui.importruns(pathlist=['uvis'])
            if execute:
                self.filesearchui.exec_()                
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    

    
    mainapp.exec_()

