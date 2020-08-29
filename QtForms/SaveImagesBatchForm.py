# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveImagesBatchForm.ui'
#
# Created: Fri Feb 19 13:21:05 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SaveImagesBatchDialog(object):
    def setupUi(self, SaveImagesBatchDialog):
        SaveImagesBatchDialog.setObjectName("SaveImagesBatchDialog")
        SaveImagesBatchDialog.resize(579, 455)
        self.buttonBox = QtWidgets.QDialogButtonBox(SaveImagesBatchDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 400, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.FilesTreeWidget = QtWidgets.QTreeWidget(SaveImagesBatchDialog)
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
        self.overwriteCheckBox = QtWidgets.QCheckBox(SaveImagesBatchDialog)
        self.overwriteCheckBox.setGeometry(QtCore.QRect(10, 370, 101, 31))
        self.overwriteCheckBox.setChecked(True)
        self.overwriteCheckBox.setObjectName("overwriteCheckBox")
        self.doneCheckBox = QtWidgets.QCheckBox(SaveImagesBatchDialog)
        self.doneCheckBox.setGeometry(QtCore.QRect(120, 370, 81, 31))
        self.doneCheckBox.setChecked(False)
        self.doneCheckBox.setObjectName("doneCheckBox")
        self.epsCheckBox = QtWidgets.QCheckBox(SaveImagesBatchDialog)
        self.epsCheckBox.setGeometry(QtCore.QRect(215, 370, 71, 31))
        self.epsCheckBox.setChecked(True)
        self.epsCheckBox.setObjectName("epsCheckBox")
        self.prependfilenameLineEdit = QtWidgets.QLineEdit(SaveImagesBatchDialog)
        self.prependfilenameLineEdit.setGeometry(QtCore.QRect(285, 381, 113, 20))
        self.prependfilenameLineEdit.setObjectName("prependfilenameLineEdit")
        self.label = QtWidgets.QLabel(SaveImagesBatchDialog)
        self.label.setGeometry(QtCore.QRect(290, 350, 101, 31))
        self.label.setObjectName("label")
        self.plotstyleoverrideCheckBox = QtWidgets.QCheckBox(SaveImagesBatchDialog)
        self.plotstyleoverrideCheckBox.setGeometry(QtCore.QRect(410, 360, 161, 31))
        self.plotstyleoverrideCheckBox.setChecked(False)
        self.plotstyleoverrideCheckBox.setObjectName("plotstyleoverrideCheckBox")
        self.filenamesearchLineEdit = QtWidgets.QLineEdit(SaveImagesBatchDialog)
        self.filenamesearchLineEdit.setGeometry(QtCore.QRect(140, 420, 261, 20))
        self.filenamesearchLineEdit.setObjectName("filenamesearchLineEdit")
        self.label_2 = QtWidgets.QLabel(SaveImagesBatchDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 410, 131, 31))
        self.label_2.setObjectName("label_2")
        self.retranslateUi(SaveImagesBatchDialog)
        self.buttonBox.accepted.connect(SaveImagesBatchDialog.accept)
        self.buttonBox.rejected.connect(SaveImagesBatchDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveImagesBatchDialog)

    def retranslateUi(self, SaveImagesBatchDialog):
        SaveImagesBatchDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog", "ChooseImagesToSave", None
            )
        )
        self.overwriteCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog", "overwrite files\n" "with same name", None
            )
        )
        self.doneCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog", "convert \n" "to .done", None
            )
        )
        self.epsCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog", "also save\n" ".eps", None
            )
        )
        self.label.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog",
                "Prepend to filename, in\n" "addition to auto-prepend",
                None,
            )
        )
        self.plotstyleoverrideCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog",
                "Override std plot plot options\n" "(colormap, fom range, etc.)",
                None,
            )
        )
        self.filenamesearchLineEdit.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog", "plate_id__, code__", None
            )
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate(
                "SaveImagesBatchDialog",
                "filename search strings for \n" "selecting images to save",
                None,
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SaveImagesBatchDialog = QtWidgets.QDialog()
    ui = Ui_SaveImagesBatchDialog()
    ui.setupUi(SaveImagesBatchDialog)
    SaveImagesBatchDialog.show()
    sys.exit(app.exec_())
