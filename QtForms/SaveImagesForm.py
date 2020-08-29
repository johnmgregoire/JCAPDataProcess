# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveImagesForm.ui'
#
# Created: Fri Feb 19 13:21:15 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SaveImagesDialog(object):
    def setupUi(self, SaveImagesDialog):
        SaveImagesDialog.setObjectName("SaveImagesDialog")
        SaveImagesDialog.resize(579, 408)
        self.buttonBox = QtWidgets.QDialogButtonBox(SaveImagesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 360, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.FilesTreeWidget = QtWidgets.QTreeWidget(SaveImagesDialog)
        self.FilesTreeWidget.setGeometry(QtCore.QRect(10, 10, 561, 341))
        self.FilesTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.FilesTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.FilesTreeWidget.setHeaderHidden(True)
        self.FilesTreeWidget.setExpandsOnDoubleClick(False)
        self.FilesTreeWidget.setObjectName("FilesTreeWidget")
        self.FilesTreeWidget.headerItem().setText(0, "1")
        self.FilesTreeWidget.header().setVisible(False)
        self.FilesTreeWidget.header().setCascadingSectionResizes(False)
        self.FilesTreeWidget.header().setStretchLastSection(True)
        self.overwriteCheckBox = QtWidgets.QCheckBox(SaveImagesDialog)
        self.overwriteCheckBox.setGeometry(QtCore.QRect(10, 370, 101, 31))
        self.overwriteCheckBox.setChecked(True)
        self.overwriteCheckBox.setObjectName("overwriteCheckBox")
        self.doneCheckBox = QtWidgets.QCheckBox(SaveImagesDialog)
        self.doneCheckBox.setGeometry(QtCore.QRect(120, 370, 81, 31))
        self.doneCheckBox.setChecked(False)
        self.doneCheckBox.setObjectName("doneCheckBox")
        self.epsCheckBox = QtWidgets.QCheckBox(SaveImagesDialog)
        self.epsCheckBox.setGeometry(QtCore.QRect(215, 370, 71, 31))
        self.epsCheckBox.setChecked(True)
        self.epsCheckBox.setObjectName("epsCheckBox")
        self.prependfilenameLineEdit = QtWidgets.QLineEdit(SaveImagesDialog)
        self.prependfilenameLineEdit.setGeometry(QtCore.QRect(285, 380, 113, 20))
        self.prependfilenameLineEdit.setObjectName("prependfilenameLineEdit")
        self.label = QtWidgets.QLabel(SaveImagesDialog)
        self.label.setGeometry(QtCore.QRect(290, 360, 101, 20))
        self.label.setObjectName("label")
        self.retranslateUi(SaveImagesDialog)
        self.buttonBox.accepted.connect(SaveImagesDialog.accept)
        self.buttonBox.rejected.connect(SaveImagesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveImagesDialog)

    def retranslateUi(self, SaveImagesDialog):
        SaveImagesDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "SaveImagesDialog", "ChooseImagesToSave", None
            )
        )
        self.overwriteCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesDialog", "overwrite files\n" "with same name", None
            )
        )
        self.doneCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesDialog", "convert\n" "to .done", None
            )
        )
        self.epsCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesDialog", "also save\n" ".eps", None
            )
        )
        self.label.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesDialog", "Prepend to filename:", None
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SaveImagesDialog = QtWidgets.QDialog()
    ui = Ui_SaveImagesDialog()
    ui.setupUi(SaveImagesDialog)
    SaveImagesDialog.show()
    sys.exit(app.exec_())
