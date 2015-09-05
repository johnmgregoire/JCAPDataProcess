# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveButtonChoices.ui'
#
# Created: Fri Sep 04 21:12:56 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SaveOptionsDialog(object):
    def setupUi(self, SaveOptionsDialog):
        SaveOptionsDialog.setObjectName(_fromUtf8("SaveOptionsDialog"))
        SaveOptionsDialog.resize(353, 63)
        self.dfltButton = QtGui.QPushButton(SaveOptionsDialog)
        self.dfltButton.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.dfltButton.setObjectName(_fromUtf8("dfltButton"))
        self.tempButton = QtGui.QPushButton(SaveOptionsDialog)
        self.tempButton.setGeometry(QtCore.QRect(90, 20, 75, 23))
        self.tempButton.setObjectName(_fromUtf8("tempButton"))
        self.browseButton = QtGui.QPushButton(SaveOptionsDialog)
        self.browseButton.setGeometry(QtCore.QRect(170, 20, 75, 23))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.cancelButton = QtGui.QPushButton(SaveOptionsDialog)
        self.cancelButton.setGeometry(QtCore.QRect(250, 20, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))

        self.retranslateUi(SaveOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(SaveOptionsDialog)

    def retranslateUi(self, SaveOptionsDialog):
        SaveOptionsDialog.setWindowTitle(QtGui.QApplication.translate("SaveOptionsDialog", "Choose K: folder", None, QtGui.QApplication.UnicodeUTF8))
        self.dfltButton.setText(QtGui.QApplication.translate("SaveOptionsDialog", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.tempButton.setText(QtGui.QApplication.translate("SaveOptionsDialog", "TEMP", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("SaveOptionsDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("SaveOptionsDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SaveOptionsDialog = QtGui.QDialog()
    ui = Ui_SaveOptionsDialog()
    ui.setupUi(SaveOptionsDialog)
    SaveOptionsDialog.show()
    sys.exit(app.exec_())

