# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\ExternalImportForm.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)


class Ui_ExternalImportDialog(object):
    def setupUi(self, ExternalImportDialog):
        ExternalImportDialog.setObjectName("ExternalImportDialog")
        ExternalImportDialog.resize(1142, 882)
        self.ProfileComboBox = QtWidgets.QComboBox(ExternalImportDialog)
        self.ProfileComboBox.setGeometry(QtCore.QRect(10, 10, 271, 22))
        self.ProfileComboBox.setObjectName("ProfileComboBox")
        self.CreateFilesPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.CreateFilesPushButton.setGeometry(QtCore.QRect(10, 90, 151, 21))
        self.CreateFilesPushButton.setObjectName("CreateFilesPushButton")
        self.OpenFolderPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.OpenFolderPushButton.setGeometry(QtCore.QRect(10, 40, 71, 21))
        self.OpenFolderPushButton.setObjectName("OpenFolderPushButton")
        self.OpenPlatemapPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.OpenPlatemapPushButton.setGeometry(QtCore.QRect(10, 60, 81, 21))
        self.OpenPlatemapPushButton.setObjectName("OpenPlatemapPushButton")
        self.textBrowser_plate = QtWidgets.QTextBrowser(ExternalImportDialog)
        self.textBrowser_plate.setGeometry(QtCore.QRect(10, 460, 551, 361))
        self.textBrowser_plate.setObjectName("textBrowser_plate")
        self.AnaTreeWidget = QtWidgets.QTreeWidget(ExternalImportDialog)
        self.AnaTreeWidget.setGeometry(QtCore.QRect(580, 550, 551, 251))
        self.AnaTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AnaTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.AnaTreeWidget.setHeaderHidden(True)
        self.AnaTreeWidget.setExpandsOnDoubleClick(False)
        self.AnaTreeWidget.setObjectName("AnaTreeWidget")
        self.AnaTreeWidget.headerItem().setText(0, "1")
        self.AnaTreeWidget.header().setVisible(False)
        self.AnaTreeWidget.header().setCascadingSectionResizes(False)
        self.AnaTreeWidget.header().setStretchLastSection(True)
        self.label_7 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_7.setGeometry(QtCore.QRect(580, 270, 111, 21))
        self.label_7.setObjectName("label_7")
        self.ExpSaveComboBox = QtWidgets.QComboBox(ExternalImportDialog)
        self.ExpSaveComboBox.setGeometry(QtCore.QRect(690, 270, 267, 20))
        self.ExpSaveComboBox.setObjectName("ExpSaveComboBox")
        self.label_14 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_14.setGeometry(QtCore.QRect(10, 120, 191, 21))
        self.label_14.setObjectName("label_14")
        self.RunSelectTreeWidget = QtWidgets.QTreeWidget(ExternalImportDialog)
        self.RunSelectTreeWidget.setGeometry(QtCore.QRect(10, 140, 551, 311))
        self.RunSelectTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RunSelectTreeWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded
        )
        self.RunSelectTreeWidget.setHeaderHidden(True)
        self.RunSelectTreeWidget.setExpandsOnDoubleClick(False)
        self.RunSelectTreeWidget.setObjectName("RunSelectTreeWidget")
        self.RunSelectTreeWidget.headerItem().setText(0, "1")
        self.RunSelectTreeWidget.header().setVisible(False)
        self.RunSelectTreeWidget.header().setCascadingSectionResizes(False)
        self.RunSelectTreeWidget.header().setStretchLastSection(True)
        self.RaiseErrorPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(1120, 0, 31, 21))
        self.RaiseErrorPushButton.setObjectName("RaiseErrorPushButton")
        self.foldernameLineEdit = QtWidgets.QLineEdit(ExternalImportDialog)
        self.foldernameLineEdit.setGeometry(QtCore.QRect(90, 40, 191, 21))
        self.foldernameLineEdit.setText("")
        self.foldernameLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.foldernameLineEdit.setObjectName("foldernameLineEdit")
        self.platemappathLineEdit = QtWidgets.QLineEdit(ExternalImportDialog)
        self.platemappathLineEdit.setGeometry(QtCore.QRect(90, 60, 191, 21))
        self.platemappathLineEdit.setText("")
        self.platemappathLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.platemappathLineEdit.setObjectName("platemappathLineEdit")
        self.ExpTreeWidget = QtWidgets.QTreeWidget(ExternalImportDialog)
        self.ExpTreeWidget.setGeometry(QtCore.QRect(580, 290, 551, 231))
        self.ExpTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ExpTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.ExpTreeWidget.setHeaderHidden(True)
        self.ExpTreeWidget.setExpandsOnDoubleClick(False)
        self.ExpTreeWidget.setObjectName("ExpTreeWidget")
        self.ExpTreeWidget.headerItem().setText(0, "1")
        self.ExpTreeWidget.header().setVisible(False)
        self.ExpTreeWidget.header().setCascadingSectionResizes(False)
        self.ExpTreeWidget.header().setStretchLastSection(True)
        self.RcpTreeWidget = QtWidgets.QTreeWidget(ExternalImportDialog)
        self.RcpTreeWidget.setGeometry(QtCore.QRect(580, 20, 551, 241))
        self.RcpTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RcpTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.RcpTreeWidget.setHeaderHidden(True)
        self.RcpTreeWidget.setExpandsOnDoubleClick(False)
        self.RcpTreeWidget.setObjectName("RcpTreeWidget")
        self.RcpTreeWidget.headerItem().setText(0, "1")
        self.RcpTreeWidget.header().setVisible(False)
        self.RcpTreeWidget.header().setCascadingSectionResizes(False)
        self.RcpTreeWidget.header().setStretchLastSection(True)
        self.label_8 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_8.setGeometry(QtCore.QRect(580, 530, 111, 21))
        self.label_8.setObjectName("label_8")
        self.AnaSaveComboBox = QtWidgets.QComboBox(ExternalImportDialog)
        self.AnaSaveComboBox.setGeometry(QtCore.QRect(690, 530, 267, 20))
        self.AnaSaveComboBox.setObjectName("AnaSaveComboBox")
        self.label_9 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_9.setGeometry(QtCore.QRect(580, 0, 111, 21))
        self.label_9.setObjectName("label_9")
        self.CalcXLineEdit = QtWidgets.QLineEdit(ExternalImportDialog)
        self.CalcXLineEdit.setGeometry(QtCore.QRect(290, 60, 121, 20))
        self.CalcXLineEdit.setObjectName("CalcXLineEdit")
        self.CalcYLineEdit = QtWidgets.QLineEdit(ExternalImportDialog)
        self.CalcYLineEdit.setGeometry(QtCore.QRect(422, 60, 121, 20))
        self.CalcYLineEdit.setObjectName("CalcYLineEdit")
        self.label_16 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_16.setGeometry(QtCore.QRect(290, 40, 265, 21))
        self.label_16.setObjectName("label_16")
        self.plateidLineEdit = QtWidgets.QLineEdit(ExternalImportDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(340, 10, 51, 21))
        self.plateidLineEdit.setText("")
        self.plateidLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.plateidLineEdit.setObjectName("plateidLineEdit")
        self.label_17 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_17.setGeometry(QtCore.QRect(290, 10, 51, 21))
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.SaveFilesPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.SaveFilesPushButton.setGeometry(QtCore.QRect(270, 90, 131, 21))
        self.SaveFilesPushButton.setObjectName("SaveFilesPushButton")
        self.AddMiscAnaPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.AddMiscAnaPushButton.setGeometry(QtCore.QRect(970, 530, 131, 21))
        self.AddMiscAnaPushButton.setObjectName("AddMiscAnaPushButton")
        self.rcplabelLineEdit = QtWidgets.QLineEdit(ExternalImportDialog)
        self.rcplabelLineEdit.setGeometry(QtCore.QRect(460, 10, 71, 21))
        self.rcplabelLineEdit.setText("")
        self.rcplabelLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.rcplabelLineEdit.setObjectName("rcplabelLineEdit")
        self.label_18 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_18.setGeometry(QtCore.QRect(400, 10, 51, 21))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.AddToAnaPushButton = QtWidgets.QPushButton(ExternalImportDialog)
        self.AddToAnaPushButton.setGeometry(QtCore.QRect(170, 90, 91, 21))
        self.AddToAnaPushButton.setObjectName("AddToAnaPushButton")
        self.critdistSpinBox = QtWidgets.QDoubleSpinBox(ExternalImportDialog)
        self.critdistSpinBox.setGeometry(QtCore.QRect(511, 90, 51, 22))
        self.critdistSpinBox.setProperty("value", 2.0)
        self.critdistSpinBox.setObjectName("critdistSpinBox")
        self.label_19 = QtWidgets.QLabel(ExternalImportDialog)
        self.label_19.setGeometry(QtCore.QRect(420, 80, 91, 41))
        self.label_19.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_19.setObjectName("label_19")
        self.retranslateUi(ExternalImportDialog)
        QtCore.QMetaObject.connectSlotsByName(ExternalImportDialog)

    def retranslateUi(self, ExternalImportDialog):
        ExternalImportDialog.setWindowTitle(
            _translate("ExternalImportDialog", "Process Data, Calc FOM from EXP", None)
        )
        self.ProfileComboBox.setToolTip(
            _translate(
                "ExternalImportDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.CreateFilesPushButton.setToolTip(
            _translate(
                "ExternalImportDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.CreateFilesPushButton.setText(
            _translate("ExternalImportDialog", "Generate RCP/EXP/ANA", None)
        )
        self.OpenFolderPushButton.setToolTip(
            _translate(
                "ExternalImportDialog",
                "Import a .exp file, which will provide options for the data type, RUNs and analysis type",
                None,
            )
        )
        self.OpenFolderPushButton.setText(
            _translate("ExternalImportDialog", "Select Folder", None)
        )
        self.OpenPlatemapPushButton.setToolTip(
            _translate(
                "ExternalImportDialog",
                'Grab the EXP from the "Create EXP" window',
                None,
            )
        )
        self.OpenPlatemapPushButton.setText(
            _translate("ExternalImportDialog", "Open platemap", None)
        )
        self.label_7.setText(
            _translate("ExternalImportDialog", "EXP file. Save Action:", None)
        )
        self.ExpSaveComboBox.setToolTip(
            _translate(
                "ExternalImportDialog",
                'This "use" is specified in the EXP \n'
                "and determines what types of analysis \n"
                "can be performed",
                None,
            )
        )
        self.label_14.setText(
            _translate("ExternalImportDialog", "Choose Data to include:", None)
        )
        self.RaiseErrorPushButton.setText(
            _translate("ExternalImportDialog", "err", None)
        )
        self.foldernameLineEdit.setToolTip(
            _translate(
                "ExternalImportDialog", "Comment string to be included in EXP", None
            )
        )
        self.platemappathLineEdit.setToolTip(
            _translate(
                "ExternalImportDialog", "Comment string to be included in EXP", None
            )
        )
        self.label_8.setText(
            _translate("ExternalImportDialog", "ANA file. Save Action:", None)
        )
        self.AnaSaveComboBox.setToolTip(
            _translate(
                "ExternalImportDialog",
                'This "use" is specified in the EXP \n'
                "and determines what types of analysis \n"
                "can be performed",
                None,
            )
        )
        self.label_9.setText(_translate("ExternalImportDialog", "RCP file:", None))
        self.CalcXLineEdit.setText(_translate("ExternalImportDialog", "Y+50.", None))
        self.CalcYLineEdit.setText(_translate("ExternalImportDialog", "X+47.3", None))
        self.label_16.setText(
            _translate(
                "ExternalImportDialog",
                "Equations for calculating platemap x,y from motor X,Y",
                None,
            )
        )
        self.plateidLineEdit.setToolTip(
            _translate(
                "ExternalImportDialog", "Comment string to be included in EXP", None
            )
        )
        self.label_17.setText(_translate("ExternalImportDialog", "plate_id:", None))
        self.SaveFilesPushButton.setToolTip(
            _translate(
                "ExternalImportDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.SaveFilesPushButton.setText(
            _translate("ExternalImportDialog", "Save RCP/EXP/ANA", None)
        )
        self.AddMiscAnaPushButton.setToolTip(
            _translate(
                "ExternalImportDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.AddMiscAnaPushButton.setText(
            _translate("ExternalImportDialog", "Add Misc File", None)
        )
        self.rcplabelLineEdit.setToolTip(
            _translate(
                "ExternalImportDialog", "Comment string to be included in EXP", None
            )
        )
        self.label_18.setText(_translate("ExternalImportDialog", "rcp label:", None))
        self.AddToAnaPushButton.setToolTip(
            _translate(
                "ExternalImportDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.AddToAnaPushButton.setText(
            _translate("ExternalImportDialog", "Addtl Analysis", None)
        )
        self.label_19.setText(
            _translate(
                "ExternalImportDialog", "crit. distance for\n" "sample assignment", None
            )
        )
