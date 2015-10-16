import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SearchFolderForm import Ui_SearchFolderDialog
from fcns_io import *
from fcns_ui import *

class SearchFolderDialog(QDialog, Ui_SearchFolderDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(SearchFolderDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent

        QObject.connect(self.FolderPushButton, SIGNAL("pressed()"), self.processopenfolder)
        QObject.connect(self.PathlistPushButton, SIGNAL("pressed()"), self.processopenpathlist)
        QObject.connect(self.SearchPushButton, SIGNAL("pressed()"), self.performsearch)
        QObject.connect(self.ParentFolderPushButton, SIGNAL("pressed()"), self.selectfolder)
        
        self.openfolder=None
        self.openpathlist=None
        self.FoldersCheckBoxes=[self.CheckBox_0, self.CheckBox_1, self.CheckBox_2, self.CheckBox_3, self.CheckBox_4, self.CheckBox_5, \
            self.CheckBox_6, self.CheckBox_7, self.CheckBox_8, self.CheckBox_9]
        
        if folderpath is None:
            self.folder=os.getcwd()
        else:
            self.folder=folderpath
        
        self.selectfolder()
        self.performsearch()
    def performsearch(self):
        if not os.path.isdir(self.folder):
            idialog=messageDialog(self, 'cannot search because\nparent folder not defined')
            idialog.exec_()
            return
        s=str(self.SearchLineEdit.text())
        folderlist, runpathlist=self.findrunfolder_searchstr(self.folder, s)
        
        qlist=self.FoldersButtonGroup.buttons()
        numbuttons=len(qlist)
        for button in qlist:
            button.setText('')
        
        for count, p in enumerate(folderlist):
            if count==numbuttons:
                break
            button=qlist[count]
            s=os.path.relpath(p, self.folder)

            button.setText(s)
            if count==0:
                button.setChecked(True)
        
        for cb in self.FoldersCheckBoxes:
            cb.setText('')
        for cb, p in zip(self.FoldersCheckBoxes, runpathlist):
            s=os.path.relpath(p, self.folder)
            cb.setText(s)
    
    def selectfolder(self):
        folder=mygetdir(parent=self, xpath=self.folder,markstr='select folder for search')
        if len(folder)==0:
            return
        else:
            self.folder=folder

    def processopenfolder(self):
        for button in self.FoldersButtonGroup.buttons():
            if button.isChecked():
                self.openfolder=os.path.join(self.folder, str(button.text()))
        
        self.reject()
    def processopenpathlist(self):
        self.openpathlist=[]
        for cb in self.FoldersCheckBoxes:
            if cb.isChecked():
                self.openpathlist+=[os.path.join(self.folder, str(cb.text()))]
        self.reject()
        
    def findrunfolder_searchstr(self, folder, searchstr):
        folderlist=[]
        runpathlist=[]
        
        for dirpath, dirnames, filenames in os.walk(folder):
            temp=[os.path.join(dirpath, dn) for dn in dirnames if searchstr in dn]
            temp2=[p for p in temp if True in ['.rcp' in p2 for p2 in os.listdir(p)]]
            temp3=[p for p in temp if not p in temp2]
            folderlist+=temp3
            runpathlist+=temp2
            runpathlist+=[os.path.join(dirpath, fn) for fn in filenames if (searchstr in fn or searchstr in os.path.split(dirpath)[1]) and '.zip' in fn]
        return folderlist, runpathlist

if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
            super(MainMenu, self).__init__(None)
            #self.setupUi(self)
            self.searchui=SearchFolderDialog(self, title='Select items to open', **kwargs)
            #self.expui.importruns(pathlist=['20150422.145113.donex.zip'])
            #self.expui.importruns(pathlist=['uvis'])
            if execute:
                self.searchui.exec_()                
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    
    #form.expui.exec_()
    print form.searchui.openfolder
    print form.searchui.openpathlist
    mainapp.exec_()
