# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveButtonChoices.ui'
#
# Created: Fri Sep 04 21:12:56 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SaveOptionsDialog(object):
    def setupUi(self, SaveOptionsDialog):
        SaveOptionsDialog.setObjectName("SaveOptionsDialog")
        SaveOptionsDialog.resize(353, 63)
        self.dfltButton = QtWidgets.QPushButton(SaveOptionsDialog)
        self.dfltButton.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.dfltButton.setObjectName("dfltButton")
        self.tempButton = QtWidgets.QPushButton(SaveOptionsDialog)
        self.tempButton.setGeometry(QtCore.QRect(90, 20, 75, 23))
        self.tempButton.setObjectName("tempButton")
        self.browseButton = QtWidgets.QPushButton(SaveOptionsDialog)
        self.browseButton.setGeometry(QtCore.QRect(170, 20, 75, 23))
        self.browseButton.setObjectName("browseButton")
        self.cancelButton = QtWidgets.QPushButton(SaveOptionsDialog)
        self.cancelButton.setGeometry(QtCore.QRect(250, 20, 75, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.retranslateUi(SaveOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(SaveOptionsDialog)

    def retranslateUi(self, SaveOptionsDialog):
        SaveOptionsDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "SaveOptionsDialog", "Choose K: folder", None
            )
        )
        self.dfltButton.setText(
            QtCore.QCoreApplication.translate("SaveOptionsDialog", "x", None)
        )
        self.tempButton.setText(
            QtCore.QCoreApplication.translate("SaveOptionsDialog", "TEMP", None)
        )
        self.browseButton.setText(
            QtCore.QCoreApplication.translate("SaveOptionsDialog", "Browse", None)
        )
        self.cancelButton.setText(
            QtCore.QCoreApplication.translate("SaveOptionsDialog", "Cancel", None)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SaveOptionsDialog = QtWidgets.QDialog()
    ui = Ui_SaveOptionsDialog()
    ui.setupUi(SaveOptionsDialog)
    SaveOptionsDialog.show()
    sys.exit(app.exec_())
