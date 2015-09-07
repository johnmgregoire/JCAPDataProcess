#cd C:\Python27\Lib\site-packages\PyQt4
#pyuic4 -x C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\QtDesign\CreateExpForm.ui -o C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\CreateExpForm.py
import time, shutil
import os, os.path
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
#from fcns_math import *
#from fcns_io import *
from fcns_ui import *
from FileManagementForm import Ui_FileManDialog
from DBPaths import *

class filemanDialog(QDialog, Ui_FileManDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(filemanDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        

        button_fcn=[\
        (self.deletefoldersButton, self.deletefolders), \
        (self.findfoldersButton, self.findfolders), \
        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        #        (self.EditParamsPushButton, self.editrunparams), \
        #(self.EditExpParamsPushButton, self.editexpparams), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        self.treeWidget=self.foldersTreeWidget
        self.toplevelitems=[]

        
    def deletefolders(self):
       
        for mainitem, fold in zip(self.toplevelitems, [EXPFOLDER_K, ANAFOLDER_K]):
            if not bool(mainitem.checkState(0)):
                continue
            subitems=[mainitem.child(i) for i in range(mainitem.childCount()) if bool(mainitem.child(i).checkState(0))]
            delpaths=[os.path.join(os.path.join(fold, str(subitem.text(0))), str(subitem.child(i).text(0))) for subitem in subitems for i in range(subitem.childCount()) if bool(subitem.child(i).checkState(0))]
            for p in delpaths:
                shutil.rmtree(p, ignore_errors=True)
                print 'removed ', p
        if bool(mainitem.checkState(0)):
            idialog=messageDialog(self, 'folders deleted: ANA temp folder possibly deleted \nso restart before performing analysis')
            idialog.exec_()

    def findfolders(self):
        self.treeWidget.clear()

        self.toplevelitems=[]
        for i, (lab, fold) in enumerate(zip(['EXP', 'ANA'], [EXPFOLDER_K, ANAFOLDER_K])):
            mainitem=QTreeWidgetItem([lab], 0)
            mainitem.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            mainitem.setCheckState(0, Qt.Checked)
            if i==0:
                item0=mainitem
            self.treeWidget.addTopLevelItem(mainitem)
            self.nestedfill(fold, mainitem, 'top', endswith=None)
            mainitem.setExpanded(True)
            self.toplevelitems+=[mainitem]
        self.treeWidget.setCurrentItem(item0)



    def nestedfill(self, fold, parentitem, level, endswith='.run'):
        subfolds=[fn for fn in os.listdir(fold) if os.path.isdir(os.path.join(fold, fn))]
        if not endswith is None:
            subfolds=[fn for fn in subfolds if fn.endswith(endswith)]
        for fn in subfolds:
            item=QTreeWidgetItem([fn],  0)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)

            if level=='top':
                p=os.path.join(fold, fn)
                print p
                addbool=self.nestedfill(p, item, 'sub')
                addbool=addbool>0
            else:
                addbool=True
            if addbool:
                parentitem.addChild(item)
        return len(subfolds)



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
            super(MainMenu, self).__init__(None)
            #self.setupUi(self)
            self.filemanui=filemanDialog(self, title='Delete obsolete .run folders', **kwargs)
            #self.expui.importruns(pathlist=['20150422.145113.donex.zip'])
            #self.expui.importruns(pathlist=['uvis'])
            if execute:
                self.filemanui.exec_()                
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    

    
    mainapp.exec_()

