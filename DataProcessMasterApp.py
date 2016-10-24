import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

projectpath=os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath,'QtForms'))
sys.path.append(os.path.join(projectpath,'AuxPrograms'))
sys.path.append(os.path.join(projectpath,'OtherApps'))

from CreateExperimentApp import expDialog
from CalcFOMApp import calcfomDialog
from VisualizeDataApp import visdataDialog
from StackPlotApp import stackplotDialog
from CombineFomApp import combinefomDialog
from FileSearchApp import filesearchDialog
from FileManagementApp import filemanDialog


class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.expui=None
        self.calcui=None
        self.visdataui=None
        self.stackplotui=None
        self.combinefomui=None
        self.filesearchui=None
        self.filemanui=None
        
        expuiButton=QPushButton()
        expuiButton.setText("Create/edit\nExperiment")
        QObject.connect(expuiButton, SIGNAL("pressed()"), self.expui_exec)

        calcuiButton=QPushButton()
        calcuiButton.setText("Calc FOM for\nExperiment")
        QObject.connect(calcuiButton, SIGNAL("pressed()"), self.calcui_exec)
        
        visdataButton=QPushButton()
        visdataButton.setText("Visualize\nData")
        QObject.connect(visdataButton, SIGNAL("pressed()"), self.visui_exec)
        
        stackplotButton=QPushButton()
        stackplotButton.setText("Stack\nPlots")
        QObject.connect(stackplotButton, SIGNAL("pressed()"), self.stackui_exec)   
        
        combinefomuiButton=QPushButton()
        combinefomuiButton.setText("Combine\nFOM files")
        QObject.connect(combinefomuiButton, SIGNAL("pressed()"), self.combinefomui_exec)
        
        filesearchButton=QPushButton()
        filesearchButton.setText("Search for\nEXP/ANA files")
        QObject.connect(filesearchButton, SIGNAL("pressed()"), self.filesearchui_exec)
        
        filemanButton=QPushButton()
        filemanButton.setText("Delete obsolete\nEXP/ANA folders")
        QObject.connect(filemanButton, SIGNAL("pressed()"), self.filemanui_exec)
        
        mainlayout=QGridLayout()

        mainlayout.addWidget(expuiButton, 0, 0)
        mainlayout.addWidget(calcuiButton, 0, 1)
        mainlayout.addWidget(visdataButton, 0, 2)
        mainlayout.addWidget(stackplotButton, 0, 3)
        mainlayout.addWidget(combinefomuiButton, 0, 4)
        mainlayout.addWidget(filesearchButton, 0, 5)
        mainlayout.addWidget(filemanButton, 0, 6)
   
        window=QWidget();
        window.setLayout(mainlayout);

        self.setCentralWidget(window)
        
        #self.setLayout(mainlayout)
        
    def expui_exec(self):
        if self.expui is None:
            self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.expui.show()
    def calcui_exec(self, show=True):
        if self.calcui is None:
            self.calcui=calcfomDialog(self, title='Calculate FOM from EXP')
        if show:
            self.calcui.show()
    def visui_exec(self, show=True):
        if self.visdataui is None:
            self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')
        if show:
            self.visdataui.show()
    def stackui_exec(self, show=True):
        if self.stackplotui is None:
            self.stackplotui=stackplotDialog(self, title='Stack Plots of FOM data')
        if show:
            self.stackplotui.show()
    def combinefomui_exec(self):
        if self.combinefomui is None:
            self.combinefomui=combinefomDialog(self, title='Combine FOM from multiple files')
        self.combinefomui.show()
    def filesearchui_exec(self):
        if self.filesearchui is None:
            self.filesearchui=filesearchDialog(self, title='Search for exp/ana files')
        self.filesearchui.show()
    def filemanui_exec(self):
        if self.filemanui is None:
            self.filemanui=filemanDialog(self, title='Delete obsolete .run folders')
        self.filemanui.show()
    
    def calcexp(self, expfiledict=None, exppath=None, show=True):
        self.calcui_exec(show=show)
        if not (expfiledict is None or exppath is None):
            self.calcui.importexp(expfiledict=expfiledict, exppath=exppath)
        
    def visexpana(self, anafiledict=None, anafolder=None, experiment_path=None, show=True):
        self.visui_exec(show=show)
        if not (anafiledict is None or anafolder is None):
            self.visdataui.importana(anafiledict=anafiledict, anafolder=anafolder)
        elif not experiment_path is None:
            self.visdataui.importexp(experiment_path=experiment_path)
        
        
        
        
        

mainapp=QApplication(sys.argv)
form=MainMenu(None)
form.show()
form.setFocus()

mainapp.exec_()
