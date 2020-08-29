# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\CalcFOMForm.ui'
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


class Ui_CalcFOMDialog(object):
    def setupUi(self, CalcFOMDialog):
        CalcFOMDialog.setObjectName("CalcFOMDialog")
        CalcFOMDialog.resize(1142, 882)
        self.BatchComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.BatchComboBox.setGeometry(QtCore.QRect(10, 80, 271, 22))
        self.BatchComboBox.setObjectName("BatchComboBox")
        self.BatchPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.BatchPushButton.setGeometry(QtCore.QRect(10, 60, 131, 21))
        self.BatchPushButton.setObjectName("BatchPushButton")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(CalcFOMDialog)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 360, 181, 163))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_17.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_18.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 2, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_19.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_19.setObjectName("label_19")
        self.gridLayout_2.addWidget(self.label_19, 3, 0, 1, 1)
        self.UserNameLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.UserNameLineEdit.setObjectName("UserNameLineEdit")
        self.gridLayout_2.addWidget(self.UserNameLineEdit, 2, 1, 1, 1)
        self.AnaTypeLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.AnaTypeLineEdit.setObjectName("AnaTypeLineEdit")
        self.gridLayout_2.addWidget(self.AnaTypeLineEdit, 0, 1, 1, 1)
        self.AnaNameLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.AnaNameLineEdit.setEnabled(False)
        self.AnaNameLineEdit.setObjectName("AnaNameLineEdit")
        self.gridLayout_2.addWidget(self.AnaNameLineEdit, 1, 1, 1, 1)
        self.AccessLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.AccessLineEdit.setObjectName("AccessLineEdit")
        self.gridLayout_2.addWidget(self.AccessLineEdit, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_16.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 0, 0, 1, 1)
        self.AnaDescLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.AnaDescLineEdit.setObjectName("AnaDescLineEdit")
        self.gridLayout_2.addWidget(self.AnaDescLineEdit, 5, 0, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 2)
        self.ImportExpPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.ImportExpPushButton.setGeometry(QtCore.QRect(0, 30, 71, 21))
        self.ImportExpPushButton.setObjectName("ImportExpPushButton")
        self.ImportAnaPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.ImportAnaPushButton.setGeometry(QtCore.QRect(0, 10, 71, 21))
        self.ImportAnaPushButton.setObjectName("ImportAnaPushButton")
        self.textBrowser_plate = QtWidgets.QTextBrowser(CalcFOMDialog)
        self.textBrowser_plate.setGeometry(QtCore.QRect(570, 530, 561, 341))
        self.textBrowser_plate.setObjectName("textBrowser_plate")
        self.textBrowser_h = QtWidgets.QTextBrowser(CalcFOMDialog)
        self.textBrowser_h.setGeometry(QtCore.QRect(760, 20, 371, 231))
        self.textBrowser_h.setObjectName("textBrowser_h")
        self.textBrowser_comp = QtWidgets.QTextBrowser(CalcFOMDialog)
        self.textBrowser_comp.setGeometry(QtCore.QRect(510, 250, 621, 281))
        self.textBrowser_comp.setObjectName("textBrowser_comp")
        self.line = QtWidgets.QFrame(CalcFOMDialog)
        self.line.setGeometry(QtCore.QRect(276, 10, 20, 351))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(CalcFOMDialog)
        self.line_2.setGeometry(QtCore.QRect(500, 0, 20, 521))
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(CalcFOMDialog)
        self.line_3.setGeometry(QtCore.QRect(0, 350, 281, 20))
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(CalcFOMDialog)
        self.line_4.setGeometry(QtCore.QRect(0, 99, 281, 21))
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.AnalysisNamesComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.AnalysisNamesComboBox.setGeometry(QtCore.QRect(200, 410, 301, 22))
        self.AnalysisNamesComboBox.setObjectName("AnalysisNamesComboBox")
        self.label_20 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_20.setGeometry(QtCore.QRect(208, 390, 301, 21))
        self.label_20.setObjectName("label_20")
        self.AnaTreeWidget = QtWidgets.QTreeWidget(CalcFOMDialog)
        self.AnaTreeWidget.setGeometry(QtCore.QRect(10, 530, 551, 341))
        self.AnaTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AnaTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.AnaTreeWidget.setHeaderHidden(True)
        self.AnaTreeWidget.setExpandsOnDoubleClick(False)
        self.AnaTreeWidget.setObjectName("AnaTreeWidget")
        self.AnaTreeWidget.headerItem().setText(0, "1")
        self.AnaTreeWidget.header().setVisible(False)
        self.AnaTreeWidget.header().setCascadingSectionResizes(False)
        self.AnaTreeWidget.header().setStretchLastSection(True)
        self.getplatemapCheckBox = QtWidgets.QCheckBox(CalcFOMDialog)
        self.getplatemapCheckBox.setGeometry(QtCore.QRect(170, 10, 111, 21))
        self.getplatemapCheckBox.setChecked(True)
        self.getplatemapCheckBox.setObjectName("getplatemapCheckBox")
        self.CompPlotOrderComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.CompPlotOrderComboBox.setGeometry(QtCore.QRect(520, 220, 111, 22))
        self.CompPlotOrderComboBox.setObjectName("CompPlotOrderComboBox")
        self.label_2 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_2.setGeometry(QtCore.QRect(520, 200, 111, 21))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(CalcFOMDialog)
        self.label.setGeometry(QtCore.QRect(520, 90, 111, 16))
        self.label.setObjectName("label")
        self.CompPlotTypeComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.CompPlotTypeComboBox.setGeometry(QtCore.QRect(520, 110, 111, 31))
        self.CompPlotTypeComboBox.setObjectName("CompPlotTypeComboBox")
        self.label_4 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_4.setGeometry(QtCore.QRect(520, 150, 111, 21))
        self.label_4.setObjectName("label_4")
        self.compplotsizeLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.compplotsizeLineEdit.setGeometry(QtCore.QRect(520, 170, 111, 22))
        self.compplotsizeLineEdit.setObjectName("compplotsizeLineEdit")
        self.label_3 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_3.setGeometry(QtCore.QRect(520, 40, 119, 21))
        self.label_3.setObjectName("label_3")
        self.fomplotchoiceComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.fomplotchoiceComboBox.setGeometry(QtCore.QRect(520, 60, 111, 22))
        self.fomplotchoiceComboBox.setObjectName("fomplotchoiceComboBox")
        self.usedaqtimeCheckBox = QtWidgets.QCheckBox(CalcFOMDialog)
        self.usedaqtimeCheckBox.setGeometry(QtCore.QRect(640, 50, 119, 20))
        self.usedaqtimeCheckBox.setObjectName("usedaqtimeCheckBox")
        self.label_9 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_9.setGeometry(QtCore.QRect(640, 80, 119, 16))
        self.label_9.setObjectName("label_9")
        self.aboverangecolLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.aboverangecolLineEdit.setGeometry(QtCore.QRect(640, 100, 119, 22))
        self.aboverangecolLineEdit.setObjectName("aboverangecolLineEdit")
        self.label_6 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_6.setGeometry(QtCore.QRect(640, 120, 119, 20))
        self.label_6.setObjectName("label_6")
        self.belowrangecolLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.belowrangecolLineEdit.setGeometry(QtCore.QRect(640, 140, 119, 22))
        self.belowrangecolLineEdit.setObjectName("belowrangecolLineEdit")
        self.label_8 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_8.setGeometry(QtCore.QRect(640, 160, 119, 21))
        self.label_8.setObjectName("label_8")
        self.vminmaxLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.vminmaxLineEdit.setGeometry(QtCore.QRect(640, 180, 119, 22))
        self.vminmaxLineEdit.setObjectName("vminmaxLineEdit")
        self.stdcsvplotchoiceComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.stdcsvplotchoiceComboBox.setGeometry(QtCore.QRect(520, 20, 111, 22))
        self.stdcsvplotchoiceComboBox.setObjectName("stdcsvplotchoiceComboBox")
        self.label_5 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_5.setGeometry(QtCore.QRect(520, 0, 119, 21))
        self.label_5.setObjectName("label_5")
        self.colormapLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.colormapLineEdit.setGeometry(QtCore.QRect(640, 220, 119, 22))
        self.colormapLineEdit.setObjectName("colormapLineEdit")
        self.label_10 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_10.setGeometry(QtCore.QRect(640, 200, 119, 21))
        self.label_10.setObjectName("label_10")
        self.label_13 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_13.setGeometry(QtCore.QRect(290, 150, 219, 21))
        self.label_13.setObjectName("label_13")
        self.TechTypeRadioButton_0 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_0.setGeometry(QtCore.QRect(290, 170, 219, 16))
        self.TechTypeRadioButton_0.setText("")
        self.TechTypeRadioButton_0.setObjectName("TechTypeRadioButton_0")
        self.TechTypeButtonGroup = QtWidgets.QButtonGroup(CalcFOMDialog)
        self.TechTypeButtonGroup.setObjectName("TechTypeButtonGroup")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_0)
        self.TechTypeRadioButton_1 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_1.setGeometry(QtCore.QRect(290, 190, 219, 16))
        self.TechTypeRadioButton_1.setText("")
        self.TechTypeRadioButton_1.setObjectName("TechTypeRadioButton_1")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_1)
        self.TechTypeRadioButton_2 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_2.setGeometry(QtCore.QRect(290, 210, 219, 16))
        self.TechTypeRadioButton_2.setText("")
        self.TechTypeRadioButton_2.setObjectName("TechTypeRadioButton_2")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_2)
        self.TechTypeRadioButton_3 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_3.setGeometry(QtCore.QRect(290, 230, 219, 16))
        self.TechTypeRadioButton_3.setText("")
        self.TechTypeRadioButton_3.setObjectName("TechTypeRadioButton_3")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_3)
        self.TechTypeRadioButton_4 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_4.setGeometry(QtCore.QRect(290, 250, 219, 16))
        self.TechTypeRadioButton_4.setText("")
        self.TechTypeRadioButton_4.setObjectName("TechTypeRadioButton_4")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_4)
        self.TechTypeRadioButton_5 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_5.setGeometry(QtCore.QRect(290, 270, 219, 16))
        self.TechTypeRadioButton_5.setText("")
        self.TechTypeRadioButton_5.setObjectName("TechTypeRadioButton_5")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_5)
        self.TechTypeRadioButton_6 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_6.setGeometry(QtCore.QRect(290, 290, 219, 16))
        self.TechTypeRadioButton_6.setText("")
        self.TechTypeRadioButton_6.setObjectName("TechTypeRadioButton_6")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_6)
        self.TechTypeRadioButton_7 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_7.setGeometry(QtCore.QRect(290, 310, 219, 16))
        self.TechTypeRadioButton_7.setText("")
        self.TechTypeRadioButton_7.setObjectName("TechTypeRadioButton_7")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_7)
        self.TechTypeRadioButton_8 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_8.setGeometry(QtCore.QRect(290, 330, 219, 16))
        self.TechTypeRadioButton_8.setText("")
        self.TechTypeRadioButton_8.setObjectName("TechTypeRadioButton_8")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_8)
        self.TechTypeRadioButton_9 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_9.setGeometry(QtCore.QRect(290, 350, 219, 16))
        self.TechTypeRadioButton_9.setText("")
        self.TechTypeRadioButton_9.setObjectName("TechTypeRadioButton_9")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_9)
        self.TechTypeRadioButton_10 = QtWidgets.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_10.setGeometry(QtCore.QRect(290, 370, 219, 16))
        self.TechTypeRadioButton_10.setText("")
        self.TechTypeRadioButton_10.setObjectName("TechTypeRadioButton_10")
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_10)
        self.label_7 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 267, 21))
        self.label_7.setObjectName("label_7")
        self.ExpRunUseComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.ExpRunUseComboBox.setGeometry(QtCore.QRect(0, 130, 267, 20))
        self.ExpRunUseComboBox.setObjectName("ExpRunUseComboBox")
        self.label_14 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_14.setGeometry(QtCore.QRect(10, 150, 265, 21))
        self.label_14.setObjectName("label_14")
        self.RunSelectTreeWidget = QtWidgets.QTreeWidget(CalcFOMDialog)
        self.RunSelectTreeWidget.setGeometry(QtCore.QRect(10, 170, 271, 181))
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
        self.UserFOMLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.UserFOMLineEdit.setGeometry(QtCore.QRect(200, 500, 301, 20))
        self.UserFOMLineEdit.setObjectName("UserFOMLineEdit")
        self.line_5 = QtWidgets.QFrame(CalcFOMDialog)
        self.line_5.setGeometry(QtCore.QRect(0, 50, 281, 21))
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_21 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_21.setGeometry(QtCore.QRect(208, 480, 301, 20))
        self.label_21.setObjectName("label_21")
        self.FOMProcessNamesComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.FOMProcessNamesComboBox.setGeometry(QtCore.QRect(200, 450, 301, 22))
        self.FOMProcessNamesComboBox.setObjectName("FOMProcessNamesComboBox")
        self.label_22 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_22.setGeometry(QtCore.QRect(208, 430, 301, 21))
        self.label_22.setObjectName("label_22")
        self.autoplotCheckBox = QtWidgets.QCheckBox(CalcFOMDialog)
        self.autoplotCheckBox.setGeometry(QtCore.QRect(640, 20, 119, 20))
        self.autoplotCheckBox.setChecked(True)
        self.autoplotCheckBox.setObjectName("autoplotCheckBox")
        self.RaiseErrorPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(1120, 0, 31, 21))
        self.RaiseErrorPushButton.setObjectName("RaiseErrorPushButton")
        self.OpenInfoPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.OpenInfoPushButton.setGeometry(QtCore.QRect(70, 10, 91, 21))
        self.OpenInfoPushButton.setObjectName("OpenInfoPushButton")
        self.expfilenameLineEdit = QtWidgets.QLineEdit(CalcFOMDialog)
        self.expfilenameLineEdit.setGeometry(QtCore.QRect(70, 30, 211, 21))
        self.expfilenameLineEdit.setText("")
        self.expfilenameLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.expfilenameLineEdit.setObjectName("expfilenameLineEdit")
        self.line_6 = QtWidgets.QFrame(CalcFOMDialog)
        self.line_6.setGeometry(QtCore.QRect(189, 360, 16, 161))
        self.line_6.setLineWidth(2)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.EditAnalysisParamsPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.EditAnalysisParamsPushButton.setGeometry(QtCore.QRect(290, 70, 102, 21))
        self.EditAnalysisParamsPushButton.setObjectName("EditAnalysisParamsPushButton")
        self.AnalyzeDataPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.AnalyzeDataPushButton.setGeometry(QtCore.QRect(290, 90, 102, 21))
        self.AnalyzeDataPushButton.setObjectName("AnalyzeDataPushButton")
        self.ImportAnalysisParamsPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.ImportAnalysisParamsPushButton.setGeometry(QtCore.QRect(400, 10, 102, 20))
        self.ImportAnalysisParamsPushButton.setObjectName(
            "ImportAnalysisParamsPushButton"
        )
        self.SaveAnaPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.SaveAnaPushButton.setGeometry(QtCore.QRect(290, 111, 102, 20))
        self.SaveAnaPushButton.setObjectName("SaveAnaPushButton")
        self.SaveViewPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.SaveViewPushButton.setGeometry(QtCore.QRect(290, 130, 102, 21))
        self.SaveViewPushButton.setObjectName("SaveViewPushButton")
        self.EditDfltVisPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.EditDfltVisPushButton.setGeometry(QtCore.QRect(400, 30, 102, 23))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.EditDfltVisPushButton.sizePolicy().hasHeightForWidth()
        )
        self.EditDfltVisPushButton.setSizePolicy(sizePolicy)
        self.EditDfltVisPushButton.setObjectName("EditDfltVisPushButton")
        self.ClearAnalysisPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.ClearAnalysisPushButton.setGeometry(QtCore.QRect(290, 10, 102, 21))
        self.ClearAnalysisPushButton.setObjectName("ClearAnalysisPushButton")
        self.ClearSingleAnalysisPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.ClearSingleAnalysisPushButton.setGeometry(QtCore.QRect(290, 32, 102, 21))
        self.ClearSingleAnalysisPushButton.setObjectName(
            "ClearSingleAnalysisPushButton"
        )
        self.ViewResultPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.ViewResultPushButton.setGeometry(QtCore.QRect(400, 132, 102, 21))
        self.ViewResultPushButton.setObjectName("ViewResultPushButton")
        self.UpdatePlotPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.UpdatePlotPushButton.setGeometry(QtCore.QRect(400, 111, 101, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.UpdatePlotPushButton.sizePolicy().hasHeightForWidth()
        )
        self.UpdatePlotPushButton.setSizePolicy(sizePolicy)
        self.UpdatePlotPushButton.setObjectName("UpdatePlotPushButton")
        self.OpenAuxExpAnaPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.OpenAuxExpAnaPushButton.setGeometry(QtCore.QRect(400, 70, 101, 21))
        self.OpenAuxExpAnaPushButton.setObjectName("OpenAuxExpAnaPushButton")
        self.AttachMiscPushButton = QtWidgets.QPushButton(CalcFOMDialog)
        self.AttachMiscPushButton.setGeometry(QtCore.QRect(400, 90, 101, 21))
        self.AttachMiscPushButton.setObjectName("AttachMiscPushButton")
        self.retranslateUi(CalcFOMDialog)
        QtCore.QMetaObject.connectSlotsByName(CalcFOMDialog)

    def retranslateUi(self, CalcFOMDialog):
        CalcFOMDialog.setWindowTitle(
            _translate("CalcFOMDialog", "Process Data, Calc FOM from EXP", None)
        )
        self.BatchComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.BatchPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.BatchPushButton.setText(
            _translate("CalcFOMDialog", "Run Batch Process:", None)
        )
        self.label_17.setText(_translate("CalcFOMDialog", "Analysis name:", None))
        self.label_18.setText(_translate("CalcFOMDialog", "created by:", None))
        self.label_19.setText(_translate("CalcFOMDialog", "access:", None))
        self.UserNameLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.UserNameLineEdit.setText(_translate("CalcFOMDialog", "eche", None))
        self.AnaTypeLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.AnaTypeLineEdit.setText(_translate("CalcFOMDialog", "eche", None))
        self.AnaNameLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.AnaNameLineEdit.setText(_translate("CalcFOMDialog", "eche", None))
        self.AccessLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.AccessLineEdit.setText(_translate("CalcFOMDialog", "hte", None))
        self.label_16.setText(_translate("CalcFOMDialog", "Analysis type:", None))
        self.AnaDescLineEdit.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Comment string to be included in EXP.\n"
                'If you modify the beginning with a"<comment>;" the \n'
                "comment will remain as you change analysis options",
                None,
            )
        )
        self.label_11.setText(
            _translate("CalcFOMDialog", "Analysis description:", None)
        )
        self.ImportExpPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Import a .exp file, which will provide options for the data type, RUNs and analysis type",
                None,
            )
        )
        self.ImportExpPushButton.setText(
            _translate("CalcFOMDialog", "Import EXP", None)
        )
        self.ImportAnaPushButton.setToolTip(
            _translate(
                "CalcFOMDialog", 'Grab the EXP from the "Create EXP" window', None
            )
        )
        self.ImportAnaPushButton.setText(_translate("CalcFOMDialog", "Open ANA", None))
        self.AnalysisNamesComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "The name of the functions that will be applied to data\n"
                "to generate Intermediate and FOM results",
                None,
            )
        )
        self.label_20.setText(
            _translate("CalcFOMDialog", "Choose analysis function:", None)
        )
        self.getplatemapCheckBox.setText(
            _translate("CalcFOMDialog", "Get platemaps", None)
        )
        self.CompPlotOrderComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_2.setText(_translate("CalcFOMDialog", "Element plot order:", None))
        self.label.setText(_translate("CalcFOMDialog", "Comp. plot type:", None))
        self.CompPlotTypeComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_4.setText(_translate("CalcFOMDialog", "Comp. point size:", None))
        self.compplotsizeLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.compplotsizeLineEdit.setText(_translate("CalcFOMDialog", "patch", None))
        self.label_3.setText(_translate("CalcFOMDialog", "fom to plot", None))
        self.fomplotchoiceComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.usedaqtimeCheckBox.setText(
            _translate("CalcFOMDialog", "Use DAQ time", None)
        )
        self.label_9.setText(_translate("CalcFOMDialog", "above color", None))
        self.aboverangecolLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.label_6.setText(_translate("CalcFOMDialog", "below color", None))
        self.belowrangecolLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.label_8.setText(_translate("CalcFOMDialog", "fom range min,max", None))
        self.vminmaxLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.stdcsvplotchoiceComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_5.setText(_translate("CalcFOMDialog", "standard plot", None))
        self.colormapLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.colormapLineEdit.setText(_translate("CalcFOMDialog", "jet", None))
        self.label_10.setText(_translate("CalcFOMDialog", "colormap", None))
        self.label_13.setText(
            _translate("CalcFOMDialog", "Choose analysis scope:", None)
        )
        self.label_7.setText(
            _translate("CalcFOMDialog", "Primary data type (run_use)", None)
        )
        self.ExpRunUseComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                'This "use" is specified in the EXP \n'
                "and determines what types of analysis \n"
                "can be performed",
                None,
            )
        )
        self.label_14.setText(
            _translate("CalcFOMDialog", "Choose RUNs to include:", None)
        )
        self.UserFOMLineEdit.setToolTip(
            _translate(
                "CalcFOMDialog",
                "enter comma-delimited list of string or\n"
                'number FOMS that will become a constant column in the .csv generated by "Analyze Data".\n'
                "After entry complete, you will be prompted for fom names",
                None,
            )
        )
        self.label_21.setText(_translate("CalcFOMDialog", "User-defined FOMs", None))
        self.FOMProcessNamesComboBox.setToolTip(
            _translate(
                "CalcFOMDialog",
                "The name of the functions that will be applied to data\n"
                "to generate Intermediate and FOM results",
                None,
            )
        )
        self.label_22.setText(
            _translate("CalcFOMDialog", "Choose FOM post-process function:", None)
        )
        self.autoplotCheckBox.setText(
            _translate("CalcFOMDialog", "Auto plot ana__x", None)
        )
        self.RaiseErrorPushButton.setText(_translate("CalcFOMDialog", "err", None))
        self.OpenInfoPushButton.setText(
            _translate("CalcFOMDialog", "Open via Search", None)
        )
        self.expfilenameLineEdit.setToolTip(
            _translate("CalcFOMDialog", "Comment string to be included in EXP", None)
        )
        self.EditAnalysisParamsPushButton.setToolTip(
            _translate("CalcFOMDialog", "Edit parameters involved inthe analysis", None)
        )
        self.EditAnalysisParamsPushButton.setText(
            _translate("CalcFOMDialog", "Edit Params", None)
        )
        self.AnalyzeDataPushButton.setToolTip(
            _translate("CalcFOMDialog", "Perform the selected analysis", None)
        )
        self.AnalyzeDataPushButton.setText(
            _translate("CalcFOMDialog", "Analyze Data", None)
        )
        self.ImportAnalysisParamsPushButton.setToolTip(
            _translate("CalcFOMDialog", "Import a .par file", None)
        )
        self.ImportAnalysisParamsPushButton.setText(
            _translate("CalcFOMDialog", "Import Params", None)
        )
        self.SaveAnaPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Save .fom, FOR THE SELECTED ANALYSIS TYPE ONLY.\n"
                " Intermediate data will also be saved",
                None,
            )
        )
        self.SaveAnaPushButton.setText(_translate("CalcFOMDialog", "Save ANA", None))
        self.SaveViewPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Send Raw, Intermediate and FOM data to the Visualize window",
                None,
            )
        )
        self.SaveViewPushButton.setText(_translate("CalcFOMDialog", "Save+View", None))
        self.EditDfltVisPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Edit the FOM visualization parameters in the .csv\n"
                'ONLY WORKS ON MOST RECENT "Analyze Data"',
                None,
            )
        )
        self.EditDfltVisPushButton.setText(
            _translate("CalcFOMDialog", "Update Dflt Vis", None)
        )
        self.ClearAnalysisPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Clear the analysis, removing intermediate data and FOMs",
                None,
            )
        )
        self.ClearAnalysisPushButton.setText(
            _translate("CalcFOMDialog", "Clear Analysis", None)
        )
        self.ClearSingleAnalysisPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Clear the analysis, removing intermediate data and FOMs",
                None,
            )
        )
        self.ClearSingleAnalysisPushButton.setText(
            _translate("CalcFOMDialog", "Del 1 ana__x", None)
        )
        self.ViewResultPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Send Raw, Intermediate and FOM data to the Visualize window",
                None,
            )
        )
        self.ViewResultPushButton.setText(
            _translate("CalcFOMDialog", "View Result", None)
        )
        self.UpdatePlotPushButton.setToolTip(
            _translate(
                "CalcFOMDialog",
                "Edit the FOM visualization parameters in the .csv\n"
                'ONLY WORKS ON MOST RECENT "Analyze Data"',
                None,
            )
        )
        self.UpdatePlotPushButton.setText(
            _translate("CalcFOMDialog", "Update Plots", None)
        )
        self.OpenAuxExpAnaPushButton.setToolTip(
            _translate("CalcFOMDialog", "Perform the selected analysis", None)
        )
        self.OpenAuxExpAnaPushButton.setText(
            _translate("CalcFOMDialog", "SelectAuxEXP/ANA", None)
        )
        self.AttachMiscPushButton.setToolTip(
            _translate("CalcFOMDialog", "Perform the selected analysis", None)
        )
        self.AttachMiscPushButton.setText(
            _translate("CalcFOMDialog", "Attach Files to ana", None)
        )
