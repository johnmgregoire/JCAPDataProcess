# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\PlotAnaForm.ui'
#
# Created: Sun May 31 20:38:39 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(868, 724)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(40, 120, 591, 411))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser_plate = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_plate.setGeometry(QtCore.QRect(0, 20, 561, 341))
        self.textBrowser_plate.setObjectName("textBrowser_plate")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QtCore.QCoreApplication.translate("Dialog", "Dialog", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QtCore.QCoreApplication.translate("Dialog", "Tab 1", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QtCore.QCoreApplication.translate("Dialog", "Tab 2", None),
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
