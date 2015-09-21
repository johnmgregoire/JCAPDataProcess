# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveImagesForm.ui'
#
# Created: Mon Sep 21 14:02:14 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SaveImagesDialog(object):
    def setupUi(self, SaveImagesDialog):
        SaveImagesDialog.setObjectName(_fromUtf8("SaveImagesDialog"))
        SaveImagesDialog.resize(579, 408)
        self.buttonBox = QtGui.QDialogButtonBox(SaveImagesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(230, 360, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.FilesTreeWidget = QtGui.QTreeWidget(SaveImagesDialog)
        self.FilesTreeWidget.setGeometry(QtCore.QRect(10, 10, 561, 341))
        self.FilesTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.FilesTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.FilesTreeWidget.setHeaderHidden(True)
        self.FilesTreeWidget.setExpandsOnDoubleClick(False)
        self.FilesTreeWidget.setObjectName(_fromUtf8("FilesTreeWidget"))
        self.FilesTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.FilesTreeWidget.header().setVisible(False)
        self.FilesTreeWidget.header().setCascadingSectionResizes(False)
        self.FilesTreeWidget.header().setStretchLastSection(True)
        self.overwriteCheckBox = QtGui.QCheckBox(SaveImagesDialog)
        self.overwriteCheckBox.setGeometry(QtCore.QRect(30, 370, 101, 21))
        self.overwriteCheckBox.setChecked(True)
        self.overwriteCheckBox.setObjectName(_fromUtf8("overwriteCheckBox"))
        self.doneCheckBox = QtGui.QCheckBox(SaveImagesDialog)
        self.doneCheckBox.setGeometry(QtCore.QRect(140, 370, 101, 21))
        self.doneCheckBox.setChecked(False)
        self.doneCheckBox.setObjectName(_fromUtf8("doneCheckBox"))

        self.retranslateUi(SaveImagesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SaveImagesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SaveImagesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveImagesDialog)

    def retranslateUi(self, SaveImagesDialog):
        SaveImagesDialog.setWindowTitle(QtGui.QApplication.translate("SaveImagesDialog", "ChooseImagesToSave", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteCheckBox.setText(QtGui.QApplication.translate("SaveImagesDialog", "overwrite files\n"
"with same name", None, QtGui.QApplication.UnicodeUTF8))
        self.doneCheckBox.setText(QtGui.QApplication.translate("SaveImagesDialog", "convert .run \n"
"to .done", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SaveImagesDialog = QtGui.QDialog()
    ui = Ui_SaveImagesDialog()
    ui.setupUi(SaveImagesDialog)
    SaveImagesDialog.show()
    sys.exit(app.exec_())

