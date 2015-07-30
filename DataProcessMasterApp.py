import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from CreateExperimentApp import expDialog
from CalcFOMApp import calcfomDialog
#from VisualizeDataApp import visdataDialog
from CombineFomApp import combinefomDialog



class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.expui=expDialog(self, title='Create/Edit an Experiment')
        self.calcui=calcfomDialog(self, title='Calculate FOM from EXP')
        #self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data')
        self.combinefomui=combinefomDialog(self, title='Combine FOM from multiple files')
        
        expuiButton=QPushButton()
        expuiButton.setText("Create/edit\nExperiment")
        QObject.connect(expuiButton, SIGNAL("pressed()"), self.expui_exec)

        calcuiButton=QPushButton()
        calcuiButton.setText("Calc FOM for\nExperiment")
        QObject.connect(calcuiButton, SIGNAL("pressed()"), self.calcui_exec)
        
        visdataButton=QPushButton()
        visdataButton.setText("Visualize\nData")
        QObject.connect(visdataButton, SIGNAL("pressed()"), self.visui_exec)
        
        combinefomuiButton=QPushButton()
        combinefomuiButton.setText("Combine\nFOM files")
        QObject.connect(combinefomuiButton, SIGNAL("pressed()"), self.combinefomui_exec)
        
        mainlayout=QGridLayout()

        mainlayout.addWidget(expuiButton, 0, 0)
        mainlayout.addWidget(calcuiButton, 0, 1)
        mainlayout.addWidget(visdataButton, 0, 2)
        mainlayout.addWidget(combinefomuiButton, 0, 3)
   
        window=QWidget();
        window.setLayout(mainlayout);

        self.setCentralWidget(window)
        
        #self.setLayout(mainlayout)
        
    def expui_exec(self):
        self.expui.show()
    def calcui_exec(self):
        self.calcui.show()
    def visui_exec(self):
        return
        #self.visdataui.show()
    def combinefomui_exec(self):
        self.combinefomui.show()
        
mainapp=QApplication(sys.argv)
form=MainMenu(None)
form.show()
form.setFocus()

mainapp.exec_()
