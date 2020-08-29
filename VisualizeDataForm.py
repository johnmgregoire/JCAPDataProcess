# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\PlotAnaForm.ui'
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


class Ui_VisDataDialog(object):
    def setupUi(self, VisDataDialog):
        VisDataDialog.setObjectName("VisDataDialog")
        VisDataDialog.resize(1597, 1026)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VisDataDialog.sizePolicy().hasHeightForWidth())
        VisDataDialog.setSizePolicy(sizePolicy)
        self.plateTabWidget = QtWidgets.QTabWidget(VisDataDialog)
        self.plateTabWidget.setGeometry(QtCore.QRect(700, 620, 891, 401))
        self.plateTabWidget.setObjectName("plateTabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser_plate = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_plate.setGeometry(QtCore.QRect(0, 30, 881, 371))
        self.textBrowser_plate.setObjectName("textBrowser_plate")
        self.plateTabWidget.addTab(self.tab, "")
        self.AnaExpFomTreeWidget = QtWidgets.QTreeWidget(VisDataDialog)
        self.AnaExpFomTreeWidget.setGeometry(QtCore.QRect(0, 740, 681, 271))
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
        self.textBrowser_xy = QtWidgets.QTextBrowser(VisDataDialog)
        self.textBrowser_xy.setGeometry(QtCore.QRect(0, 440, 681, 291))
        self.textBrowser_xy.setObjectName("textBrowser_xy")
        self.compTabWidget = QtWidgets.QTabWidget(VisDataDialog)
        self.compTabWidget.setGeometry(QtCore.QRect(700, 220, 891, 401))
        self.compTabWidget.setObjectName("compTabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textBrowser_comp = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_comp.setGeometry(QtCore.QRect(0, 30, 881, 371))
        self.textBrowser_comp.setObjectName("textBrowser_comp")
        self.compTabWidget.addTab(self.tab_2, "")
        self.browser = QtWidgets.QTextBrowser(VisDataDialog)
        self.browser.setGeometry(QtCore.QRect(940, 40, 651, 171))
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.browser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.browser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.browser.setObjectName("browser")
        self.FolderPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.FolderPushButton.setGeometry(QtCore.QRect(10, 88, 101, 23))
        self.FolderPushButton.setObjectName("FolderPushButton")
        self.AnaPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.AnaPushButton.setGeometry(QtCore.QRect(10, 0, 91, 23))
        self.AnaPushButton.setObjectName("AnaPushButton")
        self.ExpPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.ExpPushButton.setGeometry(QtCore.QRect(10, 20, 91, 23))
        self.ExpPushButton.setObjectName("ExpPushButton")
        self.UpdateFolderPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.UpdateFolderPushButton.setGeometry(QtCore.QRect(10, 108, 101, 21))
        self.UpdateFolderPushButton.setObjectName("UpdateFolderPushButton")
        self.OnFlyAnaClassComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.OnFlyAnaClassComboBox.setGeometry(QtCore.QRect(0, 300, 111, 22))
        self.OnFlyAnaClassComboBox.setObjectName("OnFlyAnaClassComboBox")
        self.OnFlyStoreInterCheckBox = QtWidgets.QCheckBox(VisDataDialog)
        self.OnFlyStoreInterCheckBox.setGeometry(QtCore.QRect(0, 320, 81, 31))
        self.OnFlyStoreInterCheckBox.setObjectName("OnFlyStoreInterCheckBox")
        self.compLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.compLineEdit.setGeometry(QtCore.QRect(970, 10, 111, 20))
        self.compLineEdit.setToolTip("")
        self.compLineEdit.setText("")
        self.compLineEdit.setObjectName("compLineEdit")
        self.label = QtWidgets.QLabel(VisDataDialog)
        self.label.setGeometry(QtCore.QRect(930, 0, 46, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(VisDataDialog)
        self.label_2.setGeometry(QtCore.QRect(1130, 0, 46, 31))
        self.label_2.setObjectName("label_2")
        self.xyLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.xyLineEdit.setGeometry(QtCore.QRect(1160, 10, 81, 20))
        self.xyLineEdit.setToolTip("")
        self.xyLineEdit.setObjectName("xyLineEdit")
        self.label_3 = QtWidgets.QLabel(VisDataDialog)
        self.label_3.setGeometry(QtCore.QRect(1300, 0, 46, 31))
        self.label_3.setObjectName("label_3")
        self.sampleLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.sampleLineEdit.setGeometry(QtCore.QRect(1340, 10, 111, 20))
        self.sampleLineEdit.setToolTip("")
        self.sampleLineEdit.setObjectName("sampleLineEdit")
        self.addComp = QtWidgets.QPushButton(VisDataDialog)
        self.addComp.setGeometry(QtCore.QRect(1080, 10, 21, 23))
        self.addComp.setObjectName("addComp")
        self.remComp = QtWidgets.QPushButton(VisDataDialog)
        self.remComp.setGeometry(QtCore.QRect(1100, 10, 21, 23))
        self.remComp.setObjectName("remComp")
        self.remxy = QtWidgets.QPushButton(VisDataDialog)
        self.remxy.setGeometry(QtCore.QRect(1270, 10, 21, 23))
        self.remxy.setObjectName("remxy")
        self.addxy = QtWidgets.QPushButton(VisDataDialog)
        self.addxy.setGeometry(QtCore.QRect(1250, 10, 21, 23))
        self.addxy.setObjectName("addxy")
        self.remSample = QtWidgets.QPushButton(VisDataDialog)
        self.remSample.setGeometry(QtCore.QRect(1470, 10, 21, 23))
        self.remSample.setObjectName("remSample")
        self.addSample = QtWidgets.QPushButton(VisDataDialog)
        self.addSample.setGeometry(QtCore.QRect(1450, 10, 21, 23))
        self.addSample.setObjectName("addSample")
        self.label_4 = QtWidgets.QLabel(VisDataDialog)
        self.label_4.setGeometry(QtCore.QRect(700, 130, 91, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(VisDataDialog)
        self.label_5.setGeometry(QtCore.QRect(700, 40, 119, 21))
        self.label_5.setObjectName("label_5")
        self.fomplotchoiceComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.fomplotchoiceComboBox.setGeometry(QtCore.QRect(700, 60, 111, 21))
        self.fomplotchoiceComboBox.setWhatsThis("")
        self.fomplotchoiceComboBox.setObjectName("fomplotchoiceComboBox")
        self.label_6 = QtWidgets.QLabel(VisDataDialog)
        self.label_6.setGeometry(QtCore.QRect(700, 80, 111, 16))
        self.label_6.setObjectName("label_6")
        self.CompPlotTypeComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.CompPlotTypeComboBox.setGeometry(QtCore.QRect(700, 100, 111, 31))
        self.CompPlotTypeComboBox.setObjectName("CompPlotTypeComboBox")
        self.label_8 = QtWidgets.QLabel(VisDataDialog)
        self.label_8.setGeometry(QtCore.QRect(820, 90, 91, 21))
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(VisDataDialog)
        self.label_10.setGeometry(QtCore.QRect(850, 190, 31, 21))
        self.label_10.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_10.setObjectName("label_10")
        self.stdcsvplotchoiceComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.stdcsvplotchoiceComboBox.setGeometry(QtCore.QRect(700, 20, 211, 22))
        self.stdcsvplotchoiceComboBox.setObjectName("stdcsvplotchoiceComboBox")
        self.compplotsizeLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.compplotsizeLineEdit.setGeometry(QtCore.QRect(820, 70, 51, 22))
        self.compplotsizeLineEdit.setObjectName("compplotsizeLineEdit")
        self.belowrangecolLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.belowrangecolLineEdit.setGeometry(QtCore.QRect(810, 160, 61, 22))
        self.belowrangecolLineEdit.setObjectName("belowrangecolLineEdit")
        self.label_9 = QtWidgets.QLabel(VisDataDialog)
        self.label_9.setGeometry(QtCore.QRect(700, 0, 111, 21))
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(VisDataDialog)
        self.label_11.setGeometry(QtCore.QRect(820, 40, 51, 31))
        self.label_11.setObjectName("label_11")
        self.colormapLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.colormapLineEdit.setGeometry(QtCore.QRect(880, 190, 51, 21))
        self.colormapLineEdit.setObjectName("colormapLineEdit")
        self.vminmaxLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.vminmaxLineEdit.setGeometry(QtCore.QRect(820, 110, 91, 22))
        self.vminmaxLineEdit.setObjectName("vminmaxLineEdit")
        self.CompPlotOrderComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.CompPlotOrderComboBox.setGeometry(QtCore.QRect(700, 150, 91, 22))
        self.CompPlotOrderComboBox.setObjectName("CompPlotOrderComboBox")
        self.label_12 = QtWidgets.QLabel(VisDataDialog)
        self.label_12.setGeometry(QtCore.QRect(820, 130, 101, 31))
        self.label_12.setObjectName("label_12")
        self.aboverangecolLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.aboverangecolLineEdit.setGeometry(QtCore.QRect(870, 160, 61, 22))
        self.aboverangecolLineEdit.setObjectName("aboverangecolLineEdit")
        self.rightyplotchoiceComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.rightyplotchoiceComboBox.setGeometry(QtCore.QRect(200, 410, 111, 22))
        self.rightyplotchoiceComboBox.setObjectName("rightyplotchoiceComboBox")
        self.label_13 = QtWidgets.QLabel(VisDataDialog)
        self.label_13.setGeometry(QtCore.QRect(200, 390, 111, 21))
        self.label_13.setObjectName("label_13")
        self.yplotchoiceComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.yplotchoiceComboBox.setGeometry(QtCore.QRect(80, 410, 111, 22))
        self.yplotchoiceComboBox.setObjectName("yplotchoiceComboBox")
        self.label_14 = QtWidgets.QLabel(VisDataDialog)
        self.label_14.setGeometry(QtCore.QRect(80, 390, 111, 21))
        self.label_14.setObjectName("label_14")
        self.xplotchoiceComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.xplotchoiceComboBox.setGeometry(QtCore.QRect(80, 370, 111, 22))
        self.xplotchoiceComboBox.setObjectName("xplotchoiceComboBox")
        self.label_15 = QtWidgets.QLabel(VisDataDialog)
        self.label_15.setGeometry(QtCore.QRect(80, 351, 111, 20))
        self.label_15.setObjectName("label_15")
        self.customxylegendPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.customxylegendPushButton.setGeometry(QtCore.QRect(10, 400, 61, 31))
        self.customxylegendPushButton.setObjectName("customxylegendPushButton")
        self.overlayselectCheckBox = QtWidgets.QCheckBox(VisDataDialog)
        self.overlayselectCheckBox.setGeometry(QtCore.QRect(200, 350, 91, 21))
        self.overlayselectCheckBox.setObjectName("overlayselectCheckBox")
        self.SelectTreeWidget = QtWidgets.QTreeWidget(VisDataDialog)
        self.SelectTreeWidget.setGeometry(QtCore.QRect(370, 50, 311, 151))
        self.SelectTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SelectTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SelectTreeWidget.setHeaderHidden(True)
        self.SelectTreeWidget.setExpandsOnDoubleClick(False)
        self.SelectTreeWidget.setObjectName("SelectTreeWidget")
        self.SelectTreeWidget.headerItem().setText(0, "1")
        self.SelectTreeWidget.header().setVisible(False)
        self.SelectTreeWidget.header().setCascadingSectionResizes(False)
        self.SelectTreeWidget.header().setStretchLastSection(True)
        self.fomstatsTextBrowser = QtWidgets.QTextBrowser(VisDataDialog)
        self.fomstatsTextBrowser.setGeometry(QtCore.QRect(120, 210, 191, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fomstatsTextBrowser.setFont(font)
        self.fomstatsTextBrowser.setObjectName("fomstatsTextBrowser")
        self.textBrowser_fomhist = QtWidgets.QTextBrowser(VisDataDialog)
        self.textBrowser_fomhist.setGeometry(QtCore.QRect(320, 250, 371, 181))
        self.textBrowser_fomhist.setObjectName("textBrowser_fomhist")
        self.FilenameFilterPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.FilenameFilterPushButton.setGeometry(QtCore.QRect(10, 128, 101, 31))
        self.FilenameFilterPushButton.setObjectName("FilenameFilterPushButton")
        self.UpdateFiltersPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.UpdateFiltersPushButton.setGeometry(QtCore.QRect(470, 22, 111, 21))
        self.UpdateFiltersPushButton.setObjectName("UpdateFiltersPushButton")
        self.compPlotMarkSelectionsCheckBox = QtWidgets.QCheckBox(VisDataDialog)
        self.compPlotMarkSelectionsCheckBox.setGeometry(QtCore.QRect(880, 50, 51, 41))
        self.compPlotMarkSelectionsCheckBox.setObjectName(
            "compPlotMarkSelectionsCheckBox"
        )
        self.UpdatePlotPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.UpdatePlotPushButton.setGeometry(QtCore.QRect(580, 22, 101, 21))
        self.UpdatePlotPushButton.setObjectName("UpdatePlotPushButton")
        self.ontheflyPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.ontheflyPushButton.setGeometry(QtCore.QRect(0, 280, 111, 21))
        self.ontheflyPushButton.setObjectName("ontheflyPushButton")
        self.line_3 = QtWidgets.QFrame(VisDataDialog)
        self.line_3.setGeometry(QtCore.QRect(300, 350, 20, 81))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.customxystylePushButton = QtWidgets.QPushButton(VisDataDialog)
        self.customxystylePushButton.setGeometry(QtCore.QRect(10, 360, 61, 31))
        self.customxystylePushButton.setObjectName("customxystylePushButton")
        self.line_5 = QtWidgets.QFrame(VisDataDialog)
        self.line_5.setGeometry(QtCore.QRect(680, 10, 20, 171))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line = QtWidgets.QFrame(VisDataDialog)
        self.line.setGeometry(QtCore.QRect(0, 340, 121, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.SaveFigsPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.SaveFigsPushButton.setGeometry(QtCore.QRect(10, 198, 101, 23))
        self.SaveFigsPushButton.setObjectName("SaveFigsPushButton")
        self.SummaryTextBrowser = QtWidgets.QTextBrowser(VisDataDialog)
        self.SummaryTextBrowser.setGeometry(QtCore.QRect(120, 30, 241, 171))
        self.SummaryTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SummaryTextBrowser.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn
        )
        self.SummaryTextBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.SummaryTextBrowser.setObjectName("SummaryTextBrowser")
        self.line_4 = QtWidgets.QFrame(VisDataDialog)
        self.line_4.setGeometry(QtCore.QRect(109, 30, 21, 311))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_2 = QtWidgets.QFrame(VisDataDialog)
        self.line_2.setGeometry(QtCore.QRect(0, 270, 121, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.platescatterLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.platescatterLineEdit.setGeometry(QtCore.QRect(740, 190, 41, 22))
        self.platescatterLineEdit.setObjectName("platescatterLineEdit")
        self.label_16 = QtWidgets.QLabel(VisDataDialog)
        self.label_16.setGeometry(QtCore.QRect(700, 190, 41, 21))
        self.label_16.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_16.setObjectName("label_16")
        self.ellabelsLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.ellabelsLineEdit.setGeometry(QtCore.QRect(590, 220, 101, 22))
        self.ellabelsLineEdit.setText("")
        self.ellabelsLineEdit.setObjectName("ellabelsLineEdit")
        self.label_17 = QtWidgets.QLabel(VisDataDialog)
        self.label_17.setGeometry(QtCore.QRect(590, 200, 91, 21))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(VisDataDialog)
        self.label_18.setGeometry(QtCore.QRect(490, 200, 91, 21))
        self.label_18.setObjectName("label_18")
        self.platemapfilenameLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.platemapfilenameLineEdit.setGeometry(QtCore.QRect(490, 220, 101, 22))
        self.platemapfilenameLineEdit.setText("")
        self.platemapfilenameLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.platemapfilenameLineEdit.setObjectName("platemapfilenameLineEdit")
        self.SaveStdFigsPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.SaveStdFigsPushButton.setGeometry(QtCore.QRect(10, 218, 101, 23))
        self.SaveStdFigsPushButton.setObjectName("SaveStdFigsPushButton")
        self.LoadCsvPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.LoadCsvPushButton.setGeometry(QtCore.QRect(10, 168, 101, 21))
        self.LoadCsvPushButton.setObjectName("LoadCsvPushButton")
        self.expanafilenameLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.expanafilenameLineEdit.setGeometry(QtCore.QRect(100, 0, 251, 21))
        self.expanafilenameLineEdit.setText("")
        self.expanafilenameLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.expanafilenameLineEdit.setObjectName("expanafilenameLineEdit")
        self.ClearPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.ClearPushButton.setGeometry(QtCore.QRect(10, 250, 91, 21))
        self.ClearPushButton.setObjectName("ClearPushButton")
        self.RaiseErrorPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(1570, 20, 31, 23))
        self.RaiseErrorPushButton.setObjectName("RaiseErrorPushButton")
        self.BatchComboBox = QtWidgets.QComboBox(VisDataDialog)
        self.BatchComboBox.setGeometry(QtCore.QRect(430, 0, 251, 22))
        self.BatchComboBox.setObjectName("BatchComboBox")
        self.BatchPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.BatchPushButton.setGeometry(QtCore.QRect(370, 0, 61, 21))
        self.BatchPushButton.setObjectName("BatchPushButton")
        self.OpenInfoPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.OpenInfoPushButton.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.OpenInfoPushButton.setObjectName("OpenInfoPushButton")
        self.saveudiPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.saveudiPushButton.setGeometry(QtCore.QRect(1560, 0, 41, 23))
        self.saveudiPushButton.setObjectName("saveudiPushButton")
        self.addallsamplesPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.addallsamplesPushButton.setGeometry(QtCore.QRect(1500, 0, 31, 23))
        self.addallsamplesPushButton.setObjectName("addallsamplesPushButton")
        self.defaultplatemapCheckBox = QtWidgets.QCheckBox(VisDataDialog)
        self.defaultplatemapCheckBox.setGeometry(QtCore.QRect(10, 66, 91, 21))
        self.defaultplatemapCheckBox.setChecked(True)
        self.defaultplatemapCheckBox.setObjectName("defaultplatemapCheckBox")
        self.compCalcFromFOMCheckBox = QtWidgets.QCheckBox(VisDataDialog)
        self.compCalcFromFOMCheckBox.setGeometry(QtCore.QRect(330, 214, 101, 31))
        self.compCalcFromFOMCheckBox.setObjectName("compCalcFromFOMCheckBox")
        self.compsCalcFOMSearchStrLineEdit = QtWidgets.QLineEdit(VisDataDialog)
        self.compsCalcFOMSearchStrLineEdit.setGeometry(QtCore.QRect(430, 220, 51, 20))
        self.compsCalcFOMSearchStrLineEdit.setObjectName(
            "compsCalcFOMSearchStrLineEdit"
        )
        self.numcompintervalsSpinBox = QtWidgets.QSpinBox(VisDataDialog)
        self.numcompintervalsSpinBox.setGeometry(QtCore.QRect(820, 190, 31, 22))
        self.numcompintervalsSpinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.numcompintervalsSpinBox.setMaximum(100)
        self.numcompintervalsSpinBox.setObjectName("numcompintervalsSpinBox")
        self.label_19 = QtWidgets.QLabel(VisDataDialog)
        self.label_19.setGeometry(QtCore.QRect(780, 190, 41, 21))
        self.label_19.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_19.setObjectName("label_19")
        self.FilterFomPlotBySelectionPushButton = QtWidgets.QPushButton(VisDataDialog)
        self.FilterFomPlotBySelectionPushButton.setGeometry(
            QtCore.QRect(1500, 20, 71, 23)
        )
        self.FilterFomPlotBySelectionPushButton.setObjectName(
            "FilterFomPlotBySelectionPushButton"
        )
        self.lockrightyCheckBox = QtWidgets.QCheckBox(VisDataDialog)
        self.lockrightyCheckBox.setGeometry(QtCore.QRect(200, 370, 101, 21))
        self.lockrightyCheckBox.setChecked(True)
        self.lockrightyCheckBox.setObjectName("lockrightyCheckBox")
        self.retranslateUi(VisDataDialog)
        self.plateTabWidget.setCurrentIndex(0)
        self.compTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VisDataDialog)

    def retranslateUi(self, VisDataDialog):
        VisDataDialog.setWindowTitle(_translate("VisDataDialog", "Dialog", None))
        self.plateTabWidget.setTabText(
            self.plateTabWidget.indexOf(self.tab),
            _translate("VisDataDialog", "Tab 1", None),
        )
        self.compTabWidget.setTabText(
            self.compTabWidget.indexOf(self.tab_2),
            _translate("VisDataDialog", "Tab 1", None),
        )
        self.FolderPushButton.setText(
            _translate("VisDataDialog", "Open OnTheFly Dir", None)
        )
        self.AnaPushButton.setText(_translate("VisDataDialog", "Open ANA", None))
        self.ExpPushButton.setText(_translate("VisDataDialog", "Open EXP", None))
        self.UpdateFolderPushButton.setText(
            _translate("VisDataDialog", "^  update  ^", None)
        )
        self.OnFlyStoreInterCheckBox.setText(
            _translate("VisDataDialog", "store interm.\n" "data", None)
        )
        self.label.setText(_translate("VisDataDialog", "a,b,c,d\n" "Comp:", None))
        self.label_2.setText(_translate("VisDataDialog", "x,y\n" "Posn:", None))
        self.label_3.setText(_translate("VisDataDialog", "Sample\n" "No(s):", None))
        self.addComp.setText(_translate("VisDataDialog", "+", None))
        self.remComp.setText(_translate("VisDataDialog", "-", None))
        self.remxy.setText(_translate("VisDataDialog", "-", None))
        self.addxy.setText(_translate("VisDataDialog", "+", None))
        self.remSample.setText(_translate("VisDataDialog", "-", None))
        self.addSample.setText(_translate("VisDataDialog", "+", None))
        self.label_4.setText(_translate("VisDataDialog", "Element plot order:", None))
        self.label_5.setText(_translate("VisDataDialog", "fom to plot", None))
        self.fomplotchoiceComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_6.setText(_translate("VisDataDialog", "Comp. plot type:", None))
        self.CompPlotTypeComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_8.setText(_translate("VisDataDialog", "fom range min,max", None))
        self.label_10.setText(_translate("VisDataDialog", "color\n" "map", None))
        self.stdcsvplotchoiceComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.compplotsizeLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.compplotsizeLineEdit.setText(_translate("VisDataDialog", "patch", None))
        self.belowrangecolLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.label_9.setText(_translate("VisDataDialog", "standard plot", None))
        self.label_11.setText(
            _translate("VisDataDialog", "Comp.\n" "point size:", None)
        )
        self.colormapLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.colormapLineEdit.setText(_translate("VisDataDialog", "jet", None))
        self.vminmaxLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.CompPlotOrderComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_12.setText(
            _translate(
                "VisDataDialog", "out of range colors\n" "   < min       > max", None
            )
        )
        self.aboverangecolLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.rightyplotchoiceComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_13.setText(_translate("VisDataDialog", "right y-axis", None))
        self.yplotchoiceComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_14.setText(_translate("VisDataDialog", "y-axis", None))
        self.xplotchoiceComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_15.setText(_translate("VisDataDialog", "x-axis", None))
        self.customxylegendPushButton.setText(
            _translate("VisDataDialog", "customize\n" "x-y legend", None)
        )
        self.overlayselectCheckBox.setText(
            _translate("VisDataDialog", "x-y overlay", None)
        )
        self.FilenameFilterPushButton.setText(
            _translate("VisDataDialog", "Create file filter\n" "(for OnTheFly)", None)
        )
        self.UpdateFiltersPushButton.setText(
            _translate("VisDataDialog", "update plots+filters", None)
        )
        self.compPlotMarkSelectionsCheckBox.setText(
            _translate("VisDataDialog", "Mark->\n" "these\n" "comps", None)
        )
        self.UpdatePlotPushButton.setText(
            _translate("VisDataDialog", "update plots only", None)
        )
        self.ontheflyPushButton.setToolTip(
            _translate(
                "VisDataDialog",
                'Perform on the first checked "technique" and "type"',
                None,
            )
        )
        self.ontheflyPushButton.setText(
            _translate("VisDataDialog", "perform on-the-fly", None)
        )
        self.customxystylePushButton.setText(
            _translate("VisDataDialog", "configure\n" "x-y style", None)
        )
        self.SaveFigsPushButton.setText(
            _translate("VisDataDialog", "Save figs to ANA", None)
        )
        self.platescatterLineEdit.setToolTip(
            _translate(
                "VisDataDialog",
                "first character can be the markertype, e.g. 's' for square, or this can be omitted.\n"
                "Rest of the string is the interger marker size.",
                None,
            )
        )
        self.platescatterLineEdit.setText(_translate("VisDataDialog", "s70", None))
        self.label_16.setText(_translate("VisDataDialog", "plate\n" "scatter", None))
        self.ellabelsLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.label_17.setText(_translate("VisDataDialog", "Element Labels", None))
        self.label_18.setText(_translate("VisDataDialog", "platemap filename", None))
        self.platemapfilenameLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.SaveStdFigsPushButton.setText(
            _translate("VisDataDialog", "BatchSave StdPlots", None)
        )
        self.LoadCsvPushButton.setText(_translate("VisDataDialog", "Load .csv", None))
        self.expanafilenameLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.ClearPushButton.setText(_translate("VisDataDialog", "Clear Data", None))
        self.RaiseErrorPushButton.setText(_translate("VisDataDialog", "err", None))
        self.BatchComboBox.setToolTip(
            _translate(
                "VisDataDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.BatchPushButton.setToolTip(
            _translate(
                "VisDataDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.BatchPushButton.setText(_translate("VisDataDialog", "Run Batch:", None))
        self.OpenInfoPushButton.setText(
            _translate("VisDataDialog", "Open via Search", None)
        )
        self.saveudiPushButton.setText(_translate("VisDataDialog", "->udi", None))
        self.addallsamplesPushButton.setText(_translate("VisDataDialog", "+all", None))
        self.defaultplatemapCheckBox.setText(
            _translate("VisDataDialog", "dflt platemap?", None)
        )
        self.compCalcFromFOMCheckBox.setText(
            _translate("VisDataDialog", "Calc. comps from\n" "FOMs containing:", None)
        )
        self.compsCalcFOMSearchStrLineEdit.setToolTip(
            _translate("VisDataDialog", "Comment string to be included in EXP", None)
        )
        self.compsCalcFOMSearchStrLineEdit.setText(
            _translate("VisDataDialog", "AtFrac", None)
        )
        self.label_19.setText(_translate("VisDataDialog", "comp\n" "intervs", None))
        self.FilterFomPlotBySelectionPushButton.setText(
            _translate("VisDataDialog", "plot selected", None)
        )
        self.lockrightyCheckBox.setText(
            _translate("VisDataDialog", "right-y lock range", None)
        )
