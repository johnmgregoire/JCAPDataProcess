import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib
from fcns_math import myeval
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter

def myexpformat_4digs(x, pos):
    return '%.3e' %x
#    for ndigs in range(4):
#        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','').replace('e-0','e')
#        if eval(lab)==x:
#            return lab
#    return lab

ExpTickLabels=FuncFormatter(myexpformat_4digs)
RegTickLabels=matplotlib.ticker.ScalarFormatter()

def autotickformat(ax, x=False, y=False, ndec=3):
    for bl, xax, lims in zip([x, y], [ax.xaxis, ax.yaxis], [ax.get_xlim(), ax.get_ylim()]):
        if bl:
            try:
                doit=numpy.max(numpy.log10(numpy.abs(numpy.array(lims))))<(-ndec)
                doit=doit or numpy.min(numpy.log10(numpy.abs(numpy.array(lims))))>ndec
            except:
                print 'error on axis formatter for lims ', lims
                continue
            if doit:
                xax.set_major_formatter(ExpTickLabels)
            else:
                xax.set_major_formatter(RegTickLabels)

def autocolorbarformat(lims, ndec=3):
    try:
        doit=numpy.max(numpy.log10(numpy.abs(numpy.array(lims))))<(-ndec)
        doit=doit or numpy.min(numpy.log10(numpy.abs(numpy.array(lims))))>ndec
    except:
        print 'error on axis formatter for lims ', lims
        return
    if doit:
        return ExpTickLabels
    else:
        return RegTickLabels


class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        
        mainlayout=QGridLayout()

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        
        if len(title)>20:
            lab=QLabel()
            lab.setText(title)
            print '***', title
            mainlayout.addWidget(lab, 0, 0)
            mainlayout.addWidget(self.buttonBox, 1, 0)
        else:
            self.setWindowTitle(title)
            mainlayout.addWidget(self.buttonBox, 0, 0)
        self.setLayout(mainlayout)


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

class getexistingFilesFolders(QFileDialog):
    def __init__(self, *args):
        QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        btns = self.findChildren(QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QTreeView)

    def openClicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
#                print i.data().__class__.__name__
                files.append(os.path.join(str(self.directory().absolutePath()),str(i.data())))
        print files
        self.selectedFiles = [str(fn) for fn in files]
        self.hide()

    def filesSelected(self):
        return self.selectedFiles
        
def userinputcaller(parent, inputs=[('testnumber', int)], title='Enter values',  cancelallowed=True, returnchangedbool=False):
    problem=True
    while problem:
        idialog=userinputDialog(parent, inputs, title)
        idialog.exec_()
        problem=idialog.problem
        if not idialog.ok and cancelallowed:
            return None
        inputs=[(tup[0], tup[1], s) for tup, s  in zip(inputs, idialog.inputstrlist)]
    
    if returnchangedbool:
        return idialog.ans, idialog.changedbool
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
        self.changedbool=[]
        self.inputstrlist=[str(le.text()).strip() for le in self.lelist]
        for s, tup in zip(self.inputstrlist, self.inputs):
            if len(tup)>2:
                self.changedbool+=[s!=tup[2]]
            else:
                self.changedbool+=[True]
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

def userselectcaller(parent, options=['none'], title='Select values',  cancelallowed=True):
    problem=True
    while problem:
        idialog=userselectDialog(parent, options, title)
        idialog.exec_()
        problem=idialog.problem
        if not idialog.ok and cancelallowed:
            return None

    return idialog.ans

class userselectDialog(QDialog):
    def __init__(self, parent, options=['none'], title='Select values'):
        super(userselectDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
        self.parent=parent
        self.options=options
        self.ComboBox=QComboBox()
        for i, s in enumerate(self.options):
            self.ComboBox.insertItem(i, s)
        self.ComboBox.setCurrentIndex(0)
        mainlayout.addWidget(self.ComboBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)

        self.setLayout(mainlayout)


        QMetaObject.connectSlotsByName(self)

        self.problem=False
        self.ok=False

    def ExitRoutine(self):
        self.ok=True
        self.problem=False
        self.ans=self.ComboBox.currentIndex()
        if self.problem:#in initial version there is never a problem
            idialog=messageDialog(self, 'problem with selection')
            idialog.exec_()
