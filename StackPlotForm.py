# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\StackPlotForm.ui'
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


class Ui_StackPlotDialog(object):
    def setupUi(self, StackPlotDialog):
        StackPlotDialog.setObjectName("StackPlotDialog")
        StackPlotDialog.resize(879, 758)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StackPlotDialog.sizePolicy().hasHeightForWidth())
        StackPlotDialog.setSizePolicy(sizePolicy)
        self.AnaExpFomTreeWidget = QtWidgets.QTreeWidget(StackPlotDialog)
        self.AnaExpFomTreeWidget.setGeometry(QtCore.QRect(120, 40, 351, 201))
        self.AnaExpFomTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AnaExpFomTreeWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded
        )
        self.AnaExpFomTreeWidget.setHeaderHidden(True)
        self.AnaExpFomTreeWidget.setExpandsOnDoubleClick(False)
        self.AnaExpFomTreeWidget.setObjectName("AnaExpFomTreeWidget")
        self.AnaExpFomTreeWidget.headerItem().setText(0, "1")
        self.AnaExpFomTreeWidget.header().setVisible(False)
        self.AnaExpFomTreeWidget.header().setCascadingSectionResizes(False)
        self.AnaExpFomTreeWidget.header().setStretchLastSection(True)
        self.textBrowser_xy = QtWidgets.QTextBrowser(StackPlotDialog)
        self.textBrowser_xy.setGeometry(QtCore.QRect(0, 369, 871, 381))
        self.textBrowser_xy.setObjectName("textBrowser_xy")
        self.AnaPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.AnaPushButton.setGeometry(QtCore.QRect(10, 0, 91, 23))
        self.AnaPushButton.setObjectName("AnaPushButton")
        self.label_12 = QtWidgets.QLabel(StackPlotDialog)
        self.label_12.setGeometry(QtCore.QRect(470, 250, 71, 51))
        self.label_12.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_12.setObjectName("label_12")
        self.rightyplotchoiceComboBox = QtWidgets.QComboBox(StackPlotDialog)
        self.rightyplotchoiceComboBox.setGeometry(QtCore.QRect(200, 339, 111, 22))
        self.rightyplotchoiceComboBox.setObjectName("rightyplotchoiceComboBox")
        self.label_13 = QtWidgets.QLabel(StackPlotDialog)
        self.label_13.setGeometry(QtCore.QRect(200, 319, 111, 21))
        self.label_13.setObjectName("label_13")
        self.yplotchoiceComboBox = QtWidgets.QComboBox(StackPlotDialog)
        self.yplotchoiceComboBox.setGeometry(QtCore.QRect(80, 339, 111, 22))
        self.yplotchoiceComboBox.setObjectName("yplotchoiceComboBox")
        self.label_14 = QtWidgets.QLabel(StackPlotDialog)
        self.label_14.setGeometry(QtCore.QRect(80, 319, 111, 21))
        self.label_14.setObjectName("label_14")
        self.xplotchoiceComboBox = QtWidgets.QComboBox(StackPlotDialog)
        self.xplotchoiceComboBox.setGeometry(QtCore.QRect(80, 299, 111, 22))
        self.xplotchoiceComboBox.setObjectName("xplotchoiceComboBox")
        self.label_15 = QtWidgets.QLabel(StackPlotDialog)
        self.label_15.setGeometry(QtCore.QRect(80, 279, 111, 21))
        self.label_15.setObjectName("label_15")
        self.overlayselectCheckBox = QtWidgets.QCheckBox(StackPlotDialog)
        self.overlayselectCheckBox.setGeometry(QtCore.QRect(210, 289, 81, 17))
        self.overlayselectCheckBox.setChecked(True)
        self.overlayselectCheckBox.setObjectName("overlayselectCheckBox")
        self.SelectTreeWidget = QtWidgets.QTreeWidget(StackPlotDialog)
        self.SelectTreeWidget.setGeometry(QtCore.QRect(490, 40, 381, 201))
        self.SelectTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SelectTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.SelectTreeWidget.setHeaderHidden(True)
        self.SelectTreeWidget.setExpandsOnDoubleClick(False)
        self.SelectTreeWidget.setObjectName("SelectTreeWidget")
        self.SelectTreeWidget.headerItem().setText(0, "1")
        self.SelectTreeWidget.header().setVisible(False)
        self.SelectTreeWidget.header().setCascadingSectionResizes(False)
        self.SelectTreeWidget.header().setStretchLastSection(True)
        self.UpdateFiltersPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.UpdateFiltersPushButton.setGeometry(QtCore.QRect(360, 260, 101, 31))
        self.UpdateFiltersPushButton.setObjectName("UpdateFiltersPushButton")
        self.UpdatePlotPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.UpdatePlotPushButton.setGeometry(QtCore.QRect(360, 290, 101, 23))
        self.UpdatePlotPushButton.setObjectName("UpdatePlotPushButton")
        self.line_3 = QtWidgets.QFrame(StackPlotDialog)
        self.line_3.setGeometry(QtCore.QRect(300, 279, 20, 81))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.customxystylePushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.customxystylePushButton.setGeometry(QtCore.QRect(10, 289, 61, 31))
        self.customxystylePushButton.setObjectName("customxystylePushButton")
        self.line = QtWidgets.QFrame(StackPlotDialog)
        self.line.setGeometry(QtCore.QRect(10, 270, 291, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.SaveFigsPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.SaveFigsPushButton.setGeometry(QtCore.QRect(10, 100, 101, 23))
        self.SaveFigsPushButton.setObjectName("SaveFigsPushButton")
        self.LoadCsvPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.LoadCsvPushButton.setGeometry(QtCore.QRect(10, 70, 101, 21))
        self.LoadCsvPushButton.setObjectName("LoadCsvPushButton")
        self.expanafilenameLineEdit = QtWidgets.QLineEdit(StackPlotDialog)
        self.expanafilenameLineEdit.setGeometry(QtCore.QRect(100, 0, 251, 21))
        self.expanafilenameLineEdit.setText("")
        self.expanafilenameLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.expanafilenameLineEdit.setObjectName("expanafilenameLineEdit")
        self.ClearPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.ClearPushButton.setGeometry(QtCore.QRect(10, 140, 91, 21))
        self.ClearPushButton.setObjectName("ClearPushButton")
        self.RaiseErrorPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(760, 0, 31, 23))
        self.RaiseErrorPushButton.setObjectName("RaiseErrorPushButton")
        self.StackClassComboBox = QtWidgets.QComboBox(StackPlotDialog)
        self.StackClassComboBox.setGeometry(QtCore.QRect(680, 270, 201, 22))
        self.StackClassComboBox.setObjectName("StackClassComboBox")
        self.OpenInfoPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.OpenInfoPushButton.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.OpenInfoPushButton.setObjectName("OpenInfoPushButton")
        self.EditParamsPushButton = QtWidgets.QPushButton(StackPlotDialog)
        self.EditParamsPushButton.setGeometry(QtCore.QRect(680, 300, 91, 21))
        self.EditParamsPushButton.setObjectName("EditParamsPushButton")
        self.StackColorsTextEdit = QtWidgets.QPlainTextEdit(StackPlotDialog)
        self.StackColorsTextEdit.setGeometry(QtCore.QRect(550, 250, 121, 111))
        self.StackColorsTextEdit.setObjectName("StackColorsTextEdit")
        self.StackXKeySearchLineEdit = QtWidgets.QLineEdit(StackPlotDialog)
        self.StackXKeySearchLineEdit.setGeometry(QtCore.QRect(570, 0, 161, 20))
        self.StackXKeySearchLineEdit.setObjectName("StackXKeySearchLineEdit")
        self.label = QtWidgets.QLabel(StackPlotDialog)
        self.label.setGeometry(QtCore.QRect(510, 2, 61, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(StackPlotDialog)
        self.label_2.setGeometry(QtCore.QRect(120, 21, 351, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(StackPlotDialog)
        self.label_3.setGeometry(QtCore.QRect(490, 20, 351, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(StackPlotDialog)
        self.label_4.setGeometry(QtCore.QRect(680, 250, 191, 20))
        self.label_4.setObjectName("label_4")
        self.retranslateUi(StackPlotDialog)
        QtCore.QMetaObject.connectSlotsByName(StackPlotDialog)

    def retranslateUi(self, StackPlotDialog):
        StackPlotDialog.setWindowTitle(_translate("StackPlotDialog", "Dialog", None))
        self.AnaPushButton.setText(_translate("StackPlotDialog", "Open ANA", None))
        self.label_12.setText(
            _translate(
                "StackPlotDialog",
                "stack colors:\n" "left to right\n" "on stack plot",
                None,
            )
        )
        self.rightyplotchoiceComboBox.setToolTip(
            _translate(
                "StackPlotDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_13.setText(_translate("StackPlotDialog", "right y-axis", None))
        self.yplotchoiceComboBox.setToolTip(
            _translate(
                "StackPlotDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_14.setText(_translate("StackPlotDialog", "y-axis", None))
        self.xplotchoiceComboBox.setToolTip(
            _translate(
                "StackPlotDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_15.setText(_translate("StackPlotDialog", "x-axis", None))
        self.overlayselectCheckBox.setText(
            _translate("StackPlotDialog", "x-y overlay", None)
        )
        self.UpdateFiltersPushButton.setText(
            _translate("StackPlotDialog", "plot Stack\n" "update filters", None)
        )
        self.UpdatePlotPushButton.setText(
            _translate("StackPlotDialog", "plot x-y line", None)
        )
        self.customxystylePushButton.setText(
            _translate("StackPlotDialog", "configure\n" "x-y style", None)
        )
        self.SaveFigsPushButton.setText(
            _translate("StackPlotDialog", "Save figs to ANA", None)
        )
        self.LoadCsvPushButton.setText(_translate("StackPlotDialog", "Load .csv", None))
        self.expanafilenameLineEdit.setToolTip(
            _translate("StackPlotDialog", "Comment string to be included in EXP", None)
        )
        self.ClearPushButton.setText(_translate("StackPlotDialog", "Clear Data", None))
        self.RaiseErrorPushButton.setText(_translate("StackPlotDialog", "err", None))
        self.StackClassComboBox.setToolTip(
            _translate(
                "StackPlotDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.OpenInfoPushButton.setText(
            _translate("StackPlotDialog", "Open via Search", None)
        )
        self.EditParamsPushButton.setText(
            _translate("StackPlotDialog", "Edit Params", None)
        )
        self.StackColorsTextEdit.setPlainText(
            _translate(
                "StackPlotDialog",
                "0.88,0.88,0.88\n"
                "1.00,0.90,0.60\n"
                "0.86,0.78,0.90\n"
                "0.94,0.67,0.67\n"
                "0.77,0.88,0 .71\n"
                "0.97,0.80,0.68\n"
                "0.71,0.82,0.90\n"
                "0.75,0.75,0.75",
                None,
            )
        )
        self.StackXKeySearchLineEdit.setText(
            _translate("StackPlotDialog", "norm_dist", None)
        )
        self.label.setText(_translate("StackPlotDialog", "stack x key:", None))
        self.label_2.setText(
            _translate(
                "StackPlotDialog", "checked CSVs are searched for x-y plots", None
            )
        )
        self.label_3.setText(
            _translate(
                "StackPlotDialog",
                "checked foms normalized for stack plot and x key must be in same csv:",
                None,
            )
        )
        self.label_4.setText(
            _translate("StackPlotDialog", "stack plot function:", None)
        )
