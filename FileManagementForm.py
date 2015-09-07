# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\FileManagementForm.ui'
#
# Created: Mon Sep 07 10:47:34 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FileManDialog(object):
    def setupUi(self, FileManDialog):
        FileManDialog.setObjectName(_fromUtf8("FileManDialog"))
        FileManDialog.resize(560, 397)
        self.deletefoldersButton = QtGui.QPushButton(FileManDialog)
        self.deletefoldersButton.setGeometry(QtCore.QRect(170, 10, 131, 23))
        self.deletefoldersButton.setObjectName(_fromUtf8("deletefoldersButton"))
        self.foldersTreeWidget = QtGui.QTreeWidget(FileManDialog)
        self.foldersTreeWidget.setGeometry(QtCore.QRect(0, 50, 551, 341))
        self.foldersTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.foldersTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foldersTreeWidget.setHeaderHidden(True)
        self.foldersTreeWidget.setExpandsOnDoubleClick(False)
        self.foldersTreeWidget.setObjectName(_fromUtf8("foldersTreeWidget"))
        self.foldersTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.foldersTreeWidget.header().setVisible(False)
        self.foldersTreeWidget.header().setCascadingSectionResizes(False)
        self.foldersTreeWidget.header().setStretchLastSection(True)
        self.findfoldersButton = QtGui.QPushButton(FileManDialog)
        self.findfoldersButton.setGeometry(QtCore.QRect(20, 10, 131, 23))
        self.findfoldersButton.setObjectName(_fromUtf8("findfoldersButton"))

        self.retranslateUi(FileManDialog)
        QtCore.QMetaObject.connectSlotsByName(FileManDialog)

    def retranslateUi(self, FileManDialog):
        FileManDialog.setWindowTitle(QtGui.QApplication.translate("FileManDialog", "EXP+ANA file management", None, QtGui.QApplication.UnicodeUTF8))
        self.deletefoldersButton.setText(QtGui.QApplication.translate("FileManDialog", "delete selected folders", None, QtGui.QApplication.UnicodeUTF8))
        self.findfoldersButton.setText(QtGui.QApplication.translate("FileManDialog", "find .run folders", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FileManDialog = QtGui.QDialog()
    ui = Ui_FileManDialog()
    ui.setupUi(FileManDialog)
    FileManDialog.show()
    sys.exit(app.exec_())

