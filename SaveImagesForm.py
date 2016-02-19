# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveImagesForm.ui'
#
# Created: Fri Feb 19 13:21:15 2016
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
        self.buttonBox.setGeometry(QtCore.QRect(410, 360, 161, 32))
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
        self.overwriteCheckBox.setGeometry(QtCore.QRect(10, 370, 101, 31))
        self.overwriteCheckBox.setChecked(True)
        self.overwriteCheckBox.setObjectName(_fromUtf8("overwriteCheckBox"))
        self.doneCheckBox = QtGui.QCheckBox(SaveImagesDialog)
        self.doneCheckBox.setGeometry(QtCore.QRect(120, 370, 81, 31))
        self.doneCheckBox.setChecked(False)
        self.doneCheckBox.setObjectName(_fromUtf8("doneCheckBox"))
        self.epsCheckBox = QtGui.QCheckBox(SaveImagesDialog)
        self.epsCheckBox.setGeometry(QtCore.QRect(215, 370, 71, 31))
        self.epsCheckBox.setChecked(True)
        self.epsCheckBox.setObjectName(_fromUtf8("epsCheckBox"))
        self.prependfilenameLineEdit = QtGui.QLineEdit(SaveImagesDialog)
        self.prependfilenameLineEdit.setGeometry(QtCore.QRect(285, 380, 113, 20))
        self.prependfilenameLineEdit.setObjectName(_fromUtf8("prependfilenameLineEdit"))
        self.label = QtGui.QLabel(SaveImagesDialog)
        self.label.setGeometry(QtCore.QRect(290, 360, 101, 20))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(SaveImagesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SaveImagesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SaveImagesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveImagesDialog)

    def retranslateUi(self, SaveImagesDialog):
        SaveImagesDialog.setWindowTitle(QtGui.QApplication.translate("SaveImagesDialog", "ChooseImagesToSave", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteCheckBox.setText(QtGui.QApplication.translate("SaveImagesDialog", "overwrite files\n"
"with same name", None, QtGui.QApplication.UnicodeUTF8))
        self.doneCheckBox.setText(QtGui.QApplication.translate("SaveImagesDialog", "convert\n"
"to .done", None, QtGui.QApplication.UnicodeUTF8))
        self.epsCheckBox.setText(QtGui.QApplication.translate("SaveImagesDialog", "also save\n"
".eps", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SaveImagesDialog", "Prepend to filename:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SaveImagesDialog = QtGui.QDialog()
    ui = Ui_SaveImagesDialog()
    ui.setupUi(SaveImagesDialog)
    SaveImagesDialog.show()
    sys.exit(app.exec_())

