# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\FileManagementForm.ui'
#
# Created: Mon Sep 21 13:50:54 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileManDialog(object):
    def setupUi(self, FileManDialog):
        FileManDialog.setObjectName("FileManDialog")
        FileManDialog.resize(560, 397)
        self.deletefoldersButton = QtWidgets.QPushButton(FileManDialog)
        self.deletefoldersButton.setGeometry(QtCore.QRect(170, 10, 131, 23))
        self.deletefoldersButton.setObjectName("deletefoldersButton")
        self.foldersTreeWidget = QtWidgets.QTreeWidget(FileManDialog)
        self.foldersTreeWidget.setGeometry(QtCore.QRect(0, 50, 551, 341))
        self.foldersTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.foldersTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foldersTreeWidget.setHeaderHidden(True)
        self.foldersTreeWidget.setExpandsOnDoubleClick(False)
        self.foldersTreeWidget.setObjectName("foldersTreeWidget")
        self.foldersTreeWidget.headerItem().setText(0, "1")
        self.foldersTreeWidget.header().setVisible(False)
        self.foldersTreeWidget.header().setCascadingSectionResizes(False)
        self.foldersTreeWidget.header().setStretchLastSection(True)
        self.findfoldersButton = QtWidgets.QPushButton(FileManDialog)
        self.findfoldersButton.setGeometry(QtCore.QRect(20, 10, 131, 23))
        self.findfoldersButton.setObjectName("findfoldersButton")
        self.endswithLineEdit = QtWidgets.QLineEdit(FileManDialog)
        self.endswithLineEdit.setGeometry(QtCore.QRect(400, 10, 113, 20))
        self.endswithLineEdit.setObjectName("endswithLineEdit")
        self.label = QtWidgets.QLabel(FileManDialog)
        self.label.setGeometry(QtCore.QRect(310, 10, 91, 21))
        self.label.setObjectName("label")
        self.retranslateUi(FileManDialog)
        QtCore.QMetaObject.connectSlotsByName(FileManDialog)

    def retranslateUi(self, FileManDialog):
        FileManDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "FileManDialog", "EXP+ANA file management", None
            )
        )
        self.deletefoldersButton.setText(
            QtCore.QCoreApplication.translate(
                "FileManDialog", "delete selected folders", None
            )
        )
        self.findfoldersButton.setText(
            QtCore.QCoreApplication.translate("FileManDialog", "find folders", None)
        )
        self.endswithLineEdit.setText(
            QtCore.QCoreApplication.translate("FileManDialog", ".incomplete", None)
        )
        self.label.setText(
            QtCore.QCoreApplication.translate(
                "FileManDialog", "EXP or ANA folder\n" "must end with ", None
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    FileManDialog = QtWidgets.QDialog()
    ui = Ui_FileManDialog()
    ui.setupUi(FileManDialog)
    FileManDialog.show()
    sys.exit(app.exec_())
