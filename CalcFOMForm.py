# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\CalcFOMForm.ui'
#
# Created: Sat Feb 13 11:37:35 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CalcFOMDialog(object):
    def setupUi(self, CalcFOMDialog):
        CalcFOMDialog.setObjectName(_fromUtf8("CalcFOMDialog"))
        CalcFOMDialog.resize(1142, 882)
        self.BatchComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.BatchComboBox.setGeometry(QtCore.QRect(10, 70, 271, 22))
        self.BatchComboBox.setObjectName(_fromUtf8("BatchComboBox"))
        self.BatchPushButton = QtGui.QPushButton(CalcFOMDialog)
        self.BatchPushButton.setGeometry(QtCore.QRect(10, 50, 131, 21))
        self.BatchPushButton.setObjectName(_fromUtf8("BatchPushButton"))
        self.gridLayoutWidget_3 = QtGui.QWidget(CalcFOMDialog)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 360, 261, 163))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 2)
        self.label_17 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_2.addWidget(self.label_17, 1, 0, 1, 1)
        self.label_18 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 2, 0, 1, 1)
        self.label_19 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 3, 0, 1, 1)
        self.UserNameLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.UserNameLineEdit.setObjectName(_fromUtf8("UserNameLineEdit"))
        self.gridLayout_2.addWidget(self.UserNameLineEdit, 2, 1, 1, 1)
        self.AnaTypeLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.AnaTypeLineEdit.setObjectName(_fromUtf8("AnaTypeLineEdit"))
        self.gridLayout_2.addWidget(self.AnaTypeLineEdit, 0, 1, 1, 1)
        self.AnaNameLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.AnaNameLineEdit.setEnabled(False)
        self.AnaNameLineEdit.setObjectName(_fromUtf8("AnaNameLineEdit"))
        self.gridLayout_2.addWidget(self.AnaNameLineEdit, 1, 1, 1, 1)
        self.AccessLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.AccessLineEdit.setObjectName(_fromUtf8("AccessLineEdit"))
        self.gridLayout_2.addWidget(self.AccessLineEdit, 3, 1, 1, 1)
        self.label_16 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 0, 0, 1, 1)
        self.AnaDescLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.AnaDescLineEdit.setObjectName(_fromUtf8("AnaDescLineEdit"))
        self.gridLayout_2.addWidget(self.AnaDescLineEdit, 5, 0, 1, 2)
        self.layoutWidget = QtGui.QWidget(CalcFOMDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(290, 10, 212, 141))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.AnalysisGridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.AnalysisGridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.AnalysisGridLayout.setMargin(0)
        self.AnalysisGridLayout.setObjectName(_fromUtf8("AnalysisGridLayout"))
        self.AnalyzeDataPushButton = QtGui.QPushButton(self.layoutWidget)
        self.AnalyzeDataPushButton.setObjectName(_fromUtf8("AnalyzeDataPushButton"))
        self.AnalysisGridLayout.addWidget(self.AnalyzeDataPushButton, 0, 1, 1, 1)
        self.EditDfltVisPushButton = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EditDfltVisPushButton.sizePolicy().hasHeightForWidth())
        self.EditDfltVisPushButton.setSizePolicy(sizePolicy)
        self.EditDfltVisPushButton.setObjectName(_fromUtf8("EditDfltVisPushButton"))
        self.AnalysisGridLayout.addWidget(self.EditDfltVisPushButton, 1, 1, 1, 1)
        self.ClearAnalysisPushButton = QtGui.QPushButton(self.layoutWidget)
        self.ClearAnalysisPushButton.setObjectName(_fromUtf8("ClearAnalysisPushButton"))
        self.AnalysisGridLayout.addWidget(self.ClearAnalysisPushButton, 2, 1, 1, 1)
        self.EditAnalysisParamsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.EditAnalysisParamsPushButton.setObjectName(_fromUtf8("EditAnalysisParamsPushButton"))
        self.AnalysisGridLayout.addWidget(self.EditAnalysisParamsPushButton, 0, 0, 1, 1)
        self.SaveAnaPushButton = QtGui.QPushButton(self.layoutWidget)
        self.SaveAnaPushButton.setObjectName(_fromUtf8("SaveAnaPushButton"))
        self.AnalysisGridLayout.addWidget(self.SaveAnaPushButton, 2, 0, 1, 1)
        self.ImportAnalysisParamsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.ImportAnalysisParamsPushButton.setObjectName(_fromUtf8("ImportAnalysisParamsPushButton"))
        self.AnalysisGridLayout.addWidget(self.ImportAnalysisParamsPushButton, 1, 0, 1, 1)
        self.ViewResultPushButton = QtGui.QPushButton(self.layoutWidget)
        self.ViewResultPushButton.setObjectName(_fromUtf8("ViewResultPushButton"))
        self.AnalysisGridLayout.addWidget(self.ViewResultPushButton, 3, 0, 1, 1)
        self.ClearSingleAnalysisPushButton = QtGui.QPushButton(self.layoutWidget)
        self.ClearSingleAnalysisPushButton.setObjectName(_fromUtf8("ClearSingleAnalysisPushButton"))
        self.AnalysisGridLayout.addWidget(self.ClearSingleAnalysisPushButton, 3, 1, 1, 1)
        self.SaveViewPushButton = QtGui.QPushButton(self.layoutWidget)
        self.SaveViewPushButton.setObjectName(_fromUtf8("SaveViewPushButton"))
        self.AnalysisGridLayout.addWidget(self.SaveViewPushButton, 4, 0, 1, 1)
        self.UpdatePlotPushButton = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UpdatePlotPushButton.sizePolicy().hasHeightForWidth())
        self.UpdatePlotPushButton.setSizePolicy(sizePolicy)
        self.UpdatePlotPushButton.setObjectName(_fromUtf8("UpdatePlotPushButton"))
        self.AnalysisGridLayout.addWidget(self.UpdatePlotPushButton, 4, 1, 1, 1)
        self.ImportExpPushButton = QtGui.QPushButton(CalcFOMDialog)
        self.ImportExpPushButton.setGeometry(QtCore.QRect(80, 10, 81, 21))
        self.ImportExpPushButton.setObjectName(_fromUtf8("ImportExpPushButton"))
        self.ImportAnaPushButton = QtGui.QPushButton(CalcFOMDialog)
        self.ImportAnaPushButton.setGeometry(QtCore.QRect(0, 10, 71, 21))
        self.ImportAnaPushButton.setObjectName(_fromUtf8("ImportAnaPushButton"))
        self.textBrowser_plate = QtGui.QTextBrowser(CalcFOMDialog)
        self.textBrowser_plate.setGeometry(QtCore.QRect(570, 530, 561, 341))
        self.textBrowser_plate.setObjectName(_fromUtf8("textBrowser_plate"))
        self.textBrowser_h = QtGui.QTextBrowser(CalcFOMDialog)
        self.textBrowser_h.setGeometry(QtCore.QRect(760, 10, 371, 241))
        self.textBrowser_h.setObjectName(_fromUtf8("textBrowser_h"))
        self.textBrowser_comp = QtGui.QTextBrowser(CalcFOMDialog)
        self.textBrowser_comp.setGeometry(QtCore.QRect(510, 250, 621, 281))
        self.textBrowser_comp.setObjectName(_fromUtf8("textBrowser_comp"))
        self.line = QtGui.QFrame(CalcFOMDialog)
        self.line.setGeometry(QtCore.QRect(276, 10, 20, 511))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(CalcFOMDialog)
        self.line_2.setGeometry(QtCore.QRect(500, 0, 20, 521))
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(CalcFOMDialog)
        self.line_3.setGeometry(QtCore.QRect(0, 350, 281, 20))
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.line_4 = QtGui.QFrame(CalcFOMDialog)
        self.line_4.setGeometry(QtCore.QRect(0, 89, 281, 21))
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.AnalysisNamesComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.AnalysisNamesComboBox.setGeometry(QtCore.QRect(290, 410, 211, 22))
        self.AnalysisNamesComboBox.setObjectName(_fromUtf8("AnalysisNamesComboBox"))
        self.label_20 = QtGui.QLabel(CalcFOMDialog)
        self.label_20.setGeometry(QtCore.QRect(290, 390, 219, 21))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.AnaTreeWidget = QtGui.QTreeWidget(CalcFOMDialog)
        self.AnaTreeWidget.setGeometry(QtCore.QRect(10, 530, 551, 341))
        self.AnaTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AnaTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.AnaTreeWidget.setHeaderHidden(True)
        self.AnaTreeWidget.setExpandsOnDoubleClick(False)
        self.AnaTreeWidget.setObjectName(_fromUtf8("AnaTreeWidget"))
        self.AnaTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.AnaTreeWidget.header().setVisible(False)
        self.AnaTreeWidget.header().setCascadingSectionResizes(False)
        self.AnaTreeWidget.header().setStretchLastSection(True)
        self.getplatemapCheckBox = QtGui.QCheckBox(CalcFOMDialog)
        self.getplatemapCheckBox.setGeometry(QtCore.QRect(170, 10, 111, 21))
        self.getplatemapCheckBox.setChecked(True)
        self.getplatemapCheckBox.setObjectName(_fromUtf8("getplatemapCheckBox"))
        self.CompPlotOrderComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.CompPlotOrderComboBox.setGeometry(QtCore.QRect(520, 220, 111, 22))
        self.CompPlotOrderComboBox.setObjectName(_fromUtf8("CompPlotOrderComboBox"))
        self.label_2 = QtGui.QLabel(CalcFOMDialog)
        self.label_2.setGeometry(QtCore.QRect(520, 200, 111, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(CalcFOMDialog)
        self.label.setGeometry(QtCore.QRect(520, 90, 111, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.CompPlotTypeComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.CompPlotTypeComboBox.setGeometry(QtCore.QRect(520, 110, 111, 31))
        self.CompPlotTypeComboBox.setObjectName(_fromUtf8("CompPlotTypeComboBox"))
        self.label_4 = QtGui.QLabel(CalcFOMDialog)
        self.label_4.setGeometry(QtCore.QRect(520, 150, 111, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.compplotsizeLineEdit = QtGui.QLineEdit(CalcFOMDialog)
        self.compplotsizeLineEdit.setGeometry(QtCore.QRect(520, 170, 111, 22))
        self.compplotsizeLineEdit.setObjectName(_fromUtf8("compplotsizeLineEdit"))
        self.label_3 = QtGui.QLabel(CalcFOMDialog)
        self.label_3.setGeometry(QtCore.QRect(520, 40, 119, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.fomplotchoiceComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.fomplotchoiceComboBox.setGeometry(QtCore.QRect(520, 60, 111, 22))
        self.fomplotchoiceComboBox.setObjectName(_fromUtf8("fomplotchoiceComboBox"))
        self.usedaqtimeCheckBox = QtGui.QCheckBox(CalcFOMDialog)
        self.usedaqtimeCheckBox.setGeometry(QtCore.QRect(640, 50, 119, 20))
        self.usedaqtimeCheckBox.setObjectName(_fromUtf8("usedaqtimeCheckBox"))
        self.label_9 = QtGui.QLabel(CalcFOMDialog)
        self.label_9.setGeometry(QtCore.QRect(640, 80, 119, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.aboverangecolLineEdit = QtGui.QLineEdit(CalcFOMDialog)
        self.aboverangecolLineEdit.setGeometry(QtCore.QRect(640, 100, 119, 22))
        self.aboverangecolLineEdit.setObjectName(_fromUtf8("aboverangecolLineEdit"))
        self.label_6 = QtGui.QLabel(CalcFOMDialog)
        self.label_6.setGeometry(QtCore.QRect(640, 120, 119, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.belowrangecolLineEdit = QtGui.QLineEdit(CalcFOMDialog)
        self.belowrangecolLineEdit.setGeometry(QtCore.QRect(640, 140, 119, 22))
        self.belowrangecolLineEdit.setObjectName(_fromUtf8("belowrangecolLineEdit"))
        self.label_8 = QtGui.QLabel(CalcFOMDialog)
        self.label_8.setGeometry(QtCore.QRect(640, 160, 119, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.vminmaxLineEdit = QtGui.QLineEdit(CalcFOMDialog)
        self.vminmaxLineEdit.setGeometry(QtCore.QRect(640, 180, 119, 22))
        self.vminmaxLineEdit.setObjectName(_fromUtf8("vminmaxLineEdit"))
        self.stdcsvplotchoiceComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.stdcsvplotchoiceComboBox.setGeometry(QtCore.QRect(520, 20, 111, 22))
        self.stdcsvplotchoiceComboBox.setObjectName(_fromUtf8("stdcsvplotchoiceComboBox"))
        self.label_5 = QtGui.QLabel(CalcFOMDialog)
        self.label_5.setGeometry(QtCore.QRect(520, 0, 119, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.colormapLineEdit = QtGui.QLineEdit(CalcFOMDialog)
        self.colormapLineEdit.setGeometry(QtCore.QRect(640, 220, 119, 22))
        self.colormapLineEdit.setObjectName(_fromUtf8("colormapLineEdit"))
        self.label_10 = QtGui.QLabel(CalcFOMDialog)
        self.label_10.setGeometry(QtCore.QRect(640, 200, 119, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_13 = QtGui.QLabel(CalcFOMDialog)
        self.label_13.setGeometry(QtCore.QRect(290, 150, 219, 21))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.TechTypeRadioButton_0 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_0.setGeometry(QtCore.QRect(290, 170, 219, 16))
        self.TechTypeRadioButton_0.setText(_fromUtf8(""))
        self.TechTypeRadioButton_0.setObjectName(_fromUtf8("TechTypeRadioButton_0"))
        self.TechTypeButtonGroup = QtGui.QButtonGroup(CalcFOMDialog)
        self.TechTypeButtonGroup.setObjectName(_fromUtf8("TechTypeButtonGroup"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_0)
        self.TechTypeRadioButton_1 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_1.setGeometry(QtCore.QRect(290, 190, 219, 16))
        self.TechTypeRadioButton_1.setText(_fromUtf8(""))
        self.TechTypeRadioButton_1.setObjectName(_fromUtf8("TechTypeRadioButton_1"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_1)
        self.TechTypeRadioButton_2 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_2.setGeometry(QtCore.QRect(290, 210, 219, 16))
        self.TechTypeRadioButton_2.setText(_fromUtf8(""))
        self.TechTypeRadioButton_2.setObjectName(_fromUtf8("TechTypeRadioButton_2"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_2)
        self.TechTypeRadioButton_3 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_3.setGeometry(QtCore.QRect(290, 230, 219, 16))
        self.TechTypeRadioButton_3.setText(_fromUtf8(""))
        self.TechTypeRadioButton_3.setObjectName(_fromUtf8("TechTypeRadioButton_3"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_3)
        self.TechTypeRadioButton_4 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_4.setGeometry(QtCore.QRect(290, 250, 219, 16))
        self.TechTypeRadioButton_4.setText(_fromUtf8(""))
        self.TechTypeRadioButton_4.setObjectName(_fromUtf8("TechTypeRadioButton_4"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_4)
        self.TechTypeRadioButton_5 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_5.setGeometry(QtCore.QRect(290, 270, 219, 16))
        self.TechTypeRadioButton_5.setText(_fromUtf8(""))
        self.TechTypeRadioButton_5.setObjectName(_fromUtf8("TechTypeRadioButton_5"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_5)
        self.TechTypeRadioButton_6 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_6.setGeometry(QtCore.QRect(290, 290, 219, 16))
        self.TechTypeRadioButton_6.setText(_fromUtf8(""))
        self.TechTypeRadioButton_6.setObjectName(_fromUtf8("TechTypeRadioButton_6"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_6)
        self.TechTypeRadioButton_7 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_7.setGeometry(QtCore.QRect(290, 310, 219, 16))
        self.TechTypeRadioButton_7.setText(_fromUtf8(""))
        self.TechTypeRadioButton_7.setObjectName(_fromUtf8("TechTypeRadioButton_7"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_7)
        self.TechTypeRadioButton_8 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_8.setGeometry(QtCore.QRect(290, 330, 219, 16))
        self.TechTypeRadioButton_8.setText(_fromUtf8(""))
        self.TechTypeRadioButton_8.setObjectName(_fromUtf8("TechTypeRadioButton_8"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_8)
        self.TechTypeRadioButton_9 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_9.setGeometry(QtCore.QRect(290, 350, 219, 16))
        self.TechTypeRadioButton_9.setText(_fromUtf8(""))
        self.TechTypeRadioButton_9.setObjectName(_fromUtf8("TechTypeRadioButton_9"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_9)
        self.TechTypeRadioButton_10 = QtGui.QRadioButton(CalcFOMDialog)
        self.TechTypeRadioButton_10.setGeometry(QtCore.QRect(290, 370, 219, 16))
        self.TechTypeRadioButton_10.setText(_fromUtf8(""))
        self.TechTypeRadioButton_10.setObjectName(_fromUtf8("TechTypeRadioButton_10"))
        self.TechTypeButtonGroup.addButton(self.TechTypeRadioButton_10)
        self.label_7 = QtGui.QLabel(CalcFOMDialog)
        self.label_7.setGeometry(QtCore.QRect(10, 100, 267, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.ExpRunUseComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.ExpRunUseComboBox.setGeometry(QtCore.QRect(0, 120, 267, 20))
        self.ExpRunUseComboBox.setObjectName(_fromUtf8("ExpRunUseComboBox"))
        self.label_14 = QtGui.QLabel(CalcFOMDialog)
        self.label_14.setGeometry(QtCore.QRect(10, 150, 265, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.RunSelectTreeWidget = QtGui.QTreeWidget(CalcFOMDialog)
        self.RunSelectTreeWidget.setGeometry(QtCore.QRect(10, 170, 271, 181))
        self.RunSelectTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RunSelectTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.RunSelectTreeWidget.setHeaderHidden(True)
        self.RunSelectTreeWidget.setExpandsOnDoubleClick(False)
        self.RunSelectTreeWidget.setObjectName(_fromUtf8("RunSelectTreeWidget"))
        self.RunSelectTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.RunSelectTreeWidget.header().setVisible(False)
        self.RunSelectTreeWidget.header().setCascadingSectionResizes(False)
        self.RunSelectTreeWidget.header().setStretchLastSection(True)
        self.UserFOMLineEdit = QtGui.QLineEdit(CalcFOMDialog)
        self.UserFOMLineEdit.setGeometry(QtCore.QRect(290, 500, 211, 20))
        self.UserFOMLineEdit.setObjectName(_fromUtf8("UserFOMLineEdit"))
        self.line_5 = QtGui.QFrame(CalcFOMDialog)
        self.line_5.setGeometry(QtCore.QRect(0, 30, 281, 21))
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.label_21 = QtGui.QLabel(CalcFOMDialog)
        self.label_21.setGeometry(QtCore.QRect(290, 480, 219, 20))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.FOMProcessNamesComboBox = QtGui.QComboBox(CalcFOMDialog)
        self.FOMProcessNamesComboBox.setGeometry(QtCore.QRect(290, 450, 211, 22))
        self.FOMProcessNamesComboBox.setObjectName(_fromUtf8("FOMProcessNamesComboBox"))
        self.label_22 = QtGui.QLabel(CalcFOMDialog)
        self.label_22.setGeometry(QtCore.QRect(290, 430, 219, 21))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.autoplotCheckBox = QtGui.QCheckBox(CalcFOMDialog)
        self.autoplotCheckBox.setGeometry(QtCore.QRect(640, 20, 119, 20))
        self.autoplotCheckBox.setChecked(True)
        self.autoplotCheckBox.setObjectName(_fromUtf8("autoplotCheckBox"))

        self.retranslateUi(CalcFOMDialog)
        QtCore.QMetaObject.connectSlotsByName(CalcFOMDialog)

    def retranslateUi(self, CalcFOMDialog):
        CalcFOMDialog.setWindowTitle(QtGui.QApplication.translate("CalcFOMDialog", "Process Data, Calc FOM from EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.BatchComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.BatchPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Considering the files already in the EXP, keep the files that meet all criteria", None, QtGui.QApplication.UnicodeUTF8))
        self.BatchPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Run Batch Process:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("CalcFOMDialog", "Analysis description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("CalcFOMDialog", "Analysis name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("CalcFOMDialog", "created by:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("CalcFOMDialog", "access:", None, QtGui.QApplication.UnicodeUTF8))
        self.UserNameLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.UserNameLineEdit.setText(QtGui.QApplication.translate("CalcFOMDialog", "eche", None, QtGui.QApplication.UnicodeUTF8))
        self.AnaTypeLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.AnaTypeLineEdit.setText(QtGui.QApplication.translate("CalcFOMDialog", "eche", None, QtGui.QApplication.UnicodeUTF8))
        self.AnaNameLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.AnaNameLineEdit.setText(QtGui.QApplication.translate("CalcFOMDialog", "eche", None, QtGui.QApplication.UnicodeUTF8))
        self.AccessLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.AccessLineEdit.setText(QtGui.QApplication.translate("CalcFOMDialog", "hte", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("CalcFOMDialog", "Analysis type:", None, QtGui.QApplication.UnicodeUTF8))
        self.AnaDescLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP.\n"
"If you modify the beginning with a\"<comment>;\" the \n"
"comment will remain as you change analysis options", None, QtGui.QApplication.UnicodeUTF8))
        self.AnalyzeDataPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Perform the selected analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.AnalyzeDataPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Analyze Data", None, QtGui.QApplication.UnicodeUTF8))
        self.EditDfltVisPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Edit the FOM visualization parameters in the .csv\n"
"ONLY WORKS ON MOST RECENT \"Analyze Data\"", None, QtGui.QApplication.UnicodeUTF8))
        self.EditDfltVisPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Update Dflt Vis", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearAnalysisPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Clear the analysis, removing intermediate data and FOMs", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearAnalysisPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Clear Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAnalysisParamsPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Edit parameters involved inthe analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAnalysisParamsPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Edit Params", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveAnaPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Save .fom, FOR THE SELECTED ANALYSIS TYPE ONLY.\n"
" Intermediate data will also be saved", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveAnaPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Save ANA", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportAnalysisParamsPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Import a .par file", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportAnalysisParamsPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Import Params", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewResultPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Send Raw, Intermediate and FOM data to the Visualize window", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewResultPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "View Result", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearSingleAnalysisPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Clear the analysis, removing intermediate data and FOMs", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearSingleAnalysisPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Del 1 ana__x", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveViewPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Send Raw, Intermediate and FOM data to the Visualize window", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveViewPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Save+View", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdatePlotPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Edit the FOM visualization parameters in the .csv\n"
"ONLY WORKS ON MOST RECENT \"Analyze Data\"", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdatePlotPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Update Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportExpPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Import a .exp file, which will provide options for the data type, RUNs and analysis type", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportExpPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Import EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportAnaPushButton.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Grab the EXP from the \"Create EXP\" window", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportAnaPushButton.setText(QtGui.QApplication.translate("CalcFOMDialog", "Open ANA", None, QtGui.QApplication.UnicodeUTF8))
        self.AnalysisNamesComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "The name of the functions that will be applied to data\n"
"to generate Intermediate and FOM results", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("CalcFOMDialog", "Choose analysis function:", None, QtGui.QApplication.UnicodeUTF8))
        self.getplatemapCheckBox.setText(QtGui.QApplication.translate("CalcFOMDialog", "Get platemaps", None, QtGui.QApplication.UnicodeUTF8))
        self.CompPlotOrderComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CalcFOMDialog", "Element plot order:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CalcFOMDialog", "Comp. plot type:", None, QtGui.QApplication.UnicodeUTF8))
        self.CompPlotTypeComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("CalcFOMDialog", "Comp. point size:", None, QtGui.QApplication.UnicodeUTF8))
        self.compplotsizeLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.compplotsizeLineEdit.setText(QtGui.QApplication.translate("CalcFOMDialog", "patch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CalcFOMDialog", "fom to plot", None, QtGui.QApplication.UnicodeUTF8))
        self.fomplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.usedaqtimeCheckBox.setText(QtGui.QApplication.translate("CalcFOMDialog", "Use DAQ time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("CalcFOMDialog", "above color", None, QtGui.QApplication.UnicodeUTF8))
        self.aboverangecolLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("CalcFOMDialog", "below color", None, QtGui.QApplication.UnicodeUTF8))
        self.belowrangecolLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("CalcFOMDialog", "fom range min,max", None, QtGui.QApplication.UnicodeUTF8))
        self.vminmaxLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.stdcsvplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("CalcFOMDialog", "standard plot", None, QtGui.QApplication.UnicodeUTF8))
        self.colormapLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.colormapLineEdit.setText(QtGui.QApplication.translate("CalcFOMDialog", "jet", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("CalcFOMDialog", "colormap", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("CalcFOMDialog", "Choose analysis scope:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("CalcFOMDialog", "Primary data type (run_use)", None, QtGui.QApplication.UnicodeUTF8))
        self.ExpRunUseComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "This \"use\" is specified in the EXP \n"
"and determines what types of analysis \n"
"can be performed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("CalcFOMDialog", "Choose RUNs to include:", None, QtGui.QApplication.UnicodeUTF8))
        self.UserFOMLineEdit.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "enter comma-delimited list of string or\n"
"number FOMS that will become a constant column in the .csv generated by \"Analyze Data\".\n"
"After entry complete, you will be prompted for fom names", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("CalcFOMDialog", "User-defined FOMs", None, QtGui.QApplication.UnicodeUTF8))
        self.FOMProcessNamesComboBox.setToolTip(QtGui.QApplication.translate("CalcFOMDialog", "The name of the functions that will be applied to data\n"
"to generate Intermediate and FOM results", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("CalcFOMDialog", "Choose FOM post-process function:", None, QtGui.QApplication.UnicodeUTF8))
        self.autoplotCheckBox.setText(QtGui.QApplication.translate("CalcFOMDialog", "Auto plot ana__x", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CalcFOMDialog = QtGui.QDialog()
    ui = Ui_CalcFOMDialog()
    ui.setupUi(CalcFOMDialog)
    CalcFOMDialog.show()
    sys.exit(app.exec_())

