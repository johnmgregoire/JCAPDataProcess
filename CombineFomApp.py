import csv
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

if __name__ == "__main__":
    import os, sys
    projectpath=os.path.split(os.path.abspath(__file__))[0]
    sys.path.append(os.path.join(projectpath,'AuxPrograms'))

from fcns_math import *
from fcns_io import *







    
class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
  
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 0, 0)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    def ExitRoutine(self):
        return
        
def mygetopenfile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getOpenFileName(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getOpenFileName(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetopenfiles(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfns=QFileDialog.getOpenFileNames(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/'))
        xparent.destroy()
        xapp.quit()
    else:
        returnfns=QFileDialog.getOpenFileNames(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/'))
    return [str(s) for s in returnfns]

def mygetsavefile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getSaveFileName(xparent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getSaveFileName(parent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetdir(parent=None, xpath="%s" % os.getcwd(),markstr='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getExistingDirectory(xparent,''.join(['Select directory:', markstr]), xpath))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getExistingDirectory(parent,''.join(['Select directory:', markstr]), xpath))
    

def userinputcaller(parent, inputs=[('testnumber', int)], title='Enter values',  cancelallowed=True):
    problem=True
    while problem:
        idialog=userinputDialog(parent, inputs, title)
        idialog.exec_()
        problem=idialog.problem
        if not idialog.ok and cancelallowed:
            return None
        inputs=[(tup[0], tup[1], s) for tup, s  in zip(inputs, idialog.inputstrlist)]
        
    return idialog.ans

class userinputDialog(QDialog):
    def __init__(self, parent, inputs=[('testnumber', int, '')], title='Enter values'):
        super(userinputDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
        self.parent=parent
        self.inputs=inputs
        self.lelist=[]
        for i, tup in enumerate(self.inputs):
            lab=QLabel()
            lab.setText(tup[0])
            le=QLineEdit()
            if len(tup)>2:
                le.setText(tup[2])
            self.lelist+=[le]
            mainlayout.addWidget(lab, 0, i, 1, 1)
            mainlayout.addWidget(le, 1, i, 1, 1)    
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, 2, 0, len(inputs), 1)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        
        self.setLayout(mainlayout)
        
        
        QMetaObject.connectSlotsByName(self)
        
        self.problem=False
        self.ok=False

    def ExitRoutine(self):
        self.ok=True
        self.problem=False
        self.ans=[]
        self.inputstrlist=[str(le.text()).strip() for le in self.lelist]
        for s, tup in zip(self.inputstrlist, self.inputs):
            if tup[1]==str:
                try:
                    self.ans+=[s]
                except:
                    self.problem=True
                    break
            else:
                try:
                    n=myeval(s)
                    self.ans+=[tup[1](n)]
                except:
                    self.problem=True
                    break
        if self.problem:
            idialog=messageDialog(self, 'problem with conversion of ' + tup[0])
            idialog.exec_()
            

class selectoutputsDialog(QDialog):
    def __init__(self, parent, keylists, title='Select columns for outputfile values'):
        super(selectoutputsDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
        self.keylists=keylists

        self.cblists=[]
        for i, kl in enumerate(self.keylists):
            cbl=[]
            for j, k in enumerate(kl):
                cb=QCheckBox()
                cb.setText(k)
                if (i==0 and j>0) or j==(len(kl)-1):
                    cb.setChecked(1)
                else:
                    cb.setChecked(0)
                mainlayout.addWidget(cb, j, i)
                cbl+=[cb]
            self.cblists+=[cbl]
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, j+1, 0, 1, i+1)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        
        self.setLayout(mainlayout)
        
        
        QMetaObject.connectSlotsByName(self)


    def ExitRoutine(self):
        self.keylistsselected=[]
        for cbl, kl in zip(self.cblists, self.keylists):
            kl_s=[]
            for cb, k in zip(cbl, kl):
                if cb.isChecked():
                    kl_s+=[k]
            self.keylistsselected+=[kl_s]



class combinefomDialog(QDialog):
    def __init__(self, parent, title='', folderpath=None):
        super(combinefomDialog, self).__init__(parent)
        self.parent=parent
        
        
#        folderButton=QPushButton()
#        folderButton.setText("select\nfolder")
#        QObject.connect(folderButton, SIGNAL("pressed()"), self.selectfolder)
#        
#        plotButton=QPushButton()
#        plotButton.setText("update\nfigures")
#        QObject.connect(plotButton, SIGNAL("pressed()"), self.calcandplot)
#        
        saveButton=QPushButton()
        saveButton.setText("Select Files\nTo Combine")
        QObject.connect(saveButton, SIGNAL("pressed()"), self.save)


        self.cb=QCheckBox()
        self.cb.setText('check=union\nuncheck=intersection\nof sample_no')
 
        mainlayout=QGridLayout()

    
        
        mainlayout.addWidget(saveButton, 0, 0)
        mainlayout.addWidget(self.cb, 0, 1)
   
        self.setLayout(mainlayout)
        
        #self.folderpath=folderpath

        #self.resize(600, 850)

        
    def save(self):
        dpl=mygetopenfiles(parent=self, markstr='FOM .txt files', filename='.txt')
        smpkeys=['sample_no', 'Sample']
        keylists=[]
        dropdl=[]
        for dp in dpl:
            if dp=='':
                dropdl+=[None]
                continue
            with open(dp, mode='r') as f:
                lines=f.readlines()
            
            templist=[(i, [l.startswith(k) for k in smpkeys].index(True)) for i, l in enumerate(lines) if True in [l.startswith(k) for k in smpkeys]]
            if len(templist)==0:
                print 'sample_no not found as left-most column for %s' %dp
            headingslineind, smpkeyind=templist[0]
            smpkey=smpkeys[smpkeyind]
            delim=lines[headingslineind][len(smpkey)]
            arr=readtxt_selectcolumns(dp, delim=delim, num_header_lines=headingslineind+1, floatintstr=str, zipclass=False)
            dropd={}
            kl=lines[headingslineind].split(delim)
            kl=[k.strip() for k in kl]
            for k, a in zip(kl, arr):
                if k==smpkey:
                    k='sample_no'
                dropd[k]=list(a)

            dropdl+=[dropd]
            f=open(dp, mode='r')
            l=f.readlines()[0]
            f.close()
            keylists+=[kl]
            #keylists+=[list(dropd.keys())]
        
        idialog=selectoutputsDialog(self,keylists)
        idialog.exec_()
        keylistsselected=idialog.keylistsselected

        smplists=[d['sample_no'] for d in dropdl]
        smpinters=set(smplists[0])
        unionbool=self.cb.isChecked()
        for sl in smplists:
            if unionbool:
                smpinters=smpinters.union(set(sl))
            else:
                smpinters=smpinters.intersection(set(sl))
        smpinters=numpy.array(list(smpinters))
        seval=[myeval(s) for s in smpinters]
        inds=numpy.argsort(seval)
        smpinters=smpinters[inds]
        
        lines=[['sample_no']]
        for kl in keylistsselected:
            lines[0]+=kl
        for s in smpinters:
            ll=[s]
            for d, sl, kl in zip(dropdl, smplists, keylistsselected):
                if s in sl:
                    i=sl.index(s)
                    ll+=[d[k][i] for k in kl]
                else:
                    ll+=['NaN' for k in kl]
            lines+=[ll]

        
        s='\n'.join([','.join([v for v in ll]) for ll in lines])
        
        sp=mygetsavefile(parent=self, xpath=os.path.split(dpl[0])[0],markstr='savefile', filename='combinedfom.txt' )
        
        f=open(sp, mode='w')
        f.write(s)
        f.close()

        
        
        
        
        
class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
  
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 0, 0)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    def ExitRoutine(self):
        return
        

if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
            super(MainMenu, self).__init__(None)
            
            self.combinefomui=combinefomDialog(self, title='Combine FOM from multiple files', **kwargs)
            if execute:
                self.combinefomui.exec_()                
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
    

