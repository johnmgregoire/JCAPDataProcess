# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\PlotAnaForm.ui'
#
# Created: Thu Feb 25 22:21:55 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VisDataDialog(object):
    def setupUi(self, VisDataDialog):
        VisDataDialog.setObjectName(_fromUtf8("VisDataDialog"))
        VisDataDialog.resize(1597, 1026)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VisDataDialog.sizePolicy().hasHeightForWidth())
        VisDataDialog.setSizePolicy(sizePolicy)
        self.plateTabWidget = QtGui.QTabWidget(VisDataDialog)
        self.plateTabWidget.setGeometry(QtCore.QRect(700, 610, 891, 401))
        self.plateTabWidget.setObjectName(_fromUtf8("plateTabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.textBrowser_plate = QtGui.QTextBrowser(self.tab)
        self.textBrowser_plate.setGeometry(QtCore.QRect(0, 30, 881, 371))
        self.textBrowser_plate.setObjectName(_fromUtf8("textBrowser_plate"))
        self.plateTabWidget.addTab(self.tab, _fromUtf8(""))
        self.AnaExpFomTreeWidget = QtGui.QTreeWidget(VisDataDialog)
        self.AnaExpFomTreeWidget.setGeometry(QtCore.QRect(0, 740, 681, 271))
        self.AnaExpFomTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AnaExpFomTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.AnaExpFomTreeWidget.setHeaderHidden(True)
        self.AnaExpFomTreeWidget.setExpandsOnDoubleClick(False)
        self.AnaExpFomTreeWidget.setObjectName(_fromUtf8("AnaExpFomTreeWidget"))
        self.AnaExpFomTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.AnaExpFomTreeWidget.header().setVisible(False)
        self.AnaExpFomTreeWidget.header().setCascadingSectionResizes(False)
        self.AnaExpFomTreeWidget.header().setStretchLastSection(True)
        self.textBrowser_xy = QtGui.QTextBrowser(VisDataDialog)
        self.textBrowser_xy.setGeometry(QtCore.QRect(0, 440, 681, 291))
        self.textBrowser_xy.setObjectName(_fromUtf8("textBrowser_xy"))
        self.compTabWidget = QtGui.QTabWidget(VisDataDialog)
        self.compTabWidget.setGeometry(QtCore.QRect(700, 210, 891, 401))
        self.compTabWidget.setObjectName(_fromUtf8("compTabWidget"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.textBrowser_comp = QtGui.QTextBrowser(self.tab_2)
        self.textBrowser_comp.setGeometry(QtCore.QRect(0, 30, 881, 371))
        self.textBrowser_comp.setObjectName(_fromUtf8("textBrowser_comp"))
        self.compTabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.browser = QtGui.QTextBrowser(VisDataDialog)
        self.browser.setGeometry(QtCore.QRect(930, 40, 651, 171))
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.browser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.browser.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.browser.setObjectName(_fromUtf8("browser"))
        self.FolderPushButton = QtGui.QPushButton(VisDataDialog)
        self.FolderPushButton.setGeometry(QtCore.QRect(10, 70, 101, 23))
        self.FolderPushButton.setObjectName(_fromUtf8("FolderPushButton"))
        self.AnaPushButton = QtGui.QPushButton(VisDataDialog)
        self.AnaPushButton.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.AnaPushButton.setObjectName(_fromUtf8("AnaPushButton"))
        self.ExpPushButton = QtGui.QPushButton(VisDataDialog)
        self.ExpPushButton.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.ExpPushButton.setObjectName(_fromUtf8("ExpPushButton"))
        self.UpdateFolderPushButton = QtGui.QPushButton(VisDataDialog)
        self.UpdateFolderPushButton.setGeometry(QtCore.QRect(10, 90, 101, 21))
        self.UpdateFolderPushButton.setObjectName(_fromUtf8("UpdateFolderPushButton"))
        self.OnFlyAnaClassComboBox = QtGui.QComboBox(VisDataDialog)
        self.OnFlyAnaClassComboBox.setGeometry(QtCore.QRect(0, 290, 111, 22))
        self.OnFlyAnaClassComboBox.setObjectName(_fromUtf8("OnFlyAnaClassComboBox"))
        self.OnFlyStoreInterCheckBox = QtGui.QCheckBox(VisDataDialog)
        self.OnFlyStoreInterCheckBox.setGeometry(QtCore.QRect(0, 320, 81, 21))
        self.OnFlyStoreInterCheckBox.setObjectName(_fromUtf8("OnFlyStoreInterCheckBox"))
        self.compLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.compLineEdit.setGeometry(QtCore.QRect(990, 10, 111, 20))
        self.compLineEdit.setToolTip(_fromUtf8(""))
        self.compLineEdit.setText(_fromUtf8(""))
        self.compLineEdit.setObjectName(_fromUtf8("compLineEdit"))
        self.label = QtGui.QLabel(VisDataDialog)
        self.label.setGeometry(QtCore.QRect(950, 0, 46, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(VisDataDialog)
        self.label_2.setGeometry(QtCore.QRect(1160, 0, 46, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.xyLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.xyLineEdit.setGeometry(QtCore.QRect(1200, 10, 111, 20))
        self.xyLineEdit.setToolTip(_fromUtf8(""))
        self.xyLineEdit.setObjectName(_fromUtf8("xyLineEdit"))
        self.label_3 = QtGui.QLabel(VisDataDialog)
        self.label_3.setGeometry(QtCore.QRect(1370, 0, 46, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.sampleLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.sampleLineEdit.setGeometry(QtCore.QRect(1410, 10, 111, 20))
        self.sampleLineEdit.setToolTip(_fromUtf8(""))
        self.sampleLineEdit.setObjectName(_fromUtf8("sampleLineEdit"))
        self.addComp = QtGui.QPushButton(VisDataDialog)
        self.addComp.setGeometry(QtCore.QRect(1100, 10, 21, 23))
        self.addComp.setObjectName(_fromUtf8("addComp"))
        self.remComp = QtGui.QPushButton(VisDataDialog)
        self.remComp.setGeometry(QtCore.QRect(1120, 10, 21, 23))
        self.remComp.setObjectName(_fromUtf8("remComp"))
        self.remxy = QtGui.QPushButton(VisDataDialog)
        self.remxy.setGeometry(QtCore.QRect(1330, 10, 21, 23))
        self.remxy.setObjectName(_fromUtf8("remxy"))
        self.addxy = QtGui.QPushButton(VisDataDialog)
        self.addxy.setGeometry(QtCore.QRect(1310, 10, 21, 23))
        self.addxy.setObjectName(_fromUtf8("addxy"))
        self.remSample = QtGui.QPushButton(VisDataDialog)
        self.remSample.setGeometry(QtCore.QRect(1540, 10, 21, 23))
        self.remSample.setObjectName(_fromUtf8("remSample"))
        self.addSample = QtGui.QPushButton(VisDataDialog)
        self.addSample.setGeometry(QtCore.QRect(1520, 10, 21, 23))
        self.addSample.setObjectName(_fromUtf8("addSample"))
        self.label_4 = QtGui.QLabel(VisDataDialog)
        self.label_4.setGeometry(QtCore.QRect(700, 130, 91, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(VisDataDialog)
        self.label_5.setGeometry(QtCore.QRect(700, 40, 119, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.fomplotchoiceComboBox = QtGui.QComboBox(VisDataDialog)
        self.fomplotchoiceComboBox.setGeometry(QtCore.QRect(700, 60, 111, 21))
        self.fomplotchoiceComboBox.setWhatsThis(_fromUtf8(""))
        self.fomplotchoiceComboBox.setObjectName(_fromUtf8("fomplotchoiceComboBox"))
        self.label_6 = QtGui.QLabel(VisDataDialog)
        self.label_6.setGeometry(QtCore.QRect(700, 80, 111, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.CompPlotTypeComboBox = QtGui.QComboBox(VisDataDialog)
        self.CompPlotTypeComboBox.setGeometry(QtCore.QRect(700, 100, 111, 31))
        self.CompPlotTypeComboBox.setObjectName(_fromUtf8("CompPlotTypeComboBox"))
        self.label_8 = QtGui.QLabel(VisDataDialog)
        self.label_8.setGeometry(QtCore.QRect(820, 90, 91, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_10 = QtGui.QLabel(VisDataDialog)
        self.label_10.setGeometry(QtCore.QRect(810, 180, 51, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.stdcsvplotchoiceComboBox = QtGui.QComboBox(VisDataDialog)
        self.stdcsvplotchoiceComboBox.setGeometry(QtCore.QRect(700, 20, 211, 22))
        self.stdcsvplotchoiceComboBox.setObjectName(_fromUtf8("stdcsvplotchoiceComboBox"))
        self.compplotsizeLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.compplotsizeLineEdit.setGeometry(QtCore.QRect(820, 60, 91, 22))
        self.compplotsizeLineEdit.setObjectName(_fromUtf8("compplotsizeLineEdit"))
        self.belowrangecolLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.belowrangecolLineEdit.setGeometry(QtCore.QRect(800, 160, 61, 22))
        self.belowrangecolLineEdit.setObjectName(_fromUtf8("belowrangecolLineEdit"))
        self.label_9 = QtGui.QLabel(VisDataDialog)
        self.label_9.setGeometry(QtCore.QRect(700, 0, 111, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_11 = QtGui.QLabel(VisDataDialog)
        self.label_11.setGeometry(QtCore.QRect(820, 40, 91, 21))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.colormapLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.colormapLineEdit.setGeometry(QtCore.QRect(860, 181, 51, 21))
        self.colormapLineEdit.setObjectName(_fromUtf8("colormapLineEdit"))
        self.vminmaxLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.vminmaxLineEdit.setGeometry(QtCore.QRect(820, 110, 91, 22))
        self.vminmaxLineEdit.setObjectName(_fromUtf8("vminmaxLineEdit"))
        self.CompPlotOrderComboBox = QtGui.QComboBox(VisDataDialog)
        self.CompPlotOrderComboBox.setGeometry(QtCore.QRect(700, 150, 91, 22))
        self.CompPlotOrderComboBox.setObjectName(_fromUtf8("CompPlotOrderComboBox"))
        self.label_12 = QtGui.QLabel(VisDataDialog)
        self.label_12.setGeometry(QtCore.QRect(810, 130, 101, 31))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.aboverangecolLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.aboverangecolLineEdit.setGeometry(QtCore.QRect(860, 160, 61, 22))
        self.aboverangecolLineEdit.setObjectName(_fromUtf8("aboverangecolLineEdit"))
        self.rightyplotchoiceComboBox = QtGui.QComboBox(VisDataDialog)
        self.rightyplotchoiceComboBox.setGeometry(QtCore.QRect(200, 410, 111, 22))
        self.rightyplotchoiceComboBox.setObjectName(_fromUtf8("rightyplotchoiceComboBox"))
        self.label_13 = QtGui.QLabel(VisDataDialog)
        self.label_13.setGeometry(QtCore.QRect(200, 390, 111, 21))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.yplotchoiceComboBox = QtGui.QComboBox(VisDataDialog)
        self.yplotchoiceComboBox.setGeometry(QtCore.QRect(80, 410, 111, 22))
        self.yplotchoiceComboBox.setObjectName(_fromUtf8("yplotchoiceComboBox"))
        self.label_14 = QtGui.QLabel(VisDataDialog)
        self.label_14.setGeometry(QtCore.QRect(80, 390, 111, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.xplotchoiceComboBox = QtGui.QComboBox(VisDataDialog)
        self.xplotchoiceComboBox.setGeometry(QtCore.QRect(80, 370, 111, 22))
        self.xplotchoiceComboBox.setObjectName(_fromUtf8("xplotchoiceComboBox"))
        self.label_15 = QtGui.QLabel(VisDataDialog)
        self.label_15.setGeometry(QtCore.QRect(80, 350, 111, 21))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.customxylegendPushButton = QtGui.QPushButton(VisDataDialog)
        self.customxylegendPushButton.setGeometry(QtCore.QRect(10, 400, 61, 31))
        self.customxylegendPushButton.setObjectName(_fromUtf8("customxylegendPushButton"))
        self.overlayselectCheckBox = QtGui.QCheckBox(VisDataDialog)
        self.overlayselectCheckBox.setGeometry(QtCore.QRect(210, 360, 81, 17))
        self.overlayselectCheckBox.setObjectName(_fromUtf8("overlayselectCheckBox"))
        self.SelectTreeWidget = QtGui.QTreeWidget(VisDataDialog)
        self.SelectTreeWidget.setGeometry(QtCore.QRect(370, 30, 201, 171))
        self.SelectTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SelectTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.SelectTreeWidget.setHeaderHidden(True)
        self.SelectTreeWidget.setExpandsOnDoubleClick(False)
        self.SelectTreeWidget.setObjectName(_fromUtf8("SelectTreeWidget"))
        self.SelectTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.SelectTreeWidget.header().setVisible(False)
        self.SelectTreeWidget.header().setCascadingSectionResizes(False)
        self.SelectTreeWidget.header().setStretchLastSection(True)
        self.fomstatsTextBrowser = QtGui.QTextBrowser(VisDataDialog)
        self.fomstatsTextBrowser.setGeometry(QtCore.QRect(120, 210, 191, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fomstatsTextBrowser.setFont(font)
        self.fomstatsTextBrowser.setObjectName(_fromUtf8("fomstatsTextBrowser"))
        self.textBrowser_fomhist = QtGui.QTextBrowser(VisDataDialog)
        self.textBrowser_fomhist.setGeometry(QtCore.QRect(320, 210, 371, 221))
        self.textBrowser_fomhist.setObjectName(_fromUtf8("textBrowser_fomhist"))
        self.FilenameFilterPushButton = QtGui.QPushButton(VisDataDialog)
        self.FilenameFilterPushButton.setGeometry(QtCore.QRect(10, 110, 101, 31))
        self.FilenameFilterPushButton.setObjectName(_fromUtf8("FilenameFilterPushButton"))
        self.UpdateFiltersPushButton = QtGui.QPushButton(VisDataDialog)
        self.UpdateFiltersPushButton.setGeometry(QtCore.QRect(580, 30, 101, 23))
        self.UpdateFiltersPushButton.setObjectName(_fromUtf8("UpdateFiltersPushButton"))
        self.compPlotMarkSelectionsCheckBox = QtGui.QCheckBox(VisDataDialog)
        self.compPlotMarkSelectionsCheckBox.setGeometry(QtCore.QRect(580, 90, 101, 31))
        self.compPlotMarkSelectionsCheckBox.setObjectName(_fromUtf8("compPlotMarkSelectionsCheckBox"))
        self.UpdatePlotPushButton = QtGui.QPushButton(VisDataDialog)
        self.UpdatePlotPushButton.setGeometry(QtCore.QRect(580, 60, 101, 23))
        self.UpdatePlotPushButton.setObjectName(_fromUtf8("UpdatePlotPushButton"))
        self.ontheflyPushButton = QtGui.QPushButton(VisDataDialog)
        self.ontheflyPushButton.setGeometry(QtCore.QRect(0, 260, 111, 21))
        self.ontheflyPushButton.setObjectName(_fromUtf8("ontheflyPushButton"))
        self.line_3 = QtGui.QFrame(VisDataDialog)
        self.line_3.setGeometry(QtCore.QRect(300, 350, 20, 81))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.customxystylePushButton = QtGui.QPushButton(VisDataDialog)
        self.customxystylePushButton.setGeometry(QtCore.QRect(10, 360, 61, 31))
        self.customxystylePushButton.setObjectName(_fromUtf8("customxystylePushButton"))
        self.line_5 = QtGui.QFrame(VisDataDialog)
        self.line_5.setGeometry(QtCore.QRect(680, 10, 20, 171))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.line = QtGui.QFrame(VisDataDialog)
        self.line.setGeometry(QtCore.QRect(10, 341, 291, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.SaveFigsPushButton = QtGui.QPushButton(VisDataDialog)
        self.SaveFigsPushButton.setGeometry(QtCore.QRect(10, 180, 101, 23))
        self.SaveFigsPushButton.setObjectName(_fromUtf8("SaveFigsPushButton"))
        self.SummaryTextBrowser = QtGui.QTextBrowser(VisDataDialog)
        self.SummaryTextBrowser.setGeometry(QtCore.QRect(120, 30, 241, 171))
        self.SummaryTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SummaryTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SummaryTextBrowser.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.SummaryTextBrowser.setObjectName(_fromUtf8("SummaryTextBrowser"))
        self.line_4 = QtGui.QFrame(VisDataDialog)
        self.line_4.setGeometry(QtCore.QRect(109, 30, 21, 311))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.line_2 = QtGui.QFrame(VisDataDialog)
        self.line_2.setGeometry(QtCore.QRect(0, 250, 121, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.platescatterLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.platescatterLineEdit.setGeometry(QtCore.QRect(750, 180, 41, 22))
        self.platescatterLineEdit.setObjectName(_fromUtf8("platescatterLineEdit"))
        self.label_16 = QtGui.QLabel(VisDataDialog)
        self.label_16.setGeometry(QtCore.QRect(710, 180, 51, 21))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.ellabelsLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.ellabelsLineEdit.setGeometry(QtCore.QRect(580, 140, 101, 22))
        self.ellabelsLineEdit.setText(_fromUtf8(""))
        self.ellabelsLineEdit.setObjectName(_fromUtf8("ellabelsLineEdit"))
        self.label_17 = QtGui.QLabel(VisDataDialog)
        self.label_17.setGeometry(QtCore.QRect(580, 120, 91, 21))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(VisDataDialog)
        self.label_18.setGeometry(QtCore.QRect(580, 160, 91, 21))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.platemapfilenameLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.platemapfilenameLineEdit.setGeometry(QtCore.QRect(580, 180, 101, 22))
        self.platemapfilenameLineEdit.setText(_fromUtf8(""))
        self.platemapfilenameLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.platemapfilenameLineEdit.setObjectName(_fromUtf8("platemapfilenameLineEdit"))
        self.SaveStdFigsPushButton = QtGui.QPushButton(VisDataDialog)
        self.SaveStdFigsPushButton.setGeometry(QtCore.QRect(10, 200, 101, 23))
        self.SaveStdFigsPushButton.setObjectName(_fromUtf8("SaveStdFigsPushButton"))
        self.LoadCsvPushButton = QtGui.QPushButton(VisDataDialog)
        self.LoadCsvPushButton.setGeometry(QtCore.QRect(10, 150, 101, 21))
        self.LoadCsvPushButton.setObjectName(_fromUtf8("LoadCsvPushButton"))
        self.expanafilenameLineEdit = QtGui.QLineEdit(VisDataDialog)
        self.expanafilenameLineEdit.setGeometry(QtCore.QRect(110, 5, 251, 21))
        self.expanafilenameLineEdit.setText(_fromUtf8(""))
        self.expanafilenameLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.expanafilenameLineEdit.setObjectName(_fromUtf8("expanafilenameLineEdit"))
        self.ClearPushButton = QtGui.QPushButton(VisDataDialog)
        self.ClearPushButton.setGeometry(QtCore.QRect(10, 232, 91, 21))
        self.ClearPushButton.setObjectName(_fromUtf8("ClearPushButton"))
        self.RaiseErrorPushButton = QtGui.QPushButton(VisDataDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(1570, 10, 31, 23))
        self.RaiseErrorPushButton.setObjectName(_fromUtf8("RaiseErrorPushButton"))
        self.BatchComboBox = QtGui.QComboBox(VisDataDialog)
        self.BatchComboBox.setGeometry(QtCore.QRect(430, 0, 251, 22))
        self.BatchComboBox.setObjectName(_fromUtf8("BatchComboBox"))
        self.BatchPushButton = QtGui.QPushButton(VisDataDialog)
        self.BatchPushButton.setGeometry(QtCore.QRect(370, 0, 61, 21))
        self.BatchPushButton.setObjectName(_fromUtf8("BatchPushButton"))

        self.retranslateUi(VisDataDialog)
        self.plateTabWidget.setCurrentIndex(0)
        self.compTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VisDataDialog)

    def retranslateUi(self, VisDataDialog):
        VisDataDialog.setWindowTitle(QtGui.QApplication.translate("VisDataDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.plateTabWidget.setTabText(self.plateTabWidget.indexOf(self.tab), QtGui.QApplication.translate("VisDataDialog", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.compTabWidget.setTabText(self.compTabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("VisDataDialog", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.FolderPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Open OnTheFly Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.AnaPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Open ANA", None, QtGui.QApplication.UnicodeUTF8))
        self.ExpPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Open EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdateFolderPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "^  update  ^", None, QtGui.QApplication.UnicodeUTF8))
        self.OnFlyStoreInterCheckBox.setText(QtGui.QApplication.translate("VisDataDialog", "store interm.\n"
"data", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VisDataDialog", "a,b,c,d\n"
"Comp:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VisDataDialog", "x,y\n"
"Posn:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VisDataDialog", "Sample\n"
"No(s):", None, QtGui.QApplication.UnicodeUTF8))
        self.addComp.setText(QtGui.QApplication.translate("VisDataDialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.remComp.setText(QtGui.QApplication.translate("VisDataDialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.remxy.setText(QtGui.QApplication.translate("VisDataDialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.addxy.setText(QtGui.QApplication.translate("VisDataDialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.remSample.setText(QtGui.QApplication.translate("VisDataDialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.addSample.setText(QtGui.QApplication.translate("VisDataDialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VisDataDialog", "Element plot order:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("VisDataDialog", "fom to plot", None, QtGui.QApplication.UnicodeUTF8))
        self.fomplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("VisDataDialog", "Comp. plot type:", None, QtGui.QApplication.UnicodeUTF8))
        self.CompPlotTypeComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("VisDataDialog", "fom range min,max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("VisDataDialog", "colormap:", None, QtGui.QApplication.UnicodeUTF8))
        self.stdcsvplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.compplotsizeLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.compplotsizeLineEdit.setText(QtGui.QApplication.translate("VisDataDialog", "patch", None, QtGui.QApplication.UnicodeUTF8))
        self.belowrangecolLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("VisDataDialog", "standard plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("VisDataDialog", "Comp. point size:", None, QtGui.QApplication.UnicodeUTF8))
        self.colormapLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.colormapLineEdit.setText(QtGui.QApplication.translate("VisDataDialog", "jet", None, QtGui.QApplication.UnicodeUTF8))
        self.vminmaxLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.CompPlotOrderComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("VisDataDialog", "out of range colors\n"
"   < min       > max", None, QtGui.QApplication.UnicodeUTF8))
        self.aboverangecolLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.rightyplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("VisDataDialog", "right y-axis", None, QtGui.QApplication.UnicodeUTF8))
        self.yplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("VisDataDialog", "y-axis", None, QtGui.QApplication.UnicodeUTF8))
        self.xplotchoiceComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("VisDataDialog", "x-axis", None, QtGui.QApplication.UnicodeUTF8))
        self.customxylegendPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "customize\n"
"x-y legend", None, QtGui.QApplication.UnicodeUTF8))
        self.overlayselectCheckBox.setText(QtGui.QApplication.translate("VisDataDialog", "x-y overlay", None, QtGui.QApplication.UnicodeUTF8))
        self.FilenameFilterPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Create file filter\n"
"(for OnTheFly)", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdateFiltersPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "update plots+filters", None, QtGui.QApplication.UnicodeUTF8))
        self.compPlotMarkSelectionsCheckBox.setText(QtGui.QApplication.translate("VisDataDialog", "Mark selections\n"
"on Comp.plots", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdatePlotPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "update plots only", None, QtGui.QApplication.UnicodeUTF8))
        self.ontheflyPushButton.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Perform on the first checked \"technique\" and \"type\"", None, QtGui.QApplication.UnicodeUTF8))
        self.ontheflyPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "perform on-the-fly", None, QtGui.QApplication.UnicodeUTF8))
        self.customxystylePushButton.setText(QtGui.QApplication.translate("VisDataDialog", "configure\n"
"x-y style", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveFigsPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Save figs to ANA", None, QtGui.QApplication.UnicodeUTF8))
        self.platescatterLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "first character can be the markertype, e.g. \'s\' for square, or this can be omitted.\n"
"Rest of the string is the interger marker size.", None, QtGui.QApplication.UnicodeUTF8))
        self.platescatterLineEdit.setText(QtGui.QApplication.translate("VisDataDialog", "s70", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("VisDataDialog", "plate\n"
"scatter:", None, QtGui.QApplication.UnicodeUTF8))
        self.ellabelsLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("VisDataDialog", "Element Labels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("VisDataDialog", "platemap filename", None, QtGui.QApplication.UnicodeUTF8))
        self.platemapfilenameLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveStdFigsPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "BatchSave StdPlots", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadCsvPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Load .csv", None, QtGui.QApplication.UnicodeUTF8))
        self.expanafilenameLineEdit.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Comment string to be included in EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Clear Data", None, QtGui.QApplication.UnicodeUTF8))
        self.RaiseErrorPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "err", None, QtGui.QApplication.UnicodeUTF8))
        self.BatchComboBox.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Apply all other filteres in this section to only this run", None, QtGui.QApplication.UnicodeUTF8))
        self.BatchPushButton.setToolTip(QtGui.QApplication.translate("VisDataDialog", "Considering the files already in the EXP, keep the files that meet all criteria", None, QtGui.QApplication.UnicodeUTF8))
        self.BatchPushButton.setText(QtGui.QApplication.translate("VisDataDialog", "Run Batch:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    VisDataDialog = QtGui.QDialog()
    ui = Ui_VisDataDialog()
    ui.setupUi(VisDataDialog)
    VisDataDialog.show()
    sys.exit(app.exec_())

