# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\ExternalImportForm.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ExternalImportDialog(object):
    def setupUi(self, ExternalImportDialog):
        ExternalImportDialog.setObjectName(_fromUtf8("ExternalImportDialog"))
        ExternalImportDialog.resize(1142, 882)
        self.ProfileComboBox = QtGui.QComboBox(ExternalImportDialog)
        self.ProfileComboBox.setGeometry(QtCore.QRect(10, 10, 271, 22))
        self.ProfileComboBox.setObjectName(_fromUtf8("ProfileComboBox"))
        self.CreateFilesPushButton = QtGui.QPushButton(ExternalImportDialog)
        self.CreateFilesPushButton.setGeometry(QtCore.QRect(10, 90, 151, 21))
        self.CreateFilesPushButton.setObjectName(_fromUtf8("CreateFilesPushButton"))
        self.OpenFolderPushButton = QtGui.QPushButton(ExternalImportDialog)
        self.OpenFolderPushButton.setGeometry(QtCore.QRect(10, 40, 71, 21))
        self.OpenFolderPushButton.setObjectName(_fromUtf8("OpenFolderPushButton"))
        self.OpenPlatemapPushButton = QtGui.QPushButton(ExternalImportDialog)
        self.OpenPlatemapPushButton.setGeometry(QtCore.QRect(10, 60, 81, 21))
        self.OpenPlatemapPushButton.setObjectName(_fromUtf8("OpenPlatemapPushButton"))
        self.textBrowser_plate = QtGui.QTextBrowser(ExternalImportDialog)
        self.textBrowser_plate.setGeometry(QtCore.QRect(10, 460, 551, 361))
        self.textBrowser_plate.setObjectName(_fromUtf8("textBrowser_plate"))
        self.AnaTreeWidget = QtGui.QTreeWidget(ExternalImportDialog)
        self.AnaTreeWidget.setGeometry(QtCore.QRect(580, 550, 551, 251))
        self.AnaTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AnaTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.AnaTreeWidget.setHeaderHidden(True)
        self.AnaTreeWidget.setExpandsOnDoubleClick(False)
        self.AnaTreeWidget.setObjectName(_fromUtf8("AnaTreeWidget"))
        self.AnaTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.AnaTreeWidget.header().setVisible(False)
        self.AnaTreeWidget.header().setCascadingSectionResizes(False)
        self.AnaTreeWidget.header().setStretchLastSection(True)
        self.label_7 = QtGui.QLabel(ExternalImportDialog)
        self.label_7.setGeometry(QtCore.QRect(580, 270, 111, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.ExpSaveComboBox = QtGui.QComboBox(ExternalImportDialog)
        self.ExpSaveComboBox.setGeometry(QtCore.QRect(690, 270, 267, 20))
        self.ExpSaveComboBox.setObjectName(_fromUtf8("ExpSaveComboBox"))
        self.label_14 = QtGui.QLabel(ExternalImportDialog)
        self.label_14.setGeometry(QtCore.QRect(10, 120, 265, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.RunSelectTreeWidget = QtGui.QTreeWidget(ExternalImportDialog)
        self.RunSelectTreeWidget.setGeometry(QtCore.QRect(10, 140, 551, 311))
        self.RunSelectTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RunSelectTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.RunSelectTreeWidget.setHeaderHidden(True)
        self.RunSelectTreeWidget.setExpandsOnDoubleClick(False)
        self.RunSelectTreeWidget.setObjectName(_fromUtf8("RunSelectTreeWidget"))
        self.RunSelectTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.RunSelectTreeWidget.header().setVisible(False)
        self.RunSelectTreeWidget.header().setCascadingSectionResizes(False)
        self.RunSelectTreeWidget.header().setStretchLastSection(True)
        self.RaiseErrorPushButton = QtGui.QPushButton(ExternalImportDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(1120, 0, 31, 21))
        self.RaiseErrorPushButton.setObjectName(_fromUtf8("RaiseErrorPushButton"))
        self.foldernameLineEdit = QtGui.QLineEdit(ExternalImportDialog)
        self.foldernameLineEdit.setGeometry(QtCore.QRect(90, 40, 191, 21))
        self.foldernameLineEdit.setText(_fromUtf8(""))
        self.foldernameLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.foldernameLineEdit.setObjectName(_fromUtf8("foldernameLineEdit"))
        self.platemappathLineEdit = QtGui.QLineEdit(ExternalImportDialog)
        self.platemappathLineEdit.setGeometry(QtCore.QRect(90, 60, 191, 21))
        self.platemappathLineEdit.setText(_fromUtf8(""))
        self.platemappathLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.platemappathLineEdit.setObjectName(_fromUtf8("platemappathLineEdit"))
        self.ExpTreeWidget = QtGui.QTreeWidget(ExternalImportDialog)
        self.ExpTreeWidget.setGeometry(QtCore.QRect(580, 290, 551, 231))
        self.ExpTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ExpTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.ExpTreeWidget.setHeaderHidden(True)
        self.ExpTreeWidget.setExpandsOnDoubleClick(False)
        self.ExpTreeWidget.setObjectName(_fromUtf8("ExpTreeWidget"))
        self.ExpTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.ExpTreeWidget.header().setVisible(False)
        self.ExpTreeWidget.header().setCascadingSectionResizes(False)
        self.ExpTreeWidget.header().setStretchLastSection(True)
        self.RcpTreeWidget = QtGui.QTreeWidget(ExternalImportDialog)
        self.RcpTreeWidget.setGeometry(QtCore.QRect(580, 20, 551, 241))
        self.RcpTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RcpTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.RcpTreeWidget.setHeaderHidden(True)
        self.RcpTreeWidget.setExpandsOnDoubleClick(False)
        self.RcpTreeWidget.setObjectName(_fromUtf8("RcpTreeWidget"))
        self.RcpTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.RcpTreeWidget.header().setVisible(False)
        self.RcpTreeWidget.header().setCascadingSectionResizes(False)
        self.RcpTreeWidget.header().setStretchLastSection(True)
        self.label_8 = QtGui.QLabel(ExternalImportDialog)
        self.label_8.setGeometry(QtCore.QRect(580, 530, 111, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.AnaSaveComboBox = QtGui.QComboBox(ExternalImportDialog)
        self.AnaSaveComboBox.setGeometry(QtCore.QRect(690, 530, 267, 20))
        self.AnaSaveComboBox.setObjectName(_fromUtf8("AnaSaveComboBox"))
        self.label_9 = QtGui.QLabel(ExternalImportDialog)
        self.label_9.setGeometry(QtCore.QRect(580, 0, 111, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.CalcXLineEdit = QtGui.QLineEdit(ExternalImportDialog)
        self.CalcXLineEdit.setGeometry(QtCore.QRect(290, 60, 121, 20))
        self.CalcXLineEdit.setObjectName(_fromUtf8("CalcXLineEdit"))
        self.CalcYLineEdit = QtGui.QLineEdit(ExternalImportDialog)
        self.CalcYLineEdit.setGeometry(QtCore.QRect(422, 60, 121, 20))
        self.CalcYLineEdit.setObjectName(_fromUtf8("CalcYLineEdit"))
        self.label_16 = QtGui.QLabel(ExternalImportDialog)
        self.label_16.setGeometry(QtCore.QRect(290, 40, 265, 21))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.plateidLineEdit = QtGui.QLineEdit(ExternalImportDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(340, 10, 51, 21))
        self.plateidLineEdit.setText(_fromUtf8(""))
        self.plateidLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.plateidLineEdit.setObjectName(_fromUtf8("plateidLineEdit"))
        self.label_17 = QtGui.QLabel(ExternalImportDialog)
        self.label_17.setGeometry(QtCore.QRect(290, 10, 51, 21))
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))

        self.retranslateUi(ExternalImportDialog)
        QtCore.QMetaObject.connectSlotsByName(ExternalImportDialog)

    def retranslateUi(self, ExternalImportDialog):
        ExternalImportDialog.setWindowTitle(_translate("ExternalImportDialog", "Process Data, Calc FOM from EXP", None))
        self.ProfileComboBox.setToolTip(_translate("ExternalImportDialog", "Apply all other filteres in this section to only this run", None))
        self.CreateFilesPushButton.setToolTip(_translate("ExternalImportDialog", "Considering the files already in the EXP, keep the files that meet all criteria", None))
        self.CreateFilesPushButton.setText(_translate("ExternalImportDialog", "Generate RCP/EXP/ANA", None))
        self.OpenFolderPushButton.setToolTip(_translate("ExternalImportDialog", "Import a .exp file, which will provide options for the data type, RUNs and analysis type", None))
        self.OpenFolderPushButton.setText(_translate("ExternalImportDialog", "Select Folder", None))
        self.OpenPlatemapPushButton.setToolTip(_translate("ExternalImportDialog", "Grab the EXP from the \"Create EXP\" window", None))
        self.OpenPlatemapPushButton.setText(_translate("ExternalImportDialog", "Open platemap", None))
        self.label_7.setText(_translate("ExternalImportDialog", "EXP file. Save Action:", None))
        self.ExpSaveComboBox.setToolTip(_translate("ExternalImportDialog", "This \"use\" is specified in the EXP \n"
"and determines what types of analysis \n"
"can be performed", None))
        self.label_14.setText(_translate("ExternalImportDialog", "Choose RUNs to include:", None))
        self.RaiseErrorPushButton.setText(_translate("ExternalImportDialog", "err", None))
        self.foldernameLineEdit.setToolTip(_translate("ExternalImportDialog", "Comment string to be included in EXP", None))
        self.platemappathLineEdit.setToolTip(_translate("ExternalImportDialog", "Comment string to be included in EXP", None))
        self.label_8.setText(_translate("ExternalImportDialog", "ANA file. Save Action:", None))
        self.AnaSaveComboBox.setToolTip(_translate("ExternalImportDialog", "This \"use\" is specified in the EXP \n"
"and determines what types of analysis \n"
"can be performed", None))
        self.label_9.setText(_translate("ExternalImportDialog", "RCP file:", None))
        self.CalcXLineEdit.setText(_translate("ExternalImportDialog", "X+47.3", None))
        self.CalcYLineEdit.setText(_translate("ExternalImportDialog", "Y+50", None))
        self.label_16.setText(_translate("ExternalImportDialog", "Equations for calculating platemap x,y from motor X,Y", None))
        self.plateidLineEdit.setToolTip(_translate("ExternalImportDialog", "Comment string to be included in EXP", None))
        self.label_17.setText(_translate("ExternalImportDialog", "plate_id:", None))

