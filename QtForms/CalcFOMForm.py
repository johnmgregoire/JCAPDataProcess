# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\CalcFOMForm.ui'
#
# Created: Fri Mar 11 22:03:13 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 360, 261, 163))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 2)
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
        self.layoutWidget = QtWidgets.QWidget(CalcFOMDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(290, 10, 212, 141))
        self.layoutWidget.setObjectName("layoutWidget")
        self.AnalysisGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.AnalysisGridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.AnalysisGridLayout.setContentsMargins(0, 0, 0, 0)
        self.AnalysisGridLayout.setObjectName("AnalysisGridLayout")
        self.AnalyzeDataPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.AnalyzeDataPushButton.setObjectName("AnalyzeDataPushButton")
        self.AnalysisGridLayout.addWidget(self.AnalyzeDataPushButton, 0, 1, 1, 1)
        self.EditDfltVisPushButton = QtWidgets.QPushButton(self.layoutWidget)
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
        self.AnalysisGridLayout.addWidget(self.EditDfltVisPushButton, 1, 1, 1, 1)
        self.ClearAnalysisPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ClearAnalysisPushButton.setObjectName("ClearAnalysisPushButton")
        self.AnalysisGridLayout.addWidget(self.ClearAnalysisPushButton, 2, 1, 1, 1)
        self.EditAnalysisParamsPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.EditAnalysisParamsPushButton.setObjectName("EditAnalysisParamsPushButton")
        self.AnalysisGridLayout.addWidget(self.EditAnalysisParamsPushButton, 0, 0, 1, 1)
        self.SaveAnaPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.SaveAnaPushButton.setObjectName("SaveAnaPushButton")
        self.AnalysisGridLayout.addWidget(self.SaveAnaPushButton, 2, 0, 1, 1)
        self.ImportAnalysisParamsPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ImportAnalysisParamsPushButton.setObjectName(
            "ImportAnalysisParamsPushButton"
        )
        self.AnalysisGridLayout.addWidget(
            self.ImportAnalysisParamsPushButton, 1, 0, 1, 1
        )
        self.ViewResultPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ViewResultPushButton.setObjectName("ViewResultPushButton")
        self.AnalysisGridLayout.addWidget(self.ViewResultPushButton, 3, 0, 1, 1)
        self.ClearSingleAnalysisPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ClearSingleAnalysisPushButton.setObjectName(
            "ClearSingleAnalysisPushButton"
        )
        self.AnalysisGridLayout.addWidget(
            self.ClearSingleAnalysisPushButton, 3, 1, 1, 1
        )
        self.SaveViewPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.SaveViewPushButton.setObjectName("SaveViewPushButton")
        self.AnalysisGridLayout.addWidget(self.SaveViewPushButton, 4, 0, 1, 1)
        self.UpdatePlotPushButton = QtWidgets.QPushButton(self.layoutWidget)
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
        self.AnalysisGridLayout.addWidget(self.UpdatePlotPushButton, 4, 1, 1, 1)
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
        self.line.setGeometry(QtCore.QRect(276, 10, 20, 511))
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
        self.AnalysisNamesComboBox.setGeometry(QtCore.QRect(290, 410, 211, 22))
        self.AnalysisNamesComboBox.setObjectName("AnalysisNamesComboBox")
        self.label_20 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_20.setGeometry(QtCore.QRect(290, 390, 219, 21))
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
        self.UserFOMLineEdit.setGeometry(QtCore.QRect(290, 500, 211, 20))
        self.UserFOMLineEdit.setObjectName("UserFOMLineEdit")
        self.line_5 = QtWidgets.QFrame(CalcFOMDialog)
        self.line_5.setGeometry(QtCore.QRect(0, 50, 281, 21))
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_21 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_21.setGeometry(QtCore.QRect(290, 480, 219, 20))
        self.label_21.setObjectName("label_21")
        self.FOMProcessNamesComboBox = QtWidgets.QComboBox(CalcFOMDialog)
        self.FOMProcessNamesComboBox.setGeometry(QtCore.QRect(290, 450, 211, 22))
        self.FOMProcessNamesComboBox.setObjectName("FOMProcessNamesComboBox")
        self.label_22 = QtWidgets.QLabel(CalcFOMDialog)
        self.label_22.setGeometry(QtCore.QRect(290, 430, 219, 21))
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
        self.retranslateUi(CalcFOMDialog)
        QtCore.QMetaObject.connectSlotsByName(CalcFOMDialog)

    def retranslateUi(self, CalcFOMDialog):
        CalcFOMDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Process Data, Calc FOM from EXP", None
            )
        )
        self.BatchComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.BatchPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.BatchPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Run Batch Process:", None
            )
        )
        self.label_11.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Analysis description:", None
            )
        )
        self.label_17.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Analysis name:", None)
        )
        self.label_18.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "created by:", None)
        )
        self.label_19.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "access:", None)
        )
        self.UserNameLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.UserNameLineEdit.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "eche", None)
        )
        self.AnaTypeLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.AnaTypeLineEdit.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "eche", None)
        )
        self.AnaNameLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.AnaNameLineEdit.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "eche", None)
        )
        self.AccessLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.AccessLineEdit.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "hte", None)
        )
        self.label_16.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Analysis type:", None)
        )
        self.AnaDescLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Comment string to be included in EXP.\n"
                'If you modify the beginning with a"<comment>;" the \n'
                "comment will remain as you change analysis options",
                None,
            )
        )
        self.AnalyzeDataPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Perform the selected analysis", None
            )
        )
        self.AnalyzeDataPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Analyze Data", None)
        )
        self.EditDfltVisPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Edit the FOM visualization parameters in the .csv\n"
                'ONLY WORKS ON MOST RECENT "Analyze Data"',
                None,
            )
        )
        self.EditDfltVisPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Update Dflt Vis", None)
        )
        self.ClearAnalysisPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Clear the analysis, removing intermediate data and FOMs",
                None,
            )
        )
        self.ClearAnalysisPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Clear Analysis", None)
        )
        self.EditAnalysisParamsPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Edit parameters involved inthe analysis", None
            )
        )
        self.EditAnalysisParamsPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Edit Params", None)
        )
        self.SaveAnaPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Save .fom, FOR THE SELECTED ANALYSIS TYPE ONLY.\n"
                " Intermediate data will also be saved",
                None,
            )
        )
        self.SaveAnaPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Save ANA", None)
        )
        self.ImportAnalysisParamsPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Import a .par file", None
            )
        )
        self.ImportAnalysisParamsPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Import Params", None)
        )
        self.ViewResultPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Send Raw, Intermediate and FOM data to the Visualize window",
                None,
            )
        )
        self.ViewResultPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "View Result", None)
        )
        self.ClearSingleAnalysisPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Clear the analysis, removing intermediate data and FOMs",
                None,
            )
        )
        self.ClearSingleAnalysisPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Del 1 ana__x", None)
        )
        self.SaveViewPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Send Raw, Intermediate and FOM data to the Visualize window",
                None,
            )
        )
        self.SaveViewPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Save+View", None)
        )
        self.UpdatePlotPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Edit the FOM visualization parameters in the .csv\n"
                'ONLY WORKS ON MOST RECENT "Analyze Data"',
                None,
            )
        )
        self.UpdatePlotPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Update Plots", None)
        )
        self.ImportExpPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Import a .exp file, which will provide options for the data type, RUNs and analysis type",
                None,
            )
        )
        self.ImportExpPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Import EXP", None)
        )
        self.ImportAnaPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", 'Grab the EXP from the "Create EXP" window', None
            )
        )
        self.ImportAnaPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Open ANA", None)
        )
        self.AnalysisNamesComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "The name of the functions that will be applied to data\n"
                "to generate Intermediate and FOM results",
                None,
            )
        )
        self.label_20.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Choose analysis function:", None
            )
        )
        self.getplatemapCheckBox.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Get platemaps", None)
        )
        self.CompPlotOrderComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Element plot order:", None
            )
        )
        self.label.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Comp. plot type:", None)
        )
        self.CompPlotTypeComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_4.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comp. point size:", None
            )
        )
        self.compplotsizeLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.compplotsizeLineEdit.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "patch", None)
        )
        self.label_3.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "fom to plot", None)
        )
        self.fomplotchoiceComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.usedaqtimeCheckBox.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Use DAQ time", None)
        )
        self.label_9.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "above color", None)
        )
        self.aboverangecolLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.label_6.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "below color", None)
        )
        self.belowrangecolLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.label_8.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "fom range min,max", None
            )
        )
        self.vminmaxLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.stdcsvplotchoiceComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_5.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "standard plot", None)
        )
        self.colormapLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )
        self.colormapLineEdit.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "jet", None)
        )
        self.label_10.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "colormap", None)
        )
        self.label_13.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Choose analysis scope:", None
            )
        )
        self.label_7.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Primary data type (run_use)", None
            )
        )
        self.ExpRunUseComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                'This "use" is specified in the EXP \n'
                "and determines what types of analysis \n"
                "can be performed",
                None,
            )
        )
        self.label_14.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Choose RUNs to include:", None
            )
        )
        self.UserFOMLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "enter comma-delimited list of string or\n"
                'number FOMS that will become a constant column in the .csv generated by "Analyze Data".\n'
                "After entry complete, you will be prompted for fom names",
                None,
            )
        )
        self.label_21.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "User-defined FOMs", None
            )
        )
        self.FOMProcessNamesComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog",
                "The name of the functions that will be applied to data\n"
                "to generate Intermediate and FOM results",
                None,
            )
        )
        self.label_22.setText(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Choose FOM post-process function:", None
            )
        )
        self.autoplotCheckBox.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Auto plot ana__x", None)
        )
        self.RaiseErrorPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "err", None)
        )
        self.OpenInfoPushButton.setText(
            QtCore.QCoreApplication.translate("CalcFOMDialog", "Open via Search", None)
        )
        self.expfilenameLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CalcFOMDialog", "Comment string to be included in EXP", None
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    CalcFOMDialog = QtWidgets.QDialog()
    ui = Ui_CalcFOMDialog()
    ui.setupUi(CalcFOMDialog)
    CalcFOMDialog.show()
    sys.exit(app.exec_())
